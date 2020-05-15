import pytest

import os

from paukenator import Text
from paukenator.nlp import SBD, WBD


def path_to(fname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), fname)


@pytest.fixture
def lines_2():
    with open(path_to('data/text.01.txt')) as fd:
        return [ln.strip() for ln in fd.readlines()]


@pytest.fixture
def lines_2_tokenized():
    with open(path_to('data/text.01.tok.txt')) as fd:
        return [ln.strip() for ln in fd.readlines()]


@pytest.fixture
def text_2_tokenized(lines_2_tokenized):
    text = Text()
    text.lines = lines_2_tokenized
    sbd = SBD()
    sbd.one_sentence_per_line = True
    sbd.annotate(text)
    wbd = WBD()
    wbd.split_by_whitespace = True
    wbd.annotate(text)
    return text
