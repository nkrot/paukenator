import re
from typing import List, Type

from .annotator import Annotator
from .annotations import Text, Token, WSWord
from .symbols import *


class TokenAnnotatorError(Exception):
    pass


class WrongSubtokenOffsetsError(TokenAnnotatorError):

    def __init__(self, token, offsets, msg=None):
        self.core_token = token
        self.subtoken_offsets = offsets
        self.message = msg or 'Incorrect offsets for extracting a subtoken'
        super().__init__()

    def __str__(self):
        return "{}: core={} target={}".format(self.message,
          repr(self.core_token), self.subtoken_offsets)


class Subtoken(object):
    '''Used in tokenization algorithm, does not need to be exposed outside'''

    def __init__(self, text: str, offsets=None):
        self.source = str(text)
        if not offsets:
            offsets = (0, len(self.source))
        self.start, self.end = offsets
        # links to adjacent words or subtokens
        self.previous = None
        self.next = None

    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return "<{}: offsets={} text={}>".format(
            self.__class__.__name__, self.offsets, self.text)

    def __str__(self):
        return self.source[self.start:self.end]

    @property
    def offsets(self):
        return (self.start, self.end)

    def trimleft(self, offsets: T_SPAN):
        '''Extract leading part (indentified by <offsets>)
        into a new Subtoken, updating the current token correspondingly.'''
        self._validate_span_for_extraction(offsets)
        subt = self._extract(offsets)
        # shift left boundary of the current token to the right
        self.start = subt.end
        self._link(subt, self)
        return subt

    def trimright(self, offsets: T_SPAN):
        ''''''
        self._validate_span_for_extraction(offsets)
        subt = self._extract(offsets)
        # shift right boundary of the current token to the left
        self.end = subt.start
        self._link(self, subt)
        return subt

    def _link(self, left, right):
        left.next = right
        right.previous = left

    def _extract(self, offsets: T_SPAN):
        # subtoken being extracted must have offsets relative the *full* token
        # from which it is extracted, meanwhile <offsets> is relative to
        # the subtoken that is being handled at this point in the algorithm.
        s = offsets[0] + self.start
        e = offsets[1] + self.start
        return self.__class__(self.source, (s, e))

    @property
    def text(self):
        return self.source[self.start:self.end]

    # TODO:
    # - which of these cases of offsets should lead to an error and which ones
    #   can be silently ignored?
    # - rethink how and when these validations should be used?

    def is_head_span(self, offsets: T_SPAN) -> bool:
        '''Tell if given span <offsets> is a prefix of the core token.'''
        if self.offsets == offsets:
            return False
        return True

    def is_tail_span(self, offsets: T_SPAN) -> bool:
        '''Tell if given span <offsets> is a suffix of the core token.'''
        if self.offsets == offsets:
            return False
        return True

    def _validate_span_for_extraction(self, offsets: T_SPAN):
        '''Check if given offsets are valid, that is, there is a subtoken
        that can be extracted from the current core token.

        TODO:
        - implemented only partially
        - add validations specific to trimleft and trimright operations
        - throw a more specific error(s)
        - duplicates is_head_span() and is_tail_span()
        '''
        if self.offsets == offsets:
            # it does not make sense extracting subtoken that spans the whole
            # core token or is wider that the latter.
            raise WrongSubtokenOffsetsError(self, offsets)


class TokenAnnotator(Annotator):
    '''Annotate text with annotations of type Token.
    Unlike WSWord, a Token is an linguistic annotation being more or less
    a lexeme itself without punctuation marks. Annotation of Tokens requires
    language-dependent knowledge and uses semantic dictionaries.

    TokenAnnotator requires annotations of class WSWord be available.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.split_by_whitespace = False

    @property
    def type(self) -> Type['Annotation']:
        '''Type of annotations produced by this annotator.'''
        return Token

    def annotate(self, text: Text) -> None:
        '''Split into tokens separating punctuation marks.'''

        for wsword in text.wswords():
            self.dprint(wsword)

            # the core token is the initial token that will be reduced by trimming
            # off the punctuation marks. At the end of the process, the core token
            # will also be a valid token that should be added as an annotation.
            core = Subtoken(wsword.text)
            core.next = wsword.next(wsword.line())
            self.dprint(repr(core))
            self.dprint("- next word:", repr(core.next))

            if self.split_by_whitespace:
                # basically, underlying WSWord
                subtokens = [core]
            else:
                subtokens = self._tokenize(core)

            # debug
            if self.debug:
                self.dprint("Subtokens:")
                for i, subt in enumerate(subtokens):
                    self.dprint(i, repr(subt))
                self.dprint()

            spans = [subt.offsets for subt in subtokens]

            self.annotate_spans(wsword, spans)

    def _tokenize(self, core: Subtoken) -> List[Subtoken]:
        subtokens: List[Subtoken] = []

        # TODO: move it to shared resources and extend
        ROMAN = '(II?I?|I?V|VII?I?|I?X)'  # some of roman numbers

        # handle LHS of the token
        changed = True
        while changed:
            m = re.match(r'[(\"\'\[]|--+', core.text)
            if m and core.is_head_span(m.span()):
                self.dprint(m)
                subtok = core.trimleft(m.span())
                self.dprint(repr(subtok), repr(core))
                subtokens.append(subtok)
            else:
                changed = False

        # handle RHS of the token
        changed = True
        while changed:
            m = re.search(r'([\])\"\'.,!?:;]|--+|\.\.+)$', core.text)
            if m and core.is_tail_span(m.span()):
                do_split = True
                self.dprint(m)

                if core.text in self.semdict('ABBREVIATIONS'):
                    do_split = False

                elif m[0] == '.' and core.next:
                    self.dprint("Checking right neighbour", repr(core.next))
                    # dont split after abbreviations, if
                    if core.next.text in {',', '!', '?'}:
                        # ex: um 5 p.m.,
                        do_split = False

                    elif core.next.text[0].islower():
                        # next word starts with a lowercase
                        # ex: du bzw. deine Familie
                        do_split = False

                    elif (re.match(rf'((\d+)|{ROMAN})\.$', core.text)
                          and (core.next.text in self.semdict('MONTH_NAMES') or
                               core.next.text in self.semdict('NOUNS_WITH_ORDINAL_NUMBER'))):
                        # ex: am 31. Juli
                        # ex: seit dem 11. Jahrhundert
                        # TODO: this one is not split
                        # ex: (25. Juli)
                        do_split = False

                if do_split:
                    subtok = core.trimright(m.span())
                    self.dprint(repr(subtok), repr(core))
                    subtokens.append(subtok)
                else:
                    changed = False
            else:
                changed = False

        subtokens.append(core)
        subtokens.sort()

        return subtokens
