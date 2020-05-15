
import pytest

from paukenator.nlp import Sentence, Word
from paukenator.text import Text


@pytest.fixture
def sentence():
    s = Sentence()
    s.data = "Hello, beautiful world!"
    s.offsets = (0, 22)
    return s


def test_text_sentence(sentence):
    linum = 0
    ts = Text.TextSentence(sentence, linum)
    # defined in TextSentence
    assert linum == ts.linum
    assert -1 == ts.num, "Mismatch in default value for <num> attribute"
    # defined in the underlying Sentence
    assert sentence.offsets == ts.offsets
    assert sentence.data == ts.data
    assert sentence.text == ts.text


@pytest.fixture
def words():
    text = "Hello, beautiful world!"
    params = [
        ("Hello",     (0, 4)),
        (",",         (5, 5)),
        ("beautiful", (7, 15)),
        ("world",     (17, 21)),
        ("!",         (22, 22))
    ]
    words = []
    for _, ofs in params:
        wd = Word()
        wd.data = text
        wd.offsets = ofs
        words.append(wd)
    return words


@pytest.fixture
def sentence_with_words(sentence, words):
    sentence.words = words
    s = Text.TextSentence(sentence, 0)
    return s


def test_words(sentence_with_words, words):
    assert len(sentence_with_words.words) == len(words)


def test_iterate_over_words(sentence_with_words, words):
    act_words = [wd for wd in sentence_with_words]
    assert len(words) == len(act_words), "Number of words does not match"
