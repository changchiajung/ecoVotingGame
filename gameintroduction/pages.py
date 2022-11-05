from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Subsession, Group, Player, Question
import csv
import random


class Introduction(Page):
    pass


class GeneralTest(Page):
    timeout_seconds = 600
    live_method = 'live_bid'

    def vars_for_template(self):
        question = Question.objects.filter(subsession=self.subsession,
                                           sequence=self.player.question_index,
                                           group_number=self.player.group_number)
        if question.count() > 0:
            image_link = Constants.image_base_link + question[0].image_link
            # print(image_link)
            return dict(sequence=question[0].sequence, image_link=image_link, options=question[0].options,
                        progress=round(question[0].sequence / self.subsession.total_question * 100),
                        score=self.player.score, total_score=question[0].sequence)
        else:
            image_link = Constants.image_base_link + "end.png"
            return dict(sequence=-1, image_link=image_link, options="",
                        progress=100, score=self.player.score, total_score=self.subsession.total_question + 1)


def process_rank(self):
    # NEED MODIFICATION for group divide
    # Have to compute rank in each subGroup separately
    all_group_information = {}
    for group_number in range(1, 1 + self.subsession.total_group):
        all_group_information[group_number] = {}
    # Iterate through the players to determine the rank of each player
    for p in self.group.get_players():
        all_group_information[p.group_number][p.id_in_group] = p.score
    for group_number in range(1, 1 + self.subsession.total_group):
        current_rank = 1
        for k, v in reversed(sorted(all_group_information[p.group_number].items(), key=lambda item: item[1])):
            current_player = self.group.get_player_by_id(k)
            current_player.participant.vars["score"] = current_player.score
            current_player.participant.vars["rank"] = current_rank
            print("Group : {} id: {} , rank: {} ".format(group_number, current_player.id_in_group, current_rank))
            current_rank += 1


def parse_question_from_file(self):
    f = open("questions.csv", "r")
    reader = csv.reader(f, delimiter=',', quotechar='|')
    question_list = []
    for row in reader:
        question_list.append(row)
    self.subsession.total_question = len(question_list)
    # print(len(question_list))
    # Have to repeat self.subsession.total_group times, for each subGroup
    for i in range(self.subsession.total_group):
        random.shuffle(question_list)
        for index, question in enumerate(question_list):
            Question.objects.create(subsession=self.subsession,
                                    sequence=index + 1,  # start from 1
                                    image_link=question[0],
                                    correct_answer=question[1],
                                    options=question[2],
                                    group_number=i + 1
                                    )


class IntroductionWaitPage(WaitPage):
    after_all_players_arrive = parse_question_from_file


class WaitForRankProcess(WaitPage):
    after_all_players_arrive = process_rank


class Results(Page):
    def vars_for_template(self):
        return dict(score=self.participant.vars["score"], rank=self.participant.vars["rank"])


page_sequence = [Introduction, IntroductionWaitPage, GeneralTest, WaitForRankProcess, Results]
