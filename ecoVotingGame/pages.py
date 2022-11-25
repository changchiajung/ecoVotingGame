from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class VotingPage(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['choose']

    def vars_for_template(self):
        # rank = self.player.id_in_group
        rank = self.player.participant.vars["rank"]
        score = self.player.participant.vars["score"]
        return dict(origin_division=self.group.origin_division, alternative_division=self.group.alternative_division,
                    rank=rank, score=score)


def process_voting(self):
    # NEED MODIFICATION for group divide
    voting_origin = 0
    voting_alternative = 0
    for p in self.group.get_players():
        if p.choose == "左邊":
            voting_origin += 1
        elif p.choose == "右邊":
            voting_alternative += 1
    self.group.voting_origin = voting_origin
    self.group.voting_alternative = voting_alternative
    self.group.major_result = True if voting_origin > voting_alternative else False
    if self.group.round_number == Constants.num_rounds:
        results = []
        for g in self.group.in_all_rounds():
            if g.major_result:
                results.append(g.origin_division)
            else:
                results.append(g.alternative_division)
        random_division = random.choice(results)
        self.group.final_division = random_division


class VotingWaitingPage(WaitPage):
    after_all_players_arrive = process_voting


class ResultPage(Page):
    # NEED MODIFICATION for group divide
    def vars_for_template(self):
        division = self.group.origin_division if self.group.major_result else self.group.alternative_division
        rank = self.player.participant.vars["rank"]
        return dict(voting_origin=self.group.voting_origin, voting_alternative=self.group.voting_alternative,
                    major_result=self.group.major_result, division=division, rank=rank)


class ResultWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number != Constants.num_rounds


class FinalResultWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    wait_for_all_groups = True


def set_shuffle_options(self):
    # Shuffle for group division
    # Read all options from preset file
    f = open(Constants.file_name, "r")
    lines = f.readlines()
    random.shuffle(lines)
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


class RegroupWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1

    wait_for_all_groups = True
    after_all_players_arrive = 'regroup_method'

class RegroupResultPage(Page):
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        rank = self.player.participant.vars["rank"]
        score_in_group = []
        for p in self.group.get_players():
            score_in_group.append(p.participant.vars["score"])
        score_in_group = ", ".join([str(ele) for ele in sorted(score_in_group)])

        return dict(division=score_in_group, rank=rank, score=self.player.participant.vars["score"])


class FinalResultPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        '''
        Need
            Optimization
                        Here
        '''
        division = self.group.final_division
        rank = self.player.participant.vars["rank"]
        d_list = division.split(", ")
        payment = int(d_list[len(d_list) - rank])
        self.participant.payoff = payment
        return dict(division=division, rank=rank, payment=payment)


page_sequence = [RegroupWaitPage, RegroupResultPage, IntroductionWaitPage, VotingPage, VotingWaitingPage, ResultPage,
                 ResultWaitPage, FinalResultWaitPage, FinalResultPage]
