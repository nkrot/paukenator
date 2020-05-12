import sys
import argparse

from paukenator import version
from paukenator import HiddenWord, Lesson, Text
from paukenator.nlp import WordTokenizer

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
    parser.add_argument('--hide-partially', dest='hide_mode',
                        action='store_const', const=HiddenWord.PARTIAL,
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
    lang = 'deu'

    tokenizer = WordTokenizer(lang=lang)

    for infile in args.files:
        # TODO: put initialization logic (factory) into a Teacher class?
        text = Text.load(infile, lang=lang)
        text = tokenizer.process(text)

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
