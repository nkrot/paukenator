import io
import os
import re
import sys
import configparser

import paukenator
import paukenator.exercises


class Config(object):
    """
    Config object provides a value for every configurable parameter in
    the system.

    TODO: messy, uses both internal (in-code) and external (user) terminology,
    for example, selector/select, hide_mode/hide_word. Think how to unify.
    """
    def __init__(self):
        super().__setattr__('filename', None)
        super().__setattr__('options', {
            'lang'        : 'deu',
            'filepath'    : None,
            'hide_ratio'  : 0.1,
            'hide_mode'   : paukenator.exercises.HiddenWord.FULL,
            'testmode'    : paukenator.Lesson.NON_INTERACTIVE,
            'selector'    : paukenator.Lesson.Selector()
        })

    def __getattr__(self, name):
        try:
            return self.options[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        if name in self.options:
            if value is not None:
                self.options[name] = value
        elif name in ['filename']:
            super().__setattr__(name, value)
        else:
            raise AttributeError

    def __str__(self):
        return "\n".join([f"{k} = {v}" for k, v in self.options.items()])

    @classmethod
    def load_from_file(cls, fd):
        config_from_file = configparser.ConfigParser(
            inline_comment_prefixes=('#',))

        config = cls()

        if isinstance(fd, io.IOBase):
            config_from_file.read_file(fd)
            config.filename = fd.name
        elif isinstance(fd, str):
            config_from_file.read(fd)
            config.filename = fd
        else:
            msg = f"Cannot read config from the object of type {type(fd)}"
            raise ValueError(msg)

        for section in config_from_file.sections():
            cfg = config_from_file[section]
            for key, val in cfg.items():
                converter = getattr(config, f"convert_{key}")
                nrm_name, nrm_value = converter(val)
                setattr(config, nrm_name, nrm_value)

        return config

    def update_from_file(self, fd):
        """Update current Config object with corresponding values from other
        Config object read from the configuration file (:fd:).
        NOTE that *all* parameters will be updated, because every Config object
        carries the complete set of parameters and we dont know which of them
        were actually read from the config file.
        """
        config_from_file = self.__class__.load_from_file(fd)
        self.options.update(config_from_file.options)

    def convert_hide_ratio(self, val):
        return ('hide_ratio', float(val))

    def convert_hide_word(self, value):
        mapping = {
            'fully'     : paukenator.exercises.HiddenWord.FULL,
            'partially' : paukenator.exercises.HiddenWord.PARTIAL
        }
        value = value.strip().lower()
        return ('hide_mode', mapping[value])

    def convert_testmode(self, value):
        mapping = {
            'interactive'    : paukenator.Lesson.INTERACTIVE,
            'multiplechoice' : paukenator.Lesson.MULTIPLE_CHOICE,
            'noninteractive' : paukenator.Lesson.NON_INTERACTIVE,
        }
        value = re.sub(r'[-_\s]',  '', value.strip().lower())
        return ('testmode', mapping[value])

    def convert_select(self, value):
        return ('selector', paukenator.Lesson.Selector(value))

    def convert_language(self, value):
        mapping = {
            'german'  : 'deu', 'deu' : 'deu', 'de' : 'deu',
            'english' : 'eng', 'eng' : 'eng', 'en' : 'eng'
        }
        value = value.lower()
        return ('lang', mapping.get(value, value))

    def convert_file(self, value):
        if not os.path.isfile(value):
            msg = (f"WARNING: File not found: '{value}'"
                   f" (specified in {self.filename})")
            print(msg, file=sys.stderr)
        return ('filepath', value)
