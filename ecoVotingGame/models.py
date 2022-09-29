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
    final_division = models.StringField()


class Group(BaseGroup):
    origin_division = models.StringField()
    alternative_division = models.StringField()
    voting_origin = models.IntegerField()
    voting_alternative = models.IntegerField()
    major_result = models.BooleanField() # True: origin is majority ; False: alternative is majority


class Player(BasePlayer):
    choose = models.StringField(widget=widgets.RadioSelect, choices=['origin','alternative'], label="選擇")
