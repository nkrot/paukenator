import click

from paukenator import __version__
from paukenator import Config, Lesson, Text, Selector
from paukenator.exercises import HiddenWord
from paukenator.nlp import WBD, SBD


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


def choices_explained(source):
    res = ["{} ({})".format(item[0], item[1]) for item in source]
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

    wbd = WBD(lang=config.lang)
    sbd = SBD(lang=config.lang)

    for infile in config.filepath:
        # TODO: put initialization logic (factory) into a Teacher class?
        text = Text.load(infile, lang=config.lang)
        sbd.annotate(text)
        wbd.annotate(text)

        lesson = Lesson(text, config)
        lesson.run()

    return 0


if __name__ == '__main__':
    exit(main())
