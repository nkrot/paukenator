"""tests for sentence annotator"""

from paukenator.nlp import SentenceAnnotator, Sentence
from helpers import CmpLines

# Plan
# - test some language independent behaviour
# - test some tricky cases of DEU
# - test rules that require SEMDICT: check w/o and with
# - check that SentenceAnnotator produces annotations of type Sentence


def test_has_property_type():
    assert hasattr(SentenceAnnotator, "type"), \
        ("SentenceAnnotator must have a property `type` that returns the type"
         " of created annotations.")

    exp, actual = Sentence, SentenceAnnotator().type
    msg = ("SentenceAnnotator is expected to produce objects of type {} but"
           " got {}.")
    assert exp == actual, msg.format(exp, actual)


def test_creates_annotations(sa_deu, text_deu_3):
    '''Check that the annotator actually creates something'''
    text = text_deu_3
    sa_deu(text)
    actual = len(text.sentences())
    assert 0 < actual, "Annotator did not create any annotations."


def test_returned_type(sa_deu, text_deu_3):
    '''SentenceAnnotator is supposed to create annotations of type Sentence.'''
    text = text_deu_3
    sa_deu(text)
    types = [isinstance(sent, sa_deu.type) for sent in text.sentences()]
    msg = "Not all results are annotations of type {}."
    assert all(types), msg.format(sa_deu.type)


def test_annotator_uses_semdict_deu(sa_deu):
    '''Check that semdict in the annotator has certain semclasses that are
    used in the rules.'''
    # The rules use the following classes:
    exp_classes = {'MONTH_NAME', 'NOUN_WITH_ORDINAL_NUMBER', 'NO_SENT_END'}
    # and the dictionary provides the following classes
    act_classes = set(sa_deu.semdict.semclasses())
    missing = list(exp_classes - act_classes)
    assert not missing, \
        "SemDict for {} must have semclass(es) {} but it does not.".format(
            sa_deu.semdict.lang, missing)


def test_common_1_as_deu(sa_deu, text_common_1, text_common_1_sent_lines):
    '''Compare expected vs. automatic sentences.
    This text should be processed language-agnostically.
    '''
    # sdet.semdict = empty # TODO: set dictionaries to be empty
    sa_deu(text_common_1)
    comparer = CmpLines()
    comparer(text_common_1_sent_lines, text_common_1)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_common_1_as_eng(sa_eng, text_common_1, text_common_1_sent_lines):
    '''Compare expected vs. automatic sentences.
    This text should be processed language-agnostically.
    '''
    # sdet.semdict = empty # TODO: set dictionaries to be empty
    sa_eng(text_common_1)
    comparer = CmpLines()
    comparer(text_common_1_sent_lines, text_common_1)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_deu_3(sa_deu, text_deu_3, text_deu_3_sent_lines):
    '''Compare expected vs. automatic sentences'''
    sa_deu(text_deu_3)
    comparer = CmpLines()
    comparer(text_deu_3_sent_lines, text_deu_3)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_deu_4(sa_deu, text_deu_4, text_deu_4_sent_lines):
    '''Compare expected vs. automatic sentences'''
    sa_deu(text_deu_4)
    comparer = CmpLines()
    comparer(text_deu_4_sent_lines, text_deu_4)
    assert comparer.no_diff(), comparer.diff_as_string()


def test_deu_5(sa_deu, text_deu_5, text_deu_5_sent_lines):
    '''Compare expected vs. automatic sentences'''
    sa_deu(text_deu_5)
    comparer = CmpLines()
    comparer(text_deu_5_sent_lines, text_deu_5)
    assert comparer.no_diff(), comparer.diff_as_string()
