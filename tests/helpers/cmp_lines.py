from typing import List, Union

from paukenator.nlp import Text, Line
from .common import CmpBase


class CmpLines(CmpBase):

    def __call__(self, expected: List[str], observed: Text):
        assert isinstance(expected, list), \
            "Expecting list but got {}".format(type(expected))
        assert isinstance(observed, Text), \
            "Expecting Text but got {}".format(type(observed))
        return self._compare_lines(expected, observed)

    def _compare_lines(self, expected: List[str], observed: Text):
        '''Compare two sources line by line and collectd differences'''
        expected = [line.strip() for line in expected if line.strip()]
        observed = [str(sent) for sent in observed.sentences()]
        if self.debug:
            print("Line counts", len(expected), len(observed))
            print("--- expected ---")
            print(expected)
            print("--- actual ---")
            print(observed)
        # group items from left and right sides
        cmp_lines = self.align(expected, observed)
        # select groups that have difference distinct
        self.diffs = [cmp for cmp in cmp_lines if cmp.has_diff()]
        self.equal = len(self.diffs) == 0
        return self.equal

    def align(self, litems: List[str], ritems: List[str]):
        '''Group items from left and right sides such that one groups contains
        items from both sides that sum up to the same string.
        '''
        litems, ritems = list(litems), list(ritems)
        cmps = [CmpLine()]
        c_iter = 0
        while litems or ritems:
            c_iter += 1
            assert c_iter < 1000, f"Infinite loop? Its already {c_iter} cycles"
            cmp = cmps[-1]
            if cmp.old_is_shorter() or cmp.is_empty():
                cmp.oadd(litems.pop(0))
            elif cmp.new_is_shorter():
                cmp.nadd(ritems.pop(0))
            else:
                cmps.append(CmpLine())
        assert not litems, f"Left side must be empty but got {litems}"
        assert not ritems, f"Right side must be empty but got {ritems}"
        return cmps

    def diff_as_string(self) -> str:
        '''Serialize different lines to a multi-line string.
        Previous state is prefixed with <, new state is prefixed with >

        Example:
        < Sentence 1. Sentence 2
        > Sentence 1.
        > Sentence 2.
        '''
        lines = []
        for cmp in self.diffs:
            lines.append("")
            lines.append(str(cmp))
        return "\n".join(lines)


class CmpLine(object):
    '''A container for a partitioned line of text.'''

    def __init__(self, old_parts=None, new_parts=None):
        self.old_parts = []
        self.new_parts = []
        if old_parts:
            self.oadd(old_parts)
        if new_parts:
            self.nadd(new_parts)

    def oadd(self, line: Union[str, List[str]]):
        if isinstance(line, list):
            self.old_parts.extend(line)
        else:
            self.old_parts.append(line)

    def nadd(self, line: Union[str, List[str]]):
        if isinstance(line, list):
            self.new_parts.extend(line)
        else:
            self.new_parts.append(line)

    def has_diff(self):
        return self.old_parts != self.new_parts

    def __str__(self):
        lines = [
            self._join(self.old_parts, "<"),
            self._join(self.new_parts, ">")
        ]
        return "\n".join(lines)

    def _join(self, lines: List[str], label: str):
        return "\n".join(["{} {}".format(label, line) for line in lines])

    def old_is_shorter(self) -> bool:
        return self._len(self.old_parts) < self._len(self.new_parts)

    def new_is_shorter(self) -> bool:
        return self._len(self.new_parts) < self._len(self.old_parts)

    def _len(self, lst):
        '''length w/o spaces'''
        return "".join(lst).replace(' ', '')

    def is_empty(self):
        return not( self.old_parts or self.new_parts )
