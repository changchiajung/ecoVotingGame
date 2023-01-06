from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ecoVotingGame'
    players_per_group = 5
    num_rounds = 24
    file_name = "divisions.txt"


class Subsession(BaseSubsession):

    def regroup_method(self):
        group_count = len(self.get_groups())
        new_dist = [[] for i in range(group_count)]
        for p in self.get_players():
            new_dist[(p.participant.vars["rank"] - 1) % group_count].append(p.id_in_subsession)
            # p.participant.payoff =((p.participant.vars["rank"] - 1) % group_count + 1) / 10.0
            p.participant.label = str((p.participant.vars["rank"] - 1) % group_count + 1)
            p.participant.vars["rank"] = (p.participant.vars["rank"] - 1) // group_count + 1
        print(new_dist)
        self.set_group_matrix(new_dist)
        for subsession in self.in_rounds(2, Constants.num_rounds):
            subsession.group_like_round(1)


class Group(BaseGroup):
    origin_division = models.StringField()
    alternative_division = models.StringField()
    voting_origin = models.IntegerField()
    voting_alternative = models.IntegerField()
    major_result = models.BooleanField()  # True: origin is majority ; False: alternative is majority
    final_division = models.StringField()


class Player(BasePlayer):
    choose = models.StringField(widget=widgets.RadioSelect, choices=['左邊', '右邊'], label="選擇")


def custom_export(players):
    all_group = Group.objects.all()

    attr_list = ["Session Code", "Group number", "Round number", "Division1", "Division2", "Player1", "Player2",
                 "Player3", "Player4",
                 "Player5", "Major(Final) Decision"]
    yield attr_list
    for group in all_group:
        # yield one more before first round
        if group.round_number == 1:
            player_list = [group.get_player_by_id(i).participant_id for i in range(1, 6)]
            yield [group.subsession.session.code, group.id_in_subsession, 0, "Record to look up participant number",
                   ""] + player_list + [""]
        player_list = [1 if group.get_player_by_id(i).choose == "左邊" else 2 for i in range(1, 6)]

        yield [group.subsession.session.code, group.id_in_subsession, group.round_number, group.origin_division,
               group.alternative_division] + player_list + [
                  group.origin_division if group.major_result else group.alternative_division]
        if group.round_number == Constants.num_rounds:
            player_list = [group.get_player_by_id(i).participant.payoff for i in range(1, 6)]
            yield [group.subsession.session.code, group.id_in_subsession, 0, "Payment and final division",
                   ""] + player_list + [
                      group.final_division]
