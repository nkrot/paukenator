import os
import pytest

from paukenator import Config, Lesson
from paukenator.exercises import HiddenWord


def path_to(fname):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), fname)


@pytest.fixture
def lesson_ini():
    return path_to("data/lesson.ini")


@pytest.fixture
def lesson_config(lesson_ini):
    return Config.load_from_file(lesson_ini)


@pytest.fixture
def default_config():
    cfg = Config()
    return cfg


@pytest.mark.parametrize(
    'optname,optval', [
        ('lang',      'deu'),
        ('hide_ratio', 0.1),
        ('hide_mode',  HiddenWord.FULL),
        ('testmode',   Lesson.NON_INTERACTIVE),
        ('selector',   Lesson.Selector()),
    ])
def test_defaults(default_config, optname, optval):
    assert getattr(default_config, optname) == optval


def test_loading_from_file(lesson_config, lesson_ini):
    assert lesson_config.filename == lesson_ini
    assert lesson_config.lang == 'eng'
    assert lesson_config.filepath == 'data/text.01.txt'  # oops
    assert lesson_config.hide_ratio == 0.9


def test_update_config_from_file(lesson_ini, default_config):
    assert default_config.hide_ratio == 0.1
    assert str(default_config.selector) == 'all'
    default_config.update_from_file(lesson_ini)
    assert default_config.hide_ratio == 0.9
    assert str(default_config.selector) == '5..10'


def test_set_values(default_config):
    assert default_config.hide_ratio == 0.1
    assert default_config.hide_mode == HiddenWord.FULL
    default_config.hide_ratio = 0.2
    default_config.hide_mode = HiddenWord.PARTIAL
    assert default_config.hide_ratio == 0.2
    assert default_config.hide_mode == HiddenWord.PARTIAL
