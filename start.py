# after building the cards and rents and players components getting turns tested then I see this
# https://www.youtube.com/watch?v=ubQXz5RBBtU
# well I'm hoping

from cards_and_rents import *
from players import *

with Gameinfo() as game_info:

    p1 = Player(playername='John', game=game_info)
    p1.strategy = Generic_Strategy(game=game_info, player=p1)
    p2 = Player('Anna')
    p2.strategy = Generic_Strategy(game=game_info, player=p2)
    game_info.playerlist.append(p1)
    game_info.playerlist.append(p2)
    game_info.rounds_to_play = 10
    game_info.start_rounds()
