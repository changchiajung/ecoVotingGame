import random

from otree.api import Currency as c, currency_range, Submission
from . import pages
from .models import Question
from ._builtin import Bot
from .models import Constants


# total_question = 1
# for question_index in range(total_question):
#     question = Question.objects.filter(subsession=self.subsession,
#                                        sequence=self.player.question_index,
#                                        group_number=self.player.group_number)
#     if question.count() > 0:
#         options = question[0].options
#         print(options)


def call_live_method(method, **kwargs):
    total_question = 30
    for question_index in range(total_question):
        for people in range(1, 6):
            method(people, random.choice("ABCD"))

class PlayerBot(Bot):
    def play_round(self):
        yield pages.Introduction
        yield Submission(pages.GeneralTest, check_html=False)
        yield pages.Results
