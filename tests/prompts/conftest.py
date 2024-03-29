import os
import pytest

from paukenator.exercises import Exercise, HiddenWord


@pytest.fixture
def path_to():
    def _path_to(fname):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), fname)
    return _path_to


@pytest.fixture
def hidden_words():
    # ex: Hello , beautiful and amazing world !
    return [ HiddenWord('Hello', 0),
             HiddenWord('beautiful', 2),
             HiddenWord('amazing', 4) ]


@pytest.fixture
def exercise(hidden_words):
    sent = "Hello , beautiful and amazing world !"
    ex = Exercise(sent)
    ex.hidden_words = hidden_words
    return ex
