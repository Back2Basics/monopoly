# after building the cards and rents and players components getting turns tested then I see this
# https://www.youtube.com/watch?v=ubQXz5RBBtU
# well I'm hoping

from cards_and_rents import *
from players import *
import numpy as np

with Gameinfo() as game_info:
    game_info.playerlist.append(Player(game_info, 'John_100_percent', 100))  # john buys 100 percent of the time
    game_info.playerlist.append(Player(game_info, 'Anna_85_percent', 85))  # anna buys 85 percent of the time
    game_info.playerlist.append(Player(game_info, 'Ian_65_percent', 65))  # anna buys 85 percent of the time
    p1 = game_info.playerlist[0]
    p2 = game_info.playerlist[1]
    game_info.rounds_to_play = 10
    game_info.start_rounds()
