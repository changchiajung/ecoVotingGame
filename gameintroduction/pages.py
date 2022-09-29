from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Subsession, Group, Player, Question
import csv
import random


class Introduction(Page):
    pass


class GeneralTest(Page):
    # form_model = 'player'
    # form_fields = ["score"]
    live_method = 'live_bid'

    def vars_for_template(self):
        question = Question.objects.filter(subsession=self.subsession,
                                           sequence=self.player.question_index)
        if question.count() > 0:
            image_link = Constants.image_base_link + question[0].image_link
            print(image_link)
        return dict(sequence=question[0].sequence, image_link=image_link)


def process_rank(self):
    player_information = {}
    # Iterate through the players to determine the rank of each player
    for p in self.group.get_players():
        player_information[p.id_in_group] = p.score
    current_rank = 1
    for k, v in reversed(sorted(player_information.items(), key=lambda item: item[1])):
        current_player = self.group.get_player_by_id(k)
        current_player.participant.vars["score"] = current_player.score
        current_player.participant.vars["rank"] = current_rank
        print("id: {} , rank: {} ".format(current_player.id_in_group, current_rank))
        current_rank += 1
    print()


def parse_question_from_file(self):
    f = open("questions.csv", "r")
    reader = csv.reader(f, delimiter=',', quotechar='|')
    question_list = []
    for row in reader:
        question_list.append(row)
    # print(len(question_list))
    random.shuffle(question_list)
    # print(question_list)
    self.subsession.total_question = len(question_list)
    for index, question in enumerate(question_list):
        Question.objects.create(subsession=self.subsession,
                                sequence=index + 1,  # start from 1
                                image_link=question[1],
                                correct_answer=question[2]
                                )


class IntroductionWaitPage(WaitPage):
    after_all_players_arrive = parse_question_from_file


class WaitForRankProcess(WaitPage):
    after_all_players_arrive = process_rank


page_sequence = [Introduction, IntroductionWaitPage, GeneralTest, WaitForRankProcess]
