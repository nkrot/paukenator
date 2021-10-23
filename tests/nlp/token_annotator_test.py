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


def test_creates_annotations(ta_deu, text_deu_3):
    '''Check that the annotator actually creates something'''
    text = text_deu_3
    ta_deu(text)
    actual = len(text.tokens())
    assert 0 < actual, "Annotator did not create any annotations."


def test_returned_type(ta_deu, text_deu_3):
    '''SentenceAnnotator is supposed to create annotations of type Sentence.'''
    text = text_deu_3
    ta_deu(text)
    types = [isinstance(token, ta_deu.type) for token in text.tokens()]
    msg = "Not all results are annotations of type {}."
    assert all(types), msg.format(ta_deu.type)


def test_common_1_as_deu(ta_deu, text_common_1, text_common_1_tok_lines):
    '''Compare expected vs. automatic tokens.
    This text should be tokenized without using any language-specific info.
    '''
    text = text_common_1
    # ta_deu.  # TODO: reset semdict to empty
    ta_deu(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_common_1_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_common_1_as_eng(ta_eng, text_common_1, text_common_1_tok_lines):
    '''Compare expected vs. automatic tokens.
    This text should be tokenized without using any language-specific info.
    '''
    text = text_common_1
    # ta_eng.  # TODO: reset semdict to empty
    ta_eng(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_common_1_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_annotator_uses_semdict_deu(ta_deu):
    '''Check that semdict in the annotator has certain semclasses that are
    used in the rules.'''
    # The rules use the following classes:
    exp_classes = {'ABBREVIATION', 'MONTH_NAME', 'NOUN_WITH_ORDINAL_NUMBER'}
    # and the dictionary provides the following classes
    act_classes = set(ta_deu.semdict.semclasses())
    missing = list(exp_classes - act_classes)
    assert not missing, \
        "SemDict for {} must have semclass(es) {} but it does not.".format(
            ta_deu.semdict.lang, missing)


def test_deu_4(ta_deu, text_deu_4, text_deu_4_tok_lines):
    '''Compare expected vs. automatic tokens'''
    text = text_deu_4
    ta_deu(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_deu_4_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_deu_5(ta_deu, text_deu_5, text_deu_5_tok_lines):
    '''Compare expected vs. automatic tokens'''
    text = text_deu_5
    ta_deu(text)
    comparer = CmpTokens()
    # comparer.debug = True
    comparer(text_deu_5_tok_lines, text)
    assert comparer.no_diff(), comparer.diff_as_string()
