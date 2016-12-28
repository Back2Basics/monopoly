# after building the cards and rents and players components getting turns tested then I see this
# https://www.youtube.com/watch?v=ubQXz5RBBtU
# well I'm hoping
from cards_and_rents import *
from players import *

with Gameinfo() as g1:
    g1.playerlist.append(Player(g1, 'John', 100))  # john buys 100 percent of the time
    g1.playerlist.append(Player(g1, 'Anna', 100))  # anna buys 85 percent of the time
    p1 = g1.playerlist[0]
    p2 = g1.playerlist[1]
    g1.start()
