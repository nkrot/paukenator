from typing import List, Type
from .symbols import *
from .resources import SEMDICT


class Annotator(object):
    '''A common base class for all annotators, Works a la abstract class:
    it should not be instantiated directly.
    '''

    def __init__(self, **kwargs):
        self.lang = kwargs.get('lang', 'deu')
        self.debug = kwargs.get('debug', False)

    def semdict(self, name: str, lang=None) -> set:
        '''Return content of the semantic dictionary named <name> for
        the current language'''
        lang = lang or self.lang
        d = set(SEMDICT.get(lang, {}).get(name, []))
        return list(d)

    @property
    def type(self) -> Type['Annotation']:
        '''This method is designed to return the type of the annotation that is
        produced by specific Annotator. Every subclass of Annotator is supposed
        to redefine this method and return what is appropriate for the specific
        Annotator subclass.
        '''
        raise RuntimeError("Subclass must redefine this method")

    def dprint(self, *args):
        '''Print given message if in debug mode'''
        if self.debug:
            print(*args)

    def annotate(self, text: 'Text'):
        '''Implements core functionality of the annotator: annotates given text
        in place with appropriate annotations. Every subclass of Annotator
        must redefine this method.
        '''
        raise RuntimeError("Subclass must redefine method annotate")

    def __call__(self, *args, **kwargs):
        '''An alias to annotate()'''
        return self.annotate(*args, **kwargs)

    def annotate_spans(self, parent: 'Annotation', spans: List[T_SPAN],
                       klass=None):
        '''Create annotations of type <klass> or if not given, of type
        <self.type>, for substrings described by <spans> (each span being
        a tuple of start and end offset) and register them as annotations of
        <parent> annotation.
        For example, a Text or a Sentence can thus be annotated with
        annotations of type WSWord or Token.
        '''
        self._validate_spans(spans)
        klass = klass or self.type
        for span in sorted(spans):
            parent.add_annotation(klass(span))

    def _validate_spans(self, spans: List[T_SPAN]) -> None:
        # TODO: check spans do not overlap
        # TODO: throw AnnotatorError
        for span in spans:
            if len(span) != 2:
                raise ValueError("A span must contain exactly two values but"
                                 " got {}: {}".format(len(span), span))
            if span[0] > span[1]:
                raise ValueError("Offset values in a span must be in ascending"
                                 " order but got: {}".format(span))
            tests = [isinstance(v, int) for v in span]
            if not all(tests):
                msg = "Span values must be of type int but got: {}".format(span)
                raise ValueError(msg)

