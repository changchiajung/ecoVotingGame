from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class GeneralTest(Page):
    form_model = 'player'
    form_fields = ["score"]

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
        current_rank +=1
    print()



class WaitForRankProcess(WaitPage):
    after_all_players_arrive = process_rank

page_sequence = [Introduction, GeneralTest, WaitForRankProcess]
