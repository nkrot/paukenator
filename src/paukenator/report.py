from datetime import datetime
from collections import defaultdict
from typing import Tuple

from paukenator.utils import load_template
from paukenator.prompts.challenges import Challenge


class Report(object):

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.exercise_type = "Unknown"
        self.answer_mode = "Unknown"
        self.answers_expected = False
        self.text = None
        self.counts = defaultdict(int)
        self.template = load_template("report.en.txt.j2")
        self.incorrect_answers = []

    def start(self) -> None:
        """Start tracking time"""
        self.start_time = datetime.now()

    def finish(self) -> None:
        """End tracking time"""
        self.end_time = datetime.now()

    def __str__(self) -> str:
        """Generate a report from collected values based on the template.
        Return a string.
        """

        values = {
            'start_time'    : self.to_datestr(self.start_time),
            'end_time'      : self.to_datestr(self.end_time),
            'exercise_type' : self.exercise_type,
            'answer_mode'   : self.answer_mode,
            'text_filename' : self.text.filename,
            'text_num_sentences' : len(self.text.sentences),
            'num_studied_sentences' : self.counts['studied sentences'],
            'num_asked_questions'   : self.counts['asked questions'],
            'num_answered_questions' : self.counts['answered_questions'],
            # 'num_skipped_questions'   : self.counts['skipped_questions'],
            'num_answered_correctly' :
                self.counts['correctly_answered_questions'],
            'num_answered_correctly_1st_attempt' :
                self.counts['correctly_answered_questions_1st_atempt'],
            'num_answered_incorrectly' :
                self.counts['incorrectly_answered_questions'],
        }

        # duration of the lesson
        values['hours'], values['minutes'], values['seconds'] = \
            self.to_hms((self.end_time - self.start_time).total_seconds())

        values['show_answers'] = self.answers_expected

        if self.counts['answered_questions'] > 0:
            values['pct_answered_correctly'] = round(
                100 * self.counts['correctly_answered_questions']
                / self.counts['answered_questions'], 2)
            values['pct_answered_incorrectly'] = round(
                100 * self.counts['incorrectly_answered_questions']
                / self.counts['answered_questions'], 2)

        values['mistakes'] = self.incorrect_answers

        return self.template.render(values)

    def to_hms(self, seconds: int) -> Tuple[int, int, int]:
        """
        Convert given number of seconds to the number of hours, minutes and
        seconds.

        Return
        a tuple of ints (hours, minutes, seconds)
        """
        hours = int(int(seconds) / 60 / 60)
        seconds = seconds - (hours * 60 * 60)
        minutes = int(seconds / 60)
        seconds = int(seconds - (minutes * 60))
        return (hours, minutes, seconds)

    def to_datestr(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")

    def incr_studied_sentences(self, val: int = 1) -> None:
        """
        Increase the count of studied sentences by given number (default 1)
        """
        self.counts['studied sentences'] += val

    def incr_asked_questions(self, val: int = 1) -> None:
        """
        Increase the count of asked questions by given number (default 1)
        """
        self.counts['asked questions'] += val

    def incr_correctly_answered_questions(self, val: int = 1) -> None:
        self.counts['answered_questions'] += val
        self.counts['correctly_answered_questions'] += val

    def incr_correctly_answered_questions_1st_attempt(
            self, val: int = 1) -> None:
        self.counts['correctly_answered_questions_1st_atempt'] += val

    def incr_incorrectly_answered_questions(self, val: int = 1) -> None:
        self.counts['answered_questions'] += val
        self.counts['incorrectly_answered_questions'] += val

    def add_incorrect_answer(self, challenge: Challenge) -> None:
        user_answer = ", ".join([str(ans) for ans in challenge.user_answers_])
        mistake = (challenge.correct_answer_, user_answer)
        self.incorrect_answers.append(mistake)
