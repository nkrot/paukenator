
from collections import defaultdict
from typing import List, Union, Iterable, Dict

from .errors import NLPError
from .symbols import *
from .resources import SEMDICT


class SemDictError(NLPError):
    pass


class SemDictClassNotFoundError(SemDictError):
    '''Raised when requested semantic class does not exist in the dictionary'''

    def __init__(self, lang: str, klass: str):
        msg = ("Requested semclass '{}' does not exist"
               " for the language '{}'").format(klass, lang)
        super().__init__(msg)


# class SemDictFailedLoadingError(SemDictError):
#     pass


class SemDict(object):
    '''Iterface to certain resources read from the file system. These resources
    provide information about words and classes to which they belong, for
    example, the word "Jan." is an abbreviation and is a name of a month.
    For the time being, the source for SemDict is in data from resouces.py.

    SemDict allows checking in the first place if a word belongs to a specific
    semantic class, like ABBREVIATION or MONTH_NAME mentioned earlier.

    SemDict is language-specific and its operations are controlled by working
    language (SemDict.lang) unless a language is given explicitly to a method.

    Semantic dictionary is read-only. Modifications are not saved.
    '''

    # TODO
    # - raise SemDictFailedLoadingError("Resource file not found: {fname}")
    # - raise an error if dictionary being queried is not found?
    #   or do it only in some strict mode, for checking consistency:
    #   say, for ensuring that wbd/sbd will be able to work

    # @classmethod
    # def load_from_file(cls, path: str):
    #     '''Load from given file rather than from default location.'''
    #     # does it have any applications rather than in testing
    #     pass

    def __init__(self, lang='deu'):
        self.lang: T_LANG = lang  # working language, affects lookup operations
        self._data: Dict[T_LANG, Dict[T_WORD, List[T_SEMCLASS]]] = None
        self._source: Dict = SEMDICT
        self._load_resources()

    def __repr__(self):
        num_words = len(self._data.get(self.lang, {}))
        return "<{}: lang={}, num_words={}>".format(
            self.__class__.__name__, self.lang, num_words)

    def __contains__(self, target: Union[str, Iterable]) -> bool:
        '''Alias for has()'''
        return self.has(target)

    def has(self, target: Union[str, Iterable]) -> bool:
        '''Check if <target> is available, optionally with given class.
        A <target> is either a word (str) or a pair (word, semclass).

        Examples
        >>> has('April') => True
        >>> has('April', 'MONTH_NAME') => True
        >>> has('April', 'PLANET') => False

        Raises
        - SemDictClassNotFoundError if requested semantic class does not exist
          in the dictionary (for the working language).
          TBD: Is not it too strict?

        TODO:
        ? test if query word is known as at least one of the classes
        >>> has('April', ['MONTH_NAME', 'PLANET']) => True
        '''
        if isinstance(target, str):
            return bool(self.find(target))
        else:
            word, expected_class = target
            self._validate_semclass(expected_class)
            return expected_class in self.find(word)

    def find(self, word: str) -> List:
        '''Return list of sem classes in which given word exists.
        Return empty list if nothing found.

        TODO: allow searching case (in)sensitively
        TODO: allow <word> to be a list? return a list of klasses for all
              items in the list.
        '''
        lang = self.lang
        finds = self._data.get(lang, {}).get(word, [])
        return list(finds)

    def languages(self) -> List[T_LANG]:
        '''Return sorted list of languages available in semantic dictionary.
        '''
        return sorted(self._langs)

    def semclasses(self, lang=None) -> List[T_SEMCLASS]:
        '''Return a sorted list of semantic classes defined in the dictionary
        for given language or working language.
        '''
        lang = lang or self.lang
        return sorted(self._semclasses.get(lang, []))

    # def __getitem__(self, klass):
    #     '''Return all words in given sem class'''
    #     pass

    def _load_resources(self) -> None:
        '''Populate current dictionary from configured resources.'''

        self._langs = set()
        self._semclasses = defaultdict(set)
        self._data = defaultdict(dict)

        for lang, data in self._source.items():
            self._langs.add(lang)
            lang_dict = self._data[lang]
            for klass, words in data.items():
                self._semclasses[lang].add(klass)
                for wd in words:
                    lang_dict.setdefault(wd, set()).add(klass)

    def _validate_semclass(self, klass: str) -> None:
        if klass not in self.semclasses():
            raise SemDictClassNotFoundError(self.lang, klass)
