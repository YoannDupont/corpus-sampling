class Sentence:
    def __init__(self, tokens, sent_line):
        toks, pos, ner = zip(*tokens)
        self.tokens = toks
        self.pos = pos
        self.ner = ner
        self.sent_line = sent_line

    def __len__(self):
        return len(self.tokens)

    @property
    def text(self):
        txt = " ".join(self.tokens)
        txt = txt.replace(" ,", ",")
        txt = txt.replace(" .", ".")
        return txt

    @property
    def id(self):
        return self.sent_line

    def contains_pos(self, postag):
        return any(pos == postag for pos in self.pos)

    def count_pos(self, postag):
        return sum(pos == postag for pos in self.pos)


def read_sentence(stream, sent_line):
    line = next(stream).strip()
    sent_line += 1
    if line:
        return Sentence([item.split("|") for item in line.split()], sent_line), sent_line
    else:
        return None, sent_line


def read_corpus(path):
    sentences = []
    nth = 0
    with open(path) as input_stream:
        try:
            while True:
                sentence, nth = read_sentence(input_stream, nth)
                if sentence:
                    sentences.append(sentence)
        except StopIteration:
            pass
    return sentences
