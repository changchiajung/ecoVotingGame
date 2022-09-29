from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
    ExtraModel,
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'gameintroduction'
    players_per_group = 5
    num_rounds = 1
    image_base_link = '/static/generalQuestion/'


class Subsession(BaseSubsession):
    total_question = models.IntegerField()


class Group(BaseGroup):
    pass


class Question(ExtraModel):
    subsession = models.Link(Subsession)
    sequence = models.IntegerField()
    image_link = models.StringField()
    correct_answer = models.StringField()


class Player(BasePlayer):
    score = models.IntegerField(initial=1)
    question_index = models.IntegerField(initial=1)

    def live_bid(self, bid):
        print('received a answer from', self.id_in_group, ':', bid)
        current_question = Question.objects.filter(subsession=self.subsession, sequence=self.question_index)[0]
        if current_question.correct_answer == bid:
            print("Correct Answer")
            self.score += 1
        else:
            print("Incorrect Answer")
        # Get Next Question
        if self.question_index < self.subsession.total_question:
            self.question_index += 1
            next_question = Question.objects.filter(subsession=self.subsession, sequence=self.question_index)
            if next_question.count() > 0:
                image_link = Constants.image_base_link + next_question[0].image_link
                return {self.id_in_group:image_link}
        else:
            return {self.id_in_group: "NULL"}

