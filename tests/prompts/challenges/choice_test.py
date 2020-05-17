import pytest

from paukenator.prompts.challenges import Choice


@pytest.fixture
def correct_choice():
    return Choice("1", "Love", True)


@pytest.fixture
def wrong_choice():
    return Choice("2", "Hate", False)


def test_correct_choice(correct_choice):
    assert "1", correct_choice.name
    assert "Love", correct_choice.value
    assert correct_choice.correct


def test_wrong_choice(wrong_choice):
    assert "2", wrong_choice.name
    assert "Hate", wrong_choice.value
    assert not wrong_choice.correct


def test_serialization(correct_choice):
    assert "option 1: Love" == str(correct_choice)
