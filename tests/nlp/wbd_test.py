import pytest

from paukenator.nlp import WBD, Word


@pytest.fixture
def wbd_deu():
    return WBD(lang='deu')


@pytest.fixture
def wbd_eng():
    return WBD(lang='eng')


def test_create_wbd_deu(wbd_deu):
    assert wbd_deu.lang == 'deu'


def test_create_wbd_eng(wbd_eng):
    assert wbd_eng.lang == 'eng'


@pytest.fixture
def sample_1_str():
    return "(Hallo, zusammen!) Wie geht's ?"


@pytest.fixture
def sample_1_tuples():
    return [
        ('(',        0),
        ('Hallo',    0),
        (',',        0),
        ('zusammen', 1),
        ('!',        1),
        (')',        1),
        ('Wie',      2),
        ('geht',     3),
        ("'",        3),
        ('s',        3),
        ('?',        4)
    ]


@pytest.fixture
def sample_1_data():
    return [
        ('(',        (0, 0)),
        ('Hallo',    (1, 5)),
        (',',        (6, 6)),
        ('zusammen', (8, 15)),
        ('!',        (16, 16)),
        (')',        (17, 17)),
        ('Wie',      (19, 21)),
        ('geht',     (23, 26)),
        ("'",        (27, 27)),
        ('s',        (28, 28)),
        ('?',        (30, 30))
    ]


def test_convert_to_words(wbd_deu, sample_1_tuples, sample_1_str,
                          sample_1_data):
    words = wbd_deu.convert_to_words(sample_1_tuples, sample_1_str)
    for wd, src in zip(words, sample_1_data):
        assert wd.offsets == src[1], "Offsets do not match"
        assert wd.text == src[0], "Textual value does not match"


@pytest.mark.parametrize(
    "input_str, exp_tokenized_str", [
        ( '(Hallo, zusammen!)', '( Hallo , zusammen ! )' ),
        ( 'am 14. Januar',      'am 14. Januar' )
    ])
def test_wbd_process_deu(wbd_deu, input_str, exp_tokenized_str):
    words = wbd_deu.process(input_str)
    types = [type(wd) for wd in words]
    assert all(isinstance(wd, Word) for wd in words), \
        f"Returned value must be a list of Word objects but is: {types}"
    exp_num_tokens = len(exp_tokenized_str.split())
    assert exp_num_tokens == len(words), \
        "Number of tokens does not match"
    act_tokenized_str = " ".join([wd.text for wd in words])
    assert exp_tokenized_str == act_tokenized_str, \
        "Textual value of tokenized string does not match"

# TODO
# test .annotate(Text)
