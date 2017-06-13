# after building the cards and rents and players components getting turns tested then I see this
# https://www.youtube.com/watch?v=ubQXz5RBBtU
# well I'm hoping

from cards_and_rents import *
from players import *

with Gameinfo() as gi:
    p1 = Player(playername='John', game=gi)
    p1.strategy = Generic_Strategy(game=gi, player=p1)
    p2 = Player(playername='Anna', game=gi)
    p2.strategy = Generic_Strategy(game=gi, player=p2)
    gi.playerlist.append(p1)
    gi.playerlist.append(p2)
    gi.rounds_to_play = 10
    gi.start_rounds()
