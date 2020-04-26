import re

class WordTokenizer(object):
    def __init__(self, **kwargs):
        self.lang = kwargs.get('lang', 'deu')

    def __call__(self, string):
        return self.process(string)

    def process(self, string):
        words = []
        for wd in string.split():
            words.extend(self.tokenize_word(wd))
        return words

    def tokenize_word(self, string):
        """ TODO: this is ugly """
        if self._is_atomic(string):
            return [string]

        heads, tails = [], []
        while True:
            m = re.match(r'(\W)(.+)', string)
            if m:
                heads.append(m.group(1))
                string = m.group(2)
            else:
                break

        while True:
            m = re.match(r'(.+?)(\.\.+|\W)$', string)
            if m:
                tails.append(m.group(2))
                string = m.group(1)
            else:
                break

        return heads + [string] + tails

    def _is_atomic(self, string):
        return len(string) < 2 \
            or re.match(r'(\w+|-+)$', string) \
            or re.match(r'\d\d?\.$', string)
