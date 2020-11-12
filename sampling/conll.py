"""Package to read CoNLL-U sentences.

Named conll.py to avoid collision with the conlly package in pypi.
"""

class Sentence:
    def __init__(self, metadatas, tokens):
        self.metadatas = metadatas
        self.tokens = tokens

    def __len__(self):
        return len(self.tokens)

    @property
    def text(self):
        return self.metadatas["text"]

    @property
    def id(self):
        return self.metadatas["sent_id"]

    def contains_pos(self, postag):
        return any(line[3] == postag for line in self.tokens)

    def count_pos(self, postag):
        return sum(line[3] == postag for line in self.tokens)


def read_sentence(stream):
    metadatas = {}
    tokens = []
    for line in stream:
        line = line.strip()
        if line:
            if line.startswith("# "):
                key, value = line.split(" = ", 1)
                key = key[2:]
                metadatas[key] = value
            else:
                tokens.append(line.split("\t"))
        else:
            break
    if tokens:
        return Sentence(metadatas, tokens)


def read_corpus(path):
    sentences = []
    with open(path) as input_stream:
        while True:
            sentence = read_sentence(input_stream)
            if sentence:
                sentences.append(sentence)
            else:
                break
    return sentences
