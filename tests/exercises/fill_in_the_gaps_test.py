import pytest

from paukenator import Config
from paukenator.exercises import HiddenWord, FillInTheGaps


@pytest.fixture
def config1():
    cfg = Config()
    cfg.hide_ratio = 0.1
    cfg.hide_mode = HiddenWord.FULL
    return cfg


@pytest.fixture
def exercise1(text_sentence, config1):
    return FillInTheGaps(text_sentence, config1)


@pytest.fixture
def exercise2(text_sentence, config1):
    return FillInTheGaps(text_sentence, config1, number_gaps=True)


def test_exercise_1(exercise1):
    text = str(exercise1)
    words = text.split()
    assert isinstance(text, str)
    assert len(words) == 5
    assert words.count("...") == 1


def test_hide_word_1(exercise1):
    hw = exercise1.hide_word("Hello", 0)
    assert isinstance(hw, HiddenWord)
    assert str(hw) == "..."


def test_hide_word_2(exercise2):
    pos = 3
    hw = exercise2.hide_word("world", pos)
    assert isinstance(hw, HiddenWord)
    assert str(hw) == f"<<{pos+1} ... >>"


# TODO
# 1. How to test that some words are never hidden (_must_be_visible)?
