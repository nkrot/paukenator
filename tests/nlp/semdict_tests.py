
import pytest
from paukenator.nlp.semdict import SemDictClassNotFoundError


def test_language(semdict):
    exp_langs = ['deu', 'eng']
    assert exp_langs[0] == semdict.lang, \
        'Default language should be {} but got {}'.format(
            exp_langs[0], semdict.lang)
    assert sorted(exp_langs) == semdict.languages(), \
        'Semdict is expected to support languages {} but got {}'.format(
            sorted(exp_langs), semdict.languages())


def test_list_semclasses(semdict):
    exp = 'ABBREVIATION'
    actual = semdict.semclasses()
    assert exp in actual, \
        "Expected class {} not found in dictionary among: {}".format(
            exp, actual)


@pytest.mark.parametrize("word, semclasses", [
    ("Okt.", ["MONTH_NAME"]),
    ("z.B.", ["NO_SENT_END", "ABBREVIATION"])
])
def test_find(semdict, word, semclasses):
    '''Method SemDict.find return all sem classes that given word belong to.'''
    exp = sorted(semclasses)
    actual = sorted(semdict.find(word))
    assert exp == actual, \
        "Expecting word '{}' to be in semclasses {} but got {}".format(
            word, exp, actual)


@pytest.mark.parametrize("query, expected", [
    ("Bier",                 False),
    ("Juni",                 True),
    (("Bier", "MONTH_NAME"), False),
    (("Juni", "MONTH_NAME"), True)
])
def test_has_word(semdict, query, expected):
    actual = semdict.has(query)
    assert expected == actual, \
        "Expecting query {} to be {} but got {}".format(
            query, expected, actual)


@pytest.mark.parametrize("query, expected", [
    ("Bier",                 False),
    ("Juni",                 True),
    (("Bier", "MONTH_NAME"), False),
    (("Juni", "MONTH_NAME"), True)
])
def test_in_operator(semdict, query, expected):
    '''Opreator `in` is an alias for .has() method'''
    actual = query in semdict
    assert expected == actual, \
        "Expecting query {} to be {} but got {}".format(
            query, expected, actual)


def test_raise_error_for_unknown_semclass(semdict):
    '''If we are checking a word with a specific semantic class,
    the class must exist in the dictionary. If this is not the case,
    raise an error.'''
    query = ("Hello", "DOES_NOT_EXIST")
    with pytest.raises(SemDictClassNotFoundError):
        semdict.has(query)
