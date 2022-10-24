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
    total_group = models.IntegerField()

    def creating_session(self):
        number_of_group = 1
        number_of_player = 0
        for player in self.get_players():
            player.group_number = number_of_group
            number_of_player += 1
            if number_of_player == Constants.players_per_group:
                number_of_group += 1
                number_of_player = 0
        # Since the number_of_group would be n + 1 when players are 5n
        self.total_group = number_of_group - 1


class Group(BaseGroup):
    pass


class Question(ExtraModel):
    subsession = models.Link(Subsession)
    sequence = models.IntegerField()
    image_link = models.StringField()
    correct_answer = models.StringField()
    options = models.StringField()
    group_number = models.IntegerField()


class Player(BasePlayer):
    score = models.IntegerField(initial=0)
    question_index = models.IntegerField(initial=1)
    group_number = models.IntegerField()

    def live_bid(self, bid):
        print('received a answer from', self.id_in_group, ':', bid)
        current_question = Question.objects.filter(subsession=self.subsession, sequence=self.question_index,
                                                   group_number=self.group_number)[0]
        if current_question.correct_answer == bid:
            print("Correct Answer")
            self.score += 1
        else:
            print("Incorrect Answer")
        # Get Next Question
        if self.question_index <= self.subsession.total_question:
            self.question_index += 1
            print("index : {}".format(self.question_index))
            next_question = Question.objects.filter(subsession=self.subsession, sequence=self.question_index,
                                                    group_number=self.group_number)
            if next_question.count() > 0:
                image_link = Constants.image_base_link + next_question[0].image_link
                return {
                    self.id_in_group: {"image_link": image_link, "options": next_question[0].options, "progress": round(
                        next_question[0].sequence / self.subsession.total_question * 100), "score": self.score,
                                       "total_score": next_question[0].sequence}}
            else:
                self.question_index = self.subsession.total_question + 1
                return {self.id_in_group: {"image_link": "NULL", "options": "", "progress": 100, "score": self.score,
                                           "total_score": self.subsession.total_question + 1}}
