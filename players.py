from random import randint, choice
from cards_and_rents import *
import numpy as np


class Generic_Strategy:
    def __init__(self, game=None, player= None, buy_percent=100, favor_groups=[]):
        self.buy_percent = buy_percent
        self.favor_groups = favor_groups
        self.game = game
        self.player = player

    def house_buying_strategy(self, square): # just a lame one to start out with
        house_bought = []
        for x in range(5):
            if randint(0,100)<75:
                house_bought.append(self.should_i_buy_house(square))
            else:
                pass
        return any(house_bought)

    def should_i_buy_house(self, square=0):
        if self.game.is_house_buyable(self.player, square):
            if self.player.money >= self.game.house_cost:
                return True
        return False


    def should_i_buy_square(self, square=0):
        """buy a property or house on the current position
        percentage_in_whole_numbers = 25(%)"""
        if square is None:
            square = self.square
        if self.game.is_buyable(square):
            #should you buy if the strategy probablilities say no
            if randint(1, 100) > self.buy_percent:
                print('returning because this did not buy or upgrade anything')
                return False
            return True

            # if (self.board.type.loc[square] == 'railroad' or self.board.type.loc[square] == 'utility'):



class Player:
    def __init__(self, game=None, playername='John'):
        self.game = game
        self.money = 1500
        self.current_position = 0
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
        newpos = (self.current_position + randint(2, 12)) % 38
        if newpos < self.current_position:  # passed go
            self.money += 200
        self.current_position = newpos

    def is_owned(self, pos):
        return pos in self.game.board[not pd.isnull(self.game.board.owner)].index

    def should_i_buy_house(self, square):
        return self.strategy.should_i_buy_house(square)

    def should_i_buy_square(self, square):
        return self.strategy.should_i_buy_square(square)

    def _find_property_indexes(self):
        return list(self.game.board[self.game.board.owner == self].index)

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
            pos = self.current_position
        if (self.game.board.houses.iloc[pos]) < 0:
            print("ERROR somewhere ERROR")

        elif (self.game.board.houses.iloc[pos]) > 0:
            print('{} selling house #{} at {}'.format(self, self.game.board.houses.iloc[pos], pos))
            self.money += self.game.house_cost
            self.game.board.houses.iloc[pos] -= 1
            if self.money > 0:
                return
            else:
                self.sell(pos)
                return
        print('{} selling property {}'.format(self, pos))
        self.money += self.game.board.cost.iloc[pos]
        self.game.board.owner.iloc[pos] = None

    def house_buying_strategy(self, square):
        return self.strategy.house_buying_strategy(square)

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
