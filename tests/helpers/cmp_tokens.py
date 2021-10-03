from typing import List, Tuple
import difflib

from paukenator.nlp import Text, Line
from .common import CmpBase


class CmpTokens(CmpBase):
    '''Algorithm that compares texts at word level and detects differences in
    tokenization (splitting). Comparison works in line-by-line fashion.

    USAGE:
    comparer = CmpTokens()
    comparer(List[str], Text)
    if comparer.has_diff():
        print(comparer.diff_as_string())
    '''

    def __init__(self):
        super().__init__()
        self.diff_lines: List[Tuple[str, 'Line']] = None
        self.diff_tokens: List['CmpToken'] = None

    def __call__(self, expected: List[str], observed: Text) -> bool:
        assert isinstance(expected, list), \
            "Expecting list but got {}".format(type(expected))
        assert isinstance(observed, Text), \
            "Expecting Text but got {}".format(type(observed))
        return self._compare_lines(expected, observed)

    def _compare_lines(self, expected: List[str], observed: Text) -> bool:
        '''Compare line by line and collect different lines'''
        exp_lines = [line.strip() for line in expected if line.strip()]
        obs_lines = [line for line in observed.lines()
                     if not line.is_blank()]
        # if self.debug:
        #     print(f"+++ Expected +++\n{exp_lines}\n---")
        #     print(f"+++ Observed +++\n{obs_lines}\n---")
        self._validate(exp_lines, obs_lines)
        self._select_different_lines(exp_lines, obs_lines)
        self.equal = not self.diff_lines
        return self.equal

    # TODO:
    # 1. check how this works for two or three adjacent words that were
    #    tokenized differently

    def diff_as_string(self):
        '''Serialize difference as one string'''
        lines = ['']
        for exp, obs in self.diff_lines:
            # whole lines, the old and new ones
            lines.append("< {}".format(exp))
            lines.append("> {}".format(obs.tokenized()))
            # compute tokens that were resplit and differ in tokenization
            exp_tokens = exp.split()
            obs_tokens = obs.tokenized().split()
            self._select_different_tokens(exp_tokens, obs_tokens)
            # add changed tokens to the output
            for dtok in self.diff_tokens:
                lines.append(dtok.as_one_line())
            lines.append('')
        return "\n".join(lines)

    def _select_different_tokens(
            self, lwords: List[str], rwords: List[str]):
        '''Compare two lists of words, <lwords> and <rwords>:
        <lwords> is a list of words in a sentence (old tokenization)
        <rwords> is a list of words in the same sentence but retokenized
        '''
        if self.debug:
            print("<", " ".join(lwords))
            print(">", " ".join(rwords))

        # Ensure that a group with difference is surrounded by cmp_tokens
        # without difference. In this case outputting left/right context will
        # provide nicely looking string of text in CmpToken.as_one_line()

        # Compare two lists of words and create a list of CmpTokens
        # - if a word did not changed, it is a separate object of CmpToken
        # - if a word changed, old and new states go into one CmpToken
        cmp_tokens = []
        for cmp in difflib.ndiff(lwords, rwords):
            opcode, word = cmp[0], cmp[2:]
            if opcode == ' ':
                # unchanged word: ' word'
                cmp_tokens.append(CmpToken(word))
            elif opcode == '-':
                # old state: '- bzw' '- .'
                if not cmp_tokens[-1].has_diff():
                    cmp_tokens.append(CmpToken())
                cmp_tokens[-1].oadd(word)
            elif opcode == '+':
                # new state: '+ bzw.'
                if not cmp_tokens[-1].has_diff():
                    cmp_tokens.append(CmpToken())
                cmp_tokens[-1].nadd(word)

        # Link adjacent tokens to each other. This will be helpful later
        # when knowledge of context words is required.
        if CmpToken.WITH_CONTEXT:
            for idx in range(1, len(cmp_tokens)):
                cmp_tokens[idx-1].link_to(cmp_tokens[idx])

        # print(cmp_tokens)
        # print([cmpt for cmpt in cmp_tokens if cmpt.has_diff()])
        # for grp in cmp_tokens:
        #     if grp.has_diff():
        #         print(grp.as_one_line())

        # keep those tokens only that changed.
        self.diff_tokens = [cmpt for cmpt in cmp_tokens if cmpt.has_diff()]

    def _select_different_lines(self, exp: List[str], obs: List[Line]) -> None:
        '''Build pairs of expected and observed lines and select only those
        that differ in tokenization.
        Sets self.diff_lines: List[Tuple[str, Line]]
        '''
        self.diff_lines = []

        for e, o in zip(exp, obs):
            if e != o.tokenized():
                self.diff_lines.append((e, o))

        if self.debug:
            print(f"--- Pairs that differ: {len(self.diff_lines)} ---")
            for e, o in self.diff_lines:
                print("<", e)
                print(">", o.tokenized())
                print()

    def _validate(self, litems: List, ritems: List):
        '''Validate input'''
        llen, rlen = len(litems), len(ritems)
        assert llen == rlen, \
            f"Number of lines does not match: {llen} vs {rlen}"


class CmpToken(object):
    '''A token from the text that represents old and new states thereof.
    If the token splitting changed, it has old and new states and .old_parts
    and .new_parts are filled in.
    Otherwise, if the token splitting did not change, only .unchanged_parts
    will be filled.
    '''

    WITH_CONTEXT = True
    WITH_CONTEXT = True

    def __init__(self, word=None):
        self.old_parts = []
        self.new_parts = []
        self.unchanged_parts = []
        if word:
            self.add(word)
        # links to surrounding groups to provide context
        self._previous = None
        self._next = None

    def add(self, token: str):
        '''Add given <token> as unchanged.'''
        self.unchanged_parts.append(token)

    def oadd(self, token: str):
        '''Add given <token> as an old state'''
        self.old_parts.append(token)

    def nadd(self, token: str):
        '''Add given <token> as a new state'''
        self.new_parts.append(token)

    def __repr__(self):
        msg = "<{}: unchanged={}, old={}, new={}>".format(
            self.__class__.__name__, self.unchanged_parts, self.old_parts,
            self.new_parts)
        return msg

    def has_diff(self):
        return len(self.old_parts) or len(self.new_parts)

    def __str__(self):
        '''seems stupid but should produce correct result if current
        object carries no diff (has_diff = False)'''
        return self._join(self.unchanged_parts + self.old_parts + self.new_parts)

    def as_one_line(self) -> str:
        '''Serialize current object as *one* line'''
        if self.has_diff():
            string = "{} <> {}".format(
                self._join(self.old_parts), self._join(self.new_parts))
            if self.WITH_CONTEXT:
                if self._previous:
                    string = "{}\t{}".format(str(self._previous), string)
                if self._next:
                    string = "{}\t{}".format(string, str(self._next))
        else:
            string = "= {}".format(self._join(self.unchanged_parts))
        return string

    # def _xxx(self):
    #   # on two lines, provides better context in case context item(s)
    #   # is/are also groups with difference (has_diff = True)
    #   # < context litems
    #   # > content ritems
    #   # string = "< {}\n> {}".format(self._join(self.old_parts),
    #   #                              self._join(self.new_parts))
    #   return str

    def _join(self, items: List[str]) -> str:
        '''Serialize given list of strings to a tokenized string'''
        return " ".join(items)

    def link_to(self, other: 'CmpToken'):
        '''Link current token and <other> token together'''
        self._next = other
        other._previous = self
