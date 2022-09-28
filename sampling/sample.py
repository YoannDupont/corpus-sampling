"""Sample a given number of words given a corpus.

The allowed formats are: conllu, wikiner, text, apil.

This script will generate 2 files : (1) text file (2) id file to locate samples
in the corpus.
"""

import argparse
import sys
import random
from pathlib import Path

import sampling.conll as conll
import sampling.wikiner as wikiner
import sampling.wikinews as wikinews
import sampling.text as text
import sampling.apil as apil


def guess_format(pathname):
    if pathname.is_dir():
        return "wikinews"
    if str(pathname).endswith(".conllu") or str(pathname).endswith(".conllu.txt"):
        return "conllu"
    if pathname.suffix == ".txt":
        return "text"
    raise ValueError("Unhandled file format: {}".format(pathname.suffix))


def main(
    infilename,
    corpus_format="guess",
    sample_size=1000,
    min_size=5,
    max_size=60,
    output_dir=".",
    do_not_sample=None,
):
    infilepath = Path(infilename)
    if corpus_format == "guess":
        corpus_format = guess_format(infilepath)

    forbidden = set()
    if do_not_sample:
        with open(do_not_sample, encoding="utf-8") as input_stream:
            for line in input_stream:
                line = line.strip()
                if line:
                    forbidden.add(line)

    PN_tag = {"conllu": "PROPN", "wikiner": "NAM"}
    PN = PN_tag.get(corpus_format, "")

    basename = None
    if corpus_format == "conllu":
        corpus = conll.read_corpus(infilename)
    elif corpus_format == "wikiner":
        corpus = wikiner.read_corpus(infilename)
    elif corpus_format == "wikinews":
        corpus = wikinews.read_corpus(infilepath)
        basename = "{}-{}".format(Path(infilepath.parent).stem, infilepath.stem)
    elif corpus_format == "text":
        corpus = text.read_corpus(infilename)
    elif corpus_format == "apil":
        corpus = apil.read_corpus(infilename)
    random.shuffle(corpus)
    corpus = [sentence for sentence in corpus if sentence.id not in forbidden]

    n_toks = 0
    selected = []
    while n_toks < sample_size:
        sent = corpus.pop()
        if min_size <= len(sent.text.split()) <= max_size:
            selected.append(sent)
            n_toks += len(selected[-1])

    basename = basename or infilepath.stem
    textfile = Path(output_dir) / (basename + ".sample.txt")
    with open(textfile, "w") as output_stream:
        for sentence in selected:
            output_stream.write(f"{sentence.text}\n")

    idfile = Path(output_dir) / (basename + ".ids.txt")
    with open(idfile, "w") as output_stream:
        for sentence in selected:
            output_stream.write(f"{sentence.id}\n")

    reportfile = Path(output_dir) / (basename + ".report.txt")
    with open(reportfile, "w") as output_stream:
        n_sents = len(selected)
        n_propn = sum(sent.count_pos(PN) for sent in selected)
        output_stream.write(f"{n_sents} sentences\n")
        output_stream.write(f"{n_toks} tokens\n")
        if PN:
            output_stream.write(f"{n_propn} proper nouns\n")
        else:
            output_stream.write(f"No POS tags available.\n")


def parse_cl(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "infilename",
        type=str,
        help="The input file name."
    )
    parser.add_argument(
        "-f", "--corpus-format",
        choices=("guess", "conllu", "wikinews", "wikiner", "text", "apil"),
        default="guess",
        help="The format of the corpus."
    )
    parser.add_argument(
        "-s", "--sample-size",
        type=int,
        default=1000,
        help="The size of the sample in number of tokens (default: %(default)s)."
    )
    parser.add_argument(
        "-m", "--min-size",
        type=int,
        default=5,
        help="The minimum size of a sentence (default: %(default)s)."
    )
    parser.add_argument(
        "-x", "--max-size",
        type=int,
        default=60,
        help="The maximum size of a sentence (default: %(default)s)."
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="Output directory."
    )
    parser.add_argument(
        "-d", "--do-not-sample",
        metavar="FILE",
        type=str,
        help="A file containing a list of ids (one per line) that should not be sampled."
    )
    args = parser.parse_args(argv)

    main(**vars(args))


if __name__ == "__main__":
    parse_cl()
    sys.exit(0)
