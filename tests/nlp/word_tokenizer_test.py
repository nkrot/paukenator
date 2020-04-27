import pytest

from paukenator.nlp import WordTokenizer

@pytest.fixture
def wtok_deu():
    return WordTokenizer(lang='deu')

@pytest.fixture
def wtok_eng():
    return WordTokenizer(lang='eng')

def test_create_wtok_deu(wtok_deu):
    assert wtok_deu.lang == 'deu'

def test_create_wtok_eng(wtok_eng):
    assert wtok_eng.lang == 'eng'

@pytest.mark.parametrize(
    "inputstr, words", [
        ( '(Hallo, zusammen!)', '( Hallo , zusammen ! )' ),
        ( 'am 14. Januar',      'am 14. Januar' )
    ])
def test_wtok_process_deu(wtok_deu, inputstr, words):
    assert wtok_deu.process(inputstr) == words.split()
