import sys
import argparse

from ..text import Text
from ..lesson import Lesson

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(
        description="TODO",
        epilog="Have fun"
    )
    parser.add_argument('files', nargs='+',
                        help='input file(s)')

    args = parser.parse_args()
    return args

def main():
    args = parse_cmd_arguments()

    for infile in args.files:
        text = Text.load(infile, lang='deu')
        lesson = Lesson(text)
        lesson.run()

    return 0

if __name__ == '__main__':
    exit(main())
