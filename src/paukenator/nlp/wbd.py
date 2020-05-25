import re
from typing import List, Tuple

from paukenator import Text
from .word import Word


class WBD(object):

    def __init__(self, **kwargs):
        self.lang = kwargs.get('lang', 'deu')
        self.split_by_whitespace = False

    def annotate(self, text: Text) -> None:
        assert isinstance(text, Text), \
            f"Expecting instance of class Text but got {type(text)}"
        if not text.sentences_available:
            raise ValueError("Text must be split into sentences")

        for sent in text.sentences:
            sent.words = self.process(sent.text)

    def process(self, text: str) -> List[Word]:
        """Tokenize given string, return a list of Word objects"""
        assert isinstance(text, str), f"Expecting string but got {type(text)}"
        tokens = []
        for pos, wd in enumerate(text.split()):
            if self.split_by_whitespace:
                tokens.append((wd, pos))
            else:
                for token in self.tokenize_word(wd):
                    tokens.append((token, pos))
        words = self.convert_to_words(tokens, text)
        return words

    def tokenize_word(self, string: str) -> List[str]:
        """ TODO: this is ugly """
        if self._is_atomic(string):
            return [string]

        heads: List[str] = []
        tails: List[str] = []

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

    def _is_atomic(self, string: str) -> bool:
        """Test if given word is atmic and can not be further tokenized."""
        return bool(len(string) < 2
                    or string in ['bzw.', 'z.B.']
                    or re.match(r'(\w+|-+)$', string)
                    or re.match(r'\d\d?\.$', string))

    def convert_to_words(self,
                         tokens: List[Tuple[str, int]],
                         origtext: str) -> List[Word]:
        """
        Convert list of tokens to a list of Word objects.
        Each token is a tuple (str, idx) where str is the text of the word
        and idx is words position (0-based) in the original string.
        For example, the string 'Hello, world' is represented by 3 tokens
        [ ("Hello", 0), (",", 0), ("world", 1) ]

        TODO: this method should be made private.
        """
        prev_token = ('', 0)
        start_offset = -1

        words = []
        for curr_token in tokens:
            wd = Word()
            wd.data = origtext
            words.append(wd)
            # compute offsets
            start_offset += 1
            if prev_token[1] != curr_token[1]:
                # add 1 because we are looking at new word after a space
                start_offset += 1
            end_offset = start_offset + len(curr_token[0]) - 1
            wd.offsets = (start_offset, end_offset)
            # get ready for the next token
            start_offset = end_offset
            prev_token = curr_token

        exp_end_offset = len(origtext) - 1
        assert exp_end_offset == end_offset, \
            ("Last word end offset does not concide with end of the whole"
             " string: expected {} but got {}".format(
                 exp_end_offset, end_offset))

        return words
