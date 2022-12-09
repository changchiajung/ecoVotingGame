from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from time import sleep


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield pages.RegroupResultPage
        random_choice = ['左邊','右邊']
        yield pages.VotingPage, dict(choose=random.choice(random_choice))
        yield pages.ResultPage
        if self.round_number == 30:
            yield pages.FinalResultPage

