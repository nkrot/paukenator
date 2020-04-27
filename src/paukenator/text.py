"""
"""
class Text(object):

    @classmethod
    def load(cls, fname, **kwargs):
        text = cls()
        with open(fname) as fd:
            text.lines = fd.read().split('\n')
        text.lang = kwargs.get('lang', 'deu')
        return text

    @classmethod
    def is_comment(cls, line):
        return line.startswith('#')

    def __init__(self):
        self.lines = []
        self.lang = 'deu'
        self.skip_comments = True

    def __iter__(self):
        return self.LinesIterator(self)

    def is_empty(self):
        return len(self.lines) == 0

    class LinesIterator(object):
        def __init__(self, text):
            self.text = text
            self.items = self.text.lines
            self.idx = -1
            self.last_idx = len(self.items) - 1

        def __iter__(self):
            return self

        def __next__(self):
            while True:
                self.idx += 1
                if self.idx <= self.last_idx:
                    item = self.items[self.idx]
                    if self.text.skip_comments and self.text.is_comment(item):
                        continue
                    return item
                raise StopIteration
