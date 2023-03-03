from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class VotingPage(Page):
    # timeout_seconds = 60
    form_model = 'player'
    form_fields = ['choose']
    timer_text = '剩餘時間: '

    def get_timeout_seconds(player):
        if player.round_number <= Constants.num_rounds / 3:
            return 90
        else:
            return 60

    def vars_for_template(self):
        # rank = self.player.id_in_group
        rank = self.player.participant.vars["rank"]
        score = self.player.participant.vars["score"]
        self.player.origin_option = int(self.group.origin_division.split(",")[rank - 1])
        self.player.alternative_option = int(self.group.alternative_division.split(",")[rank - 1])
        return dict(origin_division=self.group.origin_division, alternative_division=self.group.alternative_division,
                    rank=rank, score=score, round_number=self.subsession.round_number,
                    round_number_progress=round(self.subsession.round_number / 24 * 100, 2))


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
    # Set equal situation as random
    if voting_origin > voting_alternative:
        self.group.major_result = True
    elif voting_alternative > voting_origin:
        self.group.major_result = False
    else:
        self.group.major_result = True if self.group.round_number % 2 == 0 else False

    if self.group.round_number == Constants.num_rounds:
        '''
        result_dict = {}
        for i in range(Constants.players_per_group + 1):
            result_dict[i] = []
        results = []
        for g in self.group.in_all_rounds():
            result_dict[g.voting_origin].append(g.origin_division)
            result_dict[g.voting_alternative].append(g.alternative_division)
        # print("{}: {}".format(self.group.id_in_subsession, result_dict))
        for i in range(Constants.players_per_group, -1, -1):
            if len(result_dict[i]) > 0:
                results = result_dict[i]
                break
        print("{}: {}".format(self.group.id_in_subsession, results))
        random_division = random.choice(results)
        self.group.final_division = random_division
        '''
        # Choose random winner from 24 division composition
        results = []
        for g in self.group.in_all_rounds():
            if g.major_result:
                results.append(g.origin_division)
            else:
                results.append(g.alternative_division)
        # print(results)
        random_division = random.choice(results)
        self.group.final_division = random_division


class VotingWaitingPage(WaitPage):
    title_text = "請耐心稍候其他受試者"
    body_text = "請靜待其他玩家的決定，完成後將會自動跳轉。"
    after_all_players_arrive = process_voting


class ResultPage(Page):
    # NEED MODIFICATION for group divide
    def vars_for_template(self):
        division = self.group.origin_division if self.group.major_result else self.group.alternative_division
        rank = self.player.participant.vars["rank"]
        return dict(voting_origin=self.group.voting_origin, voting_alternative=self.group.voting_alternative,
                    major_result=self.group.major_result, division=division, rank=rank)


class ResultWaitPage(WaitPage):
    title_text = "請耐心稍候其他受試者"
    body_text = "請靜待其他玩家的決定，完成後將會自動跳轉。"

    def is_displayed(self):
        return self.round_number != Constants.num_rounds


class FinalResultWaitPage(WaitPage):
    title_text = "請耐心稍候其他受試者"
    body_text = "請靜待其他玩家的決定，完成後將會自動跳轉。"

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    # wait_for_all_groups = True


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


class IntroductionPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class IntroductionWaitPage(WaitPage):
    title_text = "請耐心稍候其他受試者"
    body_text = "請靜待其他玩家的決定，完成後將會自動跳轉。"

    def is_displayed(self):
        return self.round_number == 1

    after_all_players_arrive = set_shuffle_options


class RegroupWaitPage(WaitPage):
    title_text = "請耐心稍候其他受試者"
    body_text = "請靜待其他玩家的決定，完成後將會自動跳轉。"

    def is_displayed(self):
        return self.round_number == 1

    wait_for_all_groups = True
    after_all_players_arrive = 'regroup_method'


class RegroupResultPage(Page):
    # timeout_seconds = 30
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
        return dict(division=division, rank=rank, participantFee=self.session.config["participation_fee"],
                    payment=self.participant.payoff,
                    finalPayment=self.session.config["participation_fee"] + self.participant.payoff)


class FirstQuestion(Page):
    def is_displayed(self):
        return self.round_number == 1


class VotingIntroduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class VotingIntroductionWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1


page_sequence = [RegroupWaitPage, RegroupResultPage, IntroductionPage, IntroductionWaitPage, FirstQuestion,
                 VotingIntroduction, VotingIntroductionWaitPage, VotingPage, VotingWaitingPage, ResultPage,
                 ResultWaitPage, FinalResultWaitPage, FinalResultPage]
