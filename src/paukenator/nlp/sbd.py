from .. import Text
from . import Sentence


class SBD(object):
    """
    Sentence Boundary Disambiguation (SBD)
    """

    def __init__(self, lang=None):
        self.lang = lang or 'deu'
        self.one_sentence_per_line = True

    def annotate(self, text: Text):
        assert isinstance(text, Text), \
            f"Expecting instance of class Text but got {type(text)}"

        for linum, line in enumerate(text.lines):
            if text.is_comment(line) or len(line) == 0:
                continue
            for sent in self.process(line):
                text.add_sentence(sent, linum)

    def process(self, string: str):
        """TODO: rudimentary implementation """
        assert isinstance(string, str), \
            f"This method expects a String but got {type(string)}"
        assert self.one_sentence_per_line, \
            "For now only one_sentence_per_line processing is supported"
        s = Sentence()
        s.data = string  # TODO: not really necessary
        s.offsets = (0, len(string)-1)
        return [s]
