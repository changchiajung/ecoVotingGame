from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = "player"
    form_fields = ["desire_payment"]


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    def vars_for_template(self):
        self.participant.payoff = self.player.desire_payment
        return dict(
            payment=self.player.desire_payment
        )


page_sequence = [MyPage, ResultsWaitPage, Results]
