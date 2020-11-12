from pathlib import Path
import nltk
from nltk.tokenize import sent_tokenize


tokenizer = nltk.RegexpTokenizer(r"([A-Z][A-Z0-9.]+|[0-9]+[,.][0-9]+|[cdjlmnst]'|qu'|[\w'-]+|\S)")


class Sentence:
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def __len__(self):
        return len(tokenizer.tokenize(self.text))

    @property
    def id(self):
        return self.url

    def contains_pos(self, postag):
        return False

    def count_pos(self, postag):
        return 0


def read_corpus(path):
    txts = list(path.glob("*.txt"))
    parent = Path(path.parent)
    urlfile = parent / "{}-{}-urls.txt".format(parent.name, path.name)
    urls = {}
    with open(urlfile) as input_stream:
        for line in input_stream:
            line = line.strip()
            if not line:
                continue
            key, value = line.split("\t")
            urls[key] = value
    corpus = []
    for txt in txts:
        url = urls[txt.stem]
        with open(txt) as input_stream:
            content = input_stream.read()
        sents = [item.replace("\n", " ") for item in sent_tokenize(content)]
        for sent in sents:
            corpus.append(Sentence(sent, url))
    return corpus
