class Text(object):

    @classmethod
    def load(cls, fname, **kwargs):
        text = cls()
        with open(fname) as fd:
            text.lines = fd.read().split('\n')
        text.lang = kwargs.get('lang', 'deu')
        return text

    def __iter__(self):
        return iter(self.lines)

    def __init__(self):
        self.lines = []
        self.lang = 'deu'
