import sys
import argparse

from .. import version
from ..text import Text
from ..lesson import Lesson

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A tool that helps you learn the vocabulary of a text.",
        epilog=f"""
version: {version.__version__}
Have fun and keep learning!
""")
    parser.add_argument('files', nargs='+',
                        help='input file(s)')
    parser.add_argument('--hide-ratio', type=float, default=Lesson.HIDE_RATIO,
                        help="(float) ratio of words to hide in each sentence")
    parser.add_argument('--hide-partially', action='store_const', const='partial',
                        dest='hide_mode',
                        help="show initial and last letter of the hidden words."
                             "The exact behaviour depends on the word length.")

    parser.add_argument('--interactive', dest="interactive",
                        action='store_const', const=Lesson.INTERACTIVE,
                        help='request the user to type the answers')
    parser.add_argument('--multiple-choice', dest="interactive",
                        action='store_const', const=Lesson.MULTIPLE_CHOICE,
                        help='multiple-choice test (alternative to --interactive)')

    args = parser.parse_args()
    # print(args)
    return args

def main():
    args = parse_cmd_arguments()

    for infile in args.files:
        text = Text.load(infile, lang='deu')

        kwargs = {
            'hide_ratio'  : args.hide_ratio,
            'hide_mode'   : args.hide_mode,
            'interactive' : args.interactive
        }
        lesson = Lesson(text, **kwargs)
        lesson.run()

    return 0

if __name__ == '__main__':
    exit(main())
