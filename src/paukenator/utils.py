import os
from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "templates")


def load_template(fname):
    return Environment(loader=FileSystemLoader(TEMPLATES_DIR),
                       trim_blocks=True).get_template(fname)
