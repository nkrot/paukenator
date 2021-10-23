import os
import pytest

from paukenator import nlp
from paukenator.nlp import SentenceAnnotator, TokenAnnotator
from paukenator.text import Text as LessonText
from paukenator import Config


def path_to(fname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), fname)

# text.common.01

#@pytest.fixture
#def text_common_1_lines():
#    '''Entire file content of the file as lines (with trailing \n)'''
#    with open(path_to('data/text.common.01.txt')) as fd:
#        return fd.readlines()


@pytest.fixture
def text_common_1():
    '''Load the file into nlp.Text object'''
    file = path_to('data/text.common.01.txt')
    return nlp.Text.load_from_file(file)


@pytest.fixture
def text_common_1_tok_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.common.01.tok.txt')) as fd:
        return fd.readlines()


@pytest.fixture
def text_common_1_sent_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.common.01.sent.txt')) as fd:
        return fd.readlines()


# text.deu.01

@pytest.fixture
def text_deu_1_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.01.txt')) as fd:
        return fd.readlines()


@pytest.fixture
def text_deu_1():
    '''Load the file into nlp.Text object'''
    file = path_to('data/text.deu.01.txt')
    return nlp.Text.load_from_file(file)


# text.deu.02

@pytest.fixture
def text_deu_2_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.02.txt')) as fd:
        return fd.readlines()


@pytest.fixture
def text_deu_2():
    '''Load the file into nlp.Text object'''
    file = path_to('data/text.deu.02.txt')
    return nlp.Text.load_from_file(file)

# text.deu.03

@pytest.fixture
def text_deu_3_sent_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.03.sent.txt')) as fd:
        return fd.readlines()


@pytest.fixture
def text_deu_3():
    '''Load the file into nlp.Text object'''
    file = path_to('data/text.deu.03.txt')
    return nlp.Text.load_from_file(file)

# text.deu.04

@pytest.fixture
def text_deu_4_sent_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.04.sent.txt')) as fd:
        return fd.readlines()

@pytest.fixture
def text_deu_4_tok_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.04.tok.txt')) as fd:
        return fd.readlines()

@pytest.fixture
def text_deu_4():
    '''Load the file into nlp.Text object'''
    file = path_to('data/text.deu.04.txt')
    return nlp.Text.load_from_file(file)

# text.deu.05

@pytest.fixture
def text_deu_5_sent_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.05.sent.txt')) as fd:
        return fd.readlines()


@pytest.fixture
def text_deu_5_tok_lines():
    '''Entire file content of the file as lines (with trailing \n)'''
    with open(path_to('data/text.deu.05.tok.txt')) as fd:
        return fd.readlines()


@pytest.fixture
def text_deu_5():
    '''Load the file into nlp.Text object'''
    file = path_to('data/text.deu.05.txt')
    return nlp.Text.load_from_file(file)

# text.eng.01

@pytest.fixture
def text_eng_1_lesson_text():
    '''Load fle content as text.Text object (as used in Lesson).
    NOTE: this text contains comments that are not yet handled.
    '''
    file = path_to('data/text.eng.01.tok.txt')
    cfg = Config(lang='eng')
    return LessonText.load_from_file(file, cfg)


@pytest.fixture
def semdict():
    '''Create a mocked semantic dictionary (nlp.SemDict)
    TODO: change it to load data from a tailored resource data/semdict.json
    '''
    sd = nlp.SemDict()
    return sd


@pytest.fixture
def sa_deu():
    '''Return SentenceAnnotator for the German language'''
    return SentenceAnnotator(lang='deu')


@pytest.fixture
def sa_eng():
    '''Return SentenceAnnotator for the English language'''
    return SentenceAnnotator(lang='eng')


@pytest.fixture
def ta_deu():
    '''Return TokenAnnotator for the German language'''
    return TokenAnnotator(lang='deu')


@pytest.fixture
def ta_eng():
    '''Return TokenAnnotator for the English language'''
    return TokenAnnotator(lang='eng')


# notes about pytest
# - once annotation was done in one test method, the text modification
#   is not seen in another test method
