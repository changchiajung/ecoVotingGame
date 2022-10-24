from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from time import sleep


class PlayerBot(Bot):
    def play_round(self):
        random_choice = ['origin','alternative']
        yield pages.VotingPage, dict(choose=random.choice(random_choice))
        yield pages.ResultPage

