"""tests for token annotator"""

from paukenator.nlp import TokenAnnotator, Token
from helpers import CmpTokens


def test_has_property_type():
    assert hasattr(TokenAnnotator, "type"), \
        ("TokenAnnotator must have a property `type` that returns the type of"
         " created annotations.")

    exp, actual = Token, TokenAnnotator().type
    assert exp == actual, \
        (f"TokenAnnotator is expected to produce objects of type {exp} but"
         f" got {actual}")


def test_creates_annotations(text_deu_3):
    '''Check that the annotator actually creates something'''
    text = text_deu_3
    TokenAnnotator()(text)
    actual = len(text.tokens())
    assert 0 < actual, "Annotator did not create any annotations."


def test_returned_type(text_deu_3):
    '''SentenceAnnotator is supposed to create annotations of type Sentence.'''
    text = text_deu_3
    TokenAnnotator()(text)
    types = [isinstance(token, TokenAnnotator().type)
             for token in text.tokens()]
    msg = "Not all results are annotations of type {}."
    assert all(types), msg.format(TokenAnnotator().type)


def test_common_1_as_deu(text_common_1, text_common_1_tok_lines):
    '''Compare expected vs. automatic tokens.
    This text should be tokenized without using any language-specific info.
    '''
    text = text_common_1
    wtok = TokenAnnotator(lang='deu')
    #wtok. # TODO: reset semdict to empty
    wtok(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_common_1_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_common_1_as_eng(text_common_1, text_common_1_tok_lines):
    '''Compare expected vs. automatic tokens.
    This text should be tokenized without using any language-specific info.
    '''
    text = text_common_1
    wtok = TokenAnnotator(lang='eng')
    #wtok. # TODO: reset semdict to empty
    wtok(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_common_1_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_deu_4(text_deu_4, text_deu_4_tok_lines):
    '''Compare expected vs. automatic tokens'''
    text = text_deu_4
    TokenAnnotator(lang='deu')(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_deu_4_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_deu_5(text_deu_5, text_deu_5_tok_lines):
    '''Compare expected vs. automatic tokens'''
    text = text_deu_5
    TokenAnnotator(lang='deu')(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_deu_5_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()
