from pathlib import Path
import nltk
from nltk.tokenize import sent_tokenize


tokenizer = nltk.RegexpTokenizer(r"([A-Z][A-Z0-9.]+|[0-9]+[,.][0-9]+|[cdjlmnst]'|qu'|[\w'-]+|\S)")


class Sentence:
    def __init__(self, text, nth):
        self.text = text
        self.nth = nth

    def __len__(self):
        return len(tokenizer.tokenize(self.text))

    @property
    def id(self):
        return self.nth

    def contains_pos(self, postag):
        return False

    def count_pos(self, postag):
        return 0


def read_corpus(path):
    corpus = []
    with open(path) as input_stream:
        content = input_stream.read()
    sents = [item.replace("\n", " ") for item in sent_tokenize(content)]
    for nth, sent in enumerate(sents):
        corpus.append(Sentence(sent, nth))
    return corpus
