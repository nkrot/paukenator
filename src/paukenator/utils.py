import os
import re

from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "templates")


def load_template(fname):
    return Environment(loader=FileSystemLoader(TEMPLATES_DIR),
                       trim_blocks=True).get_template(fname)


class Selector(object):
    """
    Select items from an iterable according to given specification.
    Selectors are 1-based. Negative indices are not allowed.

    Examples:
    all   -- all sentences
    1..5  -- sentences 1 though 5, both ends included
    4..   -- starting from 4 and till the end
    ..10  -- starting from 1 and till 10 inclusive
    6     -- the 6th sentence (when would one need it?)
    """

    SPEC_REGEXEN = [
        re.compile(r'^(?P<p>[1-9]\d*)$'),
        re.compile(r'^(?P<s>[1-9]\d*)\.\.+(?P<e>[1-9]\d*)$'),
        re.compile(r'^(?P<s>[1-9]\d*)\.\.+$'),
        re.compile(r'^\.\.+(?P<e>[1-9]\d*)$'),
    ]

    @classmethod
    def parse_selector_spec(cls, spec):
        """Parse sentence selector specification

        TODO: support more complex cases
        1,3,5..10,20 -- sentences 1, 3, 5 through 10 and sentence 20
        p1..3 -- sentences in paragraphs 1 through 3
        """
        if spec.lower() == 'all':
            return [slice(0, None)]

        for regex in cls.SPEC_REGEXEN:
            m = re.search(regex, spec)
            if m:
                groups = m.groupdict()
                if 'p' in groups:
                    e = int(groups['p'])
                    s = e - 1
                else:
                    s = int(groups.get('s', 1)) - 1
                    e = int(groups['e']) if 'e' in groups else None
                return [slice(s, e)]

        raise ValueError(f"Wrong selector specification: '{spec}'")

    def __init__(self, spec=None):
        if isinstance(spec, type(self)):
            self.spec = spec.spec
            self.selectors = list(spec.selectors)
        else:
            self.spec = spec or 'all'
            self.selectors = self.parse_selector_spec(self.spec)

    def __call__(self, items):
        """
        Select item(s) from the given list <items> according to predefined
        spec and return the selection as a list, even if there is only one
        item.

        TODO
        1. can the selection be empty? return empty list or raise an error
        2. error if out of range?
        """
        if self.selectors:
            selected = []
            for sel in self.selectors:
                selected.extend(items[sel])
        else:
            selected = items
        return selected

    # def __repr__(self):
    #     return f"{self.__class__.__name__}: {self.spec}"

    def __str__(self):
        return str(self.spec)

    def __eq__(self, other):
        """TODO: well, is it really needed? So far used in tests only"""
        return self.selectors == other.selectors
