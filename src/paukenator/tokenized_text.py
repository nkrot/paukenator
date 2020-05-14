from paukenator.text import Text


class TokenizedText(Text):
    @classmethod
    def is_comment(cls, line):
        return len(line) > 0 and super().is_comment(line[0])

    def __init__(self, text):
        super().__init__()
        self.lines = []
        self.original = text

    def _line_as_words(self, line):
        return line
