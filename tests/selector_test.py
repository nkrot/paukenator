import pytest

from paukenator import Selector


@pytest.fixture
def empty_selector():
    return Selector()


@pytest.fixture()
def items():
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']


def test_fields(empty_selector):
    assert hasattr(empty_selector, "spec")
    assert hasattr(empty_selector, "selectors")


def test_empty_selector_selects_all(empty_selector, items):
    selected = empty_selector(items)
    assert len(items) == len(selected), \
        ("Length of selected subset must be equal to length of"
         " original list")
    assert items == selected, \
        "Selected subset should be equal to the original list"


@pytest.mark.parametrize("spec", [
    "1,2", "1..-1", "1,2,3", "0..2", "0..", ".."
])
def test_error_on_wrong_specifications(spec):
    with pytest.raises(ValueError):
        Selector(spec)


@pytest.mark.parametrize("spec, exp_subset", [
    ("2",      ["b"]),
    ("1..4",   ['a', 'b', 'c', 'd']),
    ("3..5",   ['c', 'd', 'e']),
    ("3..3",   ['c']),
    ("9..11",  ['i', 'j', 'k']),
    ("..3",    ['a', 'b', 'c']),
    ("10..",   ['j', 'k', 'l']),
    ("12..",   ['l']),
    ("all",    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']),
    # ("20..", []) # TODO/TBD: out of range
])
def test_parse_selector_spec(items, spec, exp_subset):
    selector = Selector(spec)
    act_subset = selector(items)
    assert exp_subset == act_subset, \
        "Selected subset does not match the expectation"

