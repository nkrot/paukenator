import argparse

from paukenator import __version__
from paukenator import Config, HiddenWord, Lesson, Text
from paukenator.nlp import WBD, SBD


def parse_cmd_arguments(config):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A tool that helps you learn the vocabulary of a text.",
        epilog=f"""
version: {__version__}
Have fun and keep learning!
""")
    parser.add_argument('files', nargs='*',
                        help='input file(s)')
    parser.add_argument('-c', '--config', type=argparse.FileType('r'),
                        help='read configuration from the file')

    parser.add_argument('--hide-ratio', type=float,
                        help="(float) ratio of words to hide in each sentence")
    parser.add_argument('--hide-partially', dest='hide_mode',
                        action='store_const', const=HiddenWord.PARTIAL,
                        help="show the first and the last letter of the hidden"
                             " words. The exact behaviour depends on the word"
                             " length.")

    # According to argparse documentation/issue tracker, such a nesting is not
    # a valid usage. I do not care. It looks like argparse has stalled in
    # development long ago.
    testmode = parser.add_argument_group(
        'MODE OF EXERCISING',
        '''\
The following options control how the user will interact with the tool.
If no option was specified, the user will not need to input any answers.
Otherwise s/he will be requested to type an answer, the exact form of
which depends on the option.''')
    mutex = testmode.add_mutually_exclusive_group()
    mutex.add_argument('--interactive', dest="testmode",
                        action='store_const', const=Lesson.INTERACTIVE,
                        help='the user will be prompted to type in answers.')
    mutex.add_argument('--multiple-choice', dest="testmode",
                        action='store_const', const=Lesson.MULTIPLE_CHOICE,
                        help='the user will be prompted to select one answer'
                             ' from given set of answers.')

    parser.add_argument('--select', type=Lesson.Selector,
                        metavar="SELECTOR_SPEC",
                        help='select sentences for practice specified by this'
                              ' selector. ex: --select 3..6')

    args = parser.parse_args()
    # print(args)

    if args.config:
        config.update_from_file(args.config)

    # update config object from command line arguments
    config.hide_ratio = args.hide_ratio
    config.hide_mode  = args.hide_mode
    config.testmode   = args.testmode
    config.selector   = args.select
    # print(config)

    # Set working files from configuration file
    # TODO: perhaps for uniformity with other parameters, we should rather use
    # config object to store working files too (and not args.files). For this
    # to be possible, confile.filepath should support a list of items
    if not args.files and config.filepath:
        args.files.append(config.filepath)

    return args


def main():
    config = Config()
    args = parse_cmd_arguments(config)

    wbd = WBD(lang=config.lang)
    sbd = SBD(lang=config.lang)

    for infile in args.files:
        # TODO: put initialization logic (factory) into a Teacher class?
        text = Text.load(infile, lang=config.lang)
        sbd.annotate(text)
        wbd.annotate(text)

        lesson = Lesson(text, config)
        lesson.run()

    return 0


if __name__ == '__main__':
    exit(main())
