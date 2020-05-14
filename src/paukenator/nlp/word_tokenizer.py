import re
from paukenator import Text, TokenizedText


class WordTokenizer(object):
    def __init__(self, **kwargs):
        self.lang = kwargs.get('lang', 'deu')

    def __call__(self, string):
        return self.process(string)

    def process(self, text):
        if isinstance(text, Text):
            res = TokenizedText(text)
            for line in text:
                tokens = self.process(line)
                res.lines.append(tokens)
        else:
            res = []
            for wd in text.split():
                res.extend(self.tokenize_word(wd))
        return res

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
                tails.insert(0, m.group(2))
                string = m.group(1)
            else:
                break

        return heads + [string] + tails

    def _is_atomic(self, string):
        return len(string) < 2 \
            or re.match(r'(\w+|-+)$', string) \
            or re.match(r'\d\d?\.$', string)
