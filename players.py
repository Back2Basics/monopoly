from random import randint, choice
from cards_and_rents import *
import sys
import numpy as np


class Generic_Strategy:
    def __init__(self, game=None, buy_percent=100, favor_groups=[]):
        self.buy_percent = buy_percent
        self.favor_groups = favor_groups
        self.game = game

    def should_i_buy(self, square=0):
        """buy a property or house on the current position
        percentage_in_whole_numbers = 25(%)"""


        if square is None:
            square = self.square
        if self.is_buyable(pos=square):
            if randint(1, 100) > self.buy_percent:
                print('returning because this did not buy or upgrade anything')
                return False

            # if (self.board.type.loc[square] == 'railroad' or self.board.type.loc[square] == 'utility'):

            elif self.board.houses.iloc[square] < 5 and self.board.owner.iloc[square] == self and \
                            self.board.type.iloc[square] == 'property':  # first test for ownership and house numbers
                if self.money >= self.game.house_cost and (self.board.houses.iloc[square] < 6):
                    self.board.houses.iloc[square] += 1
                self.money -= self.game.house_cost
                print('player {} bought a house # {} at {}'.format(self.playername, self.board.houses.iloc[square],
                                                                   self.board.name.iloc[square]))
                self.buying_houses_history[square] += 1
                self.board.houses.iloc[square] += 1
                return
            else:
                # you have an apartment on the property what else do you want
                pass

            # buy it if you can
            if self.money > self.board.cost[square]:
                self.money -= self.board.cost[square]
                self.board.owner.iloc[square] = self
                self.buying_property_history.add(square)
                print('player {} buys property {}'.format(self, self.board.name.iloc[square]))
                return
            else:
                pass  # too expensive.


class Player:
    def __init__(self, game=None, playername='John'):
        self.game = game
        self.money = 1500
        self.pos = 0
        self.playername = playername
        self.strategy = None
        self.active = True  # if the player is still in the game

        #statistics data
        self.buying_property_history = set()
        self.buying_houses_history = np.array([0] * 38)
        self.selling_history = set()
        self.selling_houses = np.array([0] * 38)
        self.paid_rent_on = []


    def __str__(self):
        return self.playername

    def __repr__(self):
        return self.playername

    def move(self):
        newpos = (self.pos + randint(2, 12)) % len(self.board)
        if newpos < self.pos:  # passed go
            self.money += 200
        self.pos = newpos

    def is_owned(self, pos):
        return pos in self.board[not pd.isnull(self.board.owner)].index

    def should_i_buy(self, square):
        return self.strategy.should_i_buy(square)


    def _find_property_indexes(self):
        return list(self.board[self.board.owner == self].index)

    def get_money_by_selling(self):
        """find a owned property on the board pick one randomly and sell it"""

        while (self.money < 0):
            idxlist = self._find_property_indexes()
            print('player {} owns {}'.format(self.playername, idxlist))
            if idxlist == []:
                self.loss = True
                self.active = False
                print('Player {} loses'.format(self.playername))
                return False
            idx = choice(idxlist)
            self.sell(idx)
        return True

    def sell(self, pos=None):
        if pos is None:  # this is good for testing purposes
            pos = self.pos
        if (self.board.houses.iloc[pos]) < 0:
            print("ERROR somewhere ERROR")

        elif (self.board.houses.iloc[pos]) > 0:
            print('{} selling house #{} at {}'.format(self, self.board.houses.iloc[pos], pos))
            self.money += self.game.house_cost
            self.board.houses.iloc[pos] -= 1
            if self.money > 0:
                return
            else:
                self.sell(pos)
                return
        print('{} selling property {}'.format(self, pos))
        self.money += self.board.cost.iloc[pos]
        self.board.owner.iloc[pos] = None


if __name__ == '__main__':
    with Gameinfo() as gi:
        gi.playerlist.append(Player(gi, 'John', 100))  # john buys 100 percent of the time
        gi.playerlist.append(Player(gi, 'Anna', 100))  # anna buys 100 percent of the time
        p1 = gi.playerlist[0]
        p2 = gi.playerlist[1]

        assert (p1.money == 1500)
        p1.buy((gi, 0), percentage_in_whole_numbers=100)
        assert (p1.money == 1440)
        # # print('cost is: {}'.format(board[0]['cost']))
        # # print(house_cost)
        # p1.buy((gi, 0), percentage_in_whole_numbers=100)
        # assert (p1.money == 1440 - 150)
        # # print('player1 bought the house: {}'.format(player1.money))
        # # print(board[0]['cost'])
        # # player1.sell(0)
        # # print(player1.money)
        # p2.pay_rent()
        # # print(player2.money)
        # p1.buy((gi, 0))
        # p1.buy((gi, 3))
        # p1.buy((gi, 6))
        # p1.buy((gi, 9))
        # # print(owned_properties(player1))
