import pytest

# from paukenator.nlp import Sentence, Word
# from paukenator import Text


# TODO: same fixtures in text_sentence_test.py

# @pytest.fixture
# def words():
#     text = "Hello, beautiful world!"
#     params = [
#         ("Hello",     (0, 4)),
#         (",",         (5, 5)),
#         ("beautiful", (7, 15)),
#         ("world",     (17, 21)),
#         ("!",         (22, 22))
#     ]
#     words = []
#     for _, ofs in params:
#         wd = Word()
#         wd.data = text
#         wd.offsets = ofs
#         words.append(wd)
#     return words


# @pytest.fixture
# def sentence(words):
#     s = Sentence()
#     s.data = "Hello, beautiful world!"
#     s.offsets = (0, 22)
#     s.words = words
#     return s


# @pytest.fixture
# def text_sentence(sentence):
#     ts = Text.TextSentence(sentence, 1)
#     return ts
