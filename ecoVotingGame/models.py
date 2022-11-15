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
            p.participant.vars["rank"] = (p.participant.vars["rank"]-1)//group_count + 1
        print(new_dist)
        self.set_group_matrix(new_dist)
        for subsession in self.in_rounds(2, Constants.num_rounds):
            subsession.group_like_round(1)


class Group(BaseGroup):
    origin_division = models.StringField()
    alternative_division = models.StringField()
    voting_origin = models.IntegerField()
    voting_alternative = models.IntegerField()
    major_result = models.BooleanField() # True: origin is majority ; False: alternative is majority
    final_division = models.StringField()


class Player(BasePlayer):
    choose = models.StringField(widget=widgets.RadioSelect, choices=['origin','alternative'], label="選擇")
