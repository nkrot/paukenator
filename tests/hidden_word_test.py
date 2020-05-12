
import pytest

from paukenator.hidden_word import HiddenWord

def test_constants():
    assert HiddenWord.NOWORD == '...'
    assert HiddenWord.FULL == 1
    assert HiddenWord.PARTIAL == 2

@pytest.mark.parametrize("word,expected", [
    ("hello", False),
    (",",     True),
    ("!)",    True),
    ("-",     True),
    ("zhopa-s-ushami", False)
])
def test_is_always_visible(word, expected):
    assert expected == HiddenWord.is_always_visible(word)

@pytest.mark.parametrize(
    "word,idx,kwargs,expected", [
    ("apple",  1, None, '...'),
    ("banana", 2, {'include_position' : True}, '<<3 ... >>'),
    ("cherry", 3, {'hide_mode': HiddenWord.FULL}, '...'),
    ("kiwi",   4, {'hide_mode': HiddenWord.PARTIAL}, 'k...i'),
    ("fig",    5, {'hide_mode': HiddenWord.PARTIAL},  'f..'),
    ("coconut", 6, {'hide_mode': HiddenWord.FULL,
                   'include_position' : True}, '<<7 ... >>'),
    ("lime",   7, {'hide_mode': HiddenWord.PARTIAL,
                   'include_position' : True}, '<<8 l...e >>'),
    ("fig",    8, {'hide_mode': HiddenWord.PARTIAL,
                   'include_position' : True}, '<<9 f.. >>'),
])
def test_words(word,idx,kwargs,expected):
    if kwargs:
        hw = HiddenWord(word, idx, **kwargs)
    else:
        hw = HiddenWord(word, idx)
    assert word == hw.text
    assert idx == hw.position
    assert expected == hw.hidden
    assert expected == str(hw)

