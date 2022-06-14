from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class VotingPage(Page):
    form_model = 'player'
    form_fields = ['choose']

    def vars_for_template(self):
        ## FOR DEVELOP, set rank of player as id in round
        rank = self.player.id_in_group
        return dict(origin_division=self.group.origin_division, alternative_division=self.group.alternative_division,
                    rank=rank)


class VotingWaitingPage(WaitPage):
    pass


class ResultPage(Page):
    pass


class ResultWaitPage(WaitPage):
    pass


def set_shuffle_options(self):
    # Read all options from preset file
    f = open(Constants.file_name, "r")
    lines = f.readlines()
    group = self.group

    for index, g in enumerate(group.in_rounds(1, Constants.num_rounds)):
        origin_division = lines[index].split("\n")[0][1:-1].split("], [")[0]
        alternative_division = lines[index].split("\n")[0][1:-1].split("], [")[1]
        g.origin_division = origin_division
        g.alternative_division = alternative_division


class IntroductionWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1

    after_all_players_arrive = set_shuffle_options


page_sequence = [IntroductionWaitPage, VotingPage, VotingWaitingPage, ResultPage, ResultWaitPage]
