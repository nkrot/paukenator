import click

from paukenator import __version__
from paukenator import Config, Lesson, Text, Selector
from paukenator.exercises import HiddenWord
from paukenator import nlp


EPILOGUE = f"""\b
version: {__version__}
Have fun and keep learning!
"""


class SelectorSpec(click.ParamType):
    '''Validate value of --select option and convert it to type utils.Selector
    '''

    name = 'selector_spec'

    def convert(self, value, param, ctx):
        print(f"converting {param} to Selector")
        if isinstance(value, Selector):
            return value
        try:
            return Selector(value)
        except ValueError as ex:
            self.fail(str(ex), param, ctx)


def choices(source):
    '''Extract values to a list of choices.
    An examples of :source: is Lesson.PROMPTS
    '''
    res = [item[0] for item in source]
    return res


def choices_explained(source, indxs=(0,1)):
    ik, iv = indxs
    res = ["{} ({})".format(item[ik], item[iv]) for item in source]
    return ", ".join(res)


def get_lesson_config(files, **kwargs):
    '''Create c lesson configuration object from defaults and command line
    arguments'''
    # print("Files", files)
    # print("Args", kwargs)
    config = Config()
    config.filepath = files or config.filepath
    if kwargs.get('config_file', None):
        config.update_from_file(kwargs['config_file'])
    config.hide_ratio = kwargs.get('hide_ratio', None) or config.hide_ratio
    config.hide_mode = kwargs.get('hide_mode', None) or config.hide_mode
    config.testmode = kwargs.get('test_mode', None) or config.testmode
    config.selector = Selector(kwargs.get('select', None) or config.selector)

    return config


@click.group(invoke_without_command=True, epilog=EPILOGUE)
@click.option('--version', '-v', is_flag=True, help='Show version and exit.')
@click.pass_context
def main(ctx, version):
    """A tool that helps you practice a foreign language"""
    if version:
        click.echo(f"paukenator {__version__}")
    elif ctx.invoked_subcommand is None:
        click.echo("Try --help")


@main.command()
@click.argument('file', nargs=-1, type=click.Path(exists=True))
@click.option('--config', '-c', "config_file", type=click.Path(exists=True),
              help='read lesson configuration from the file.')
@click.option('--hide-ratio', type=float,
              help="(float) ratio of words to hide in each sentence.")
@click.option('--hide-partially', 'hide_mode',
              is_flag=True,  # TODO: is it really necessary?
              flag_value=HiddenWord.PARTIAL,
              show_default=True,
              help="""show the first and the last letter of the hidden words.
                      The exact behaviour depends on the word length.""")
@click.option('--select', '-s', metavar="SPEC", type=SelectorSpec(),
              help='practice with a set of sentences chosen by this'
                     ' selector. ex: --select 3..6')
@click.option('--test-mode',
              type=click.Choice(choices(Lesson.TEST_MODES),
                                case_sensitive=False),
              default=Lesson.DEFAULT_TEST_MODE, show_default=True,
              help="""Set study mode that defines how the user will interact
                   with the tool. Possible values are: {}.""".format(
                       choices_explained(Lesson.TEST_MODES)))
def study(file, **kwargs):
    """Study a text"""

    config = get_lesson_config(file, **kwargs)
    # print(config)

    for infile in config.filepath:
        text = Text.load_from_file(infile, config)
        lesson = Lesson(text, config)
        lesson.run()

    return 0


@main.command()
@click.argument('file', nargs=-1, type=click.Path(exists=True))
@click.option('--lang', '-l',
              type = click.Choice(choices(nlp.LANGUAGES)),
              default = nlp.DEFAULT_LANGUAGE, show_default = True,
              help="""Specify the language of the text. Possible values are:
              {}""".format(choices_explained(nlp.LANGUAGES, (0,2))))
@click.option('--words', '-w', "do_wbd", is_flag=True,
              help="""Perform word tokenization only skipping recognition of
              paragraphs and sentences. In this mode it is assumed that
              paragraphs are separated by at least one empty line and
              a line contains exactly one sentence.""")
@click.option('--debug', '-d', is_flag=True, help="be very verbose")
def tokenize(file, lang, do_wbd, debug):
    """Tokenize given plain text and recognize in it:\n
    \b
    - paragraphs;
    - sentences;
    - words and punctuation marks.

    The result will be text in which:\n
    \b
    - paragraphs are separated by an empty line;
    - one line contains one sentence only;
    - words and punctuation marks are separated by a space character.

    TODO: add an example
    """

    pa = nlp.ParagraphAnnotator(lang=lang, debug=debug)
    sa = nlp.SentenceAnnotator(lang=lang, debug=debug)
    wa = nlp.TokenAnnotator(lang=lang, debug=debug)

    if do_wbd:
        #pa is already using appropriate algorithm
        sa.one_per_line = True

    pipeline = [pa, wa, sa]

    for infile in file:
        text = nlp.Text.load_from_file(infile, lang=lang)
        for annotator in pipeline:
            annotator(text)
        print(text.tokenized())


if __name__ == '__main__':
    exit(main())
