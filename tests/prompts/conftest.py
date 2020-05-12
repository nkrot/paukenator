import pytest

from paukenator import HiddenWord

@pytest.fixture
def hidden_words():
    # ex: Hello , beautiful and amazing world !
    return [ HiddenWord('Hello', 0),
             HiddenWord('beautiful', 2),
             HiddenWord('amazing', 4) ]
