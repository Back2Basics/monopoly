from random import randint, choice
from cards_and_rents import Gameinfo
import numpy as np


class Generic_Strategy:
    def __init__(self, game=None, player=None, buy_percent=100, favor_groups=[]):
        self.buy_percent = buy_percent
        self.favor_groups = favor_groups
        self.game = game
        self.player = player

    def get_money(self):
        """You might be at a loss in the middle of a game.  So you can sell property,
        sell houses, or mortgage a property.  How you want to do that can be specified here.
        """
        return self.player.get_money_by_selling()

    def house_buying_strategy(self, square):  # just a lame one to start out with
        house_bought = []
        if self.player.money < self.game.house_cost:
            return False
        for x in range(5):
            if randint(0, 100) < 95:
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
            # should you buy if the strategy probablilities say no
            if randint(1, 100) > self.buy_percent:
                print('returning because this did not buy or upgrade anything')
                return False
            return True

            # if (self.board.type.loc[square] == 'railroad' or self.board.type.loc[square] == 'utility'):


class Player:
    def __init__(self, game=None, playername='John'):
        self.game = game
        initial_player_money = 1500
        self.money = initial_player_money
        self.game.bank_money -= initial_player_money
        self._properties_owned = set()
        self.current_position = 0
        self.playername = playername
        self.strategy = None
        self.active = True  # if the player is still in the game

        # statistics data
        self.buying_property_history = set()
        self.buying_houses_history = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int8)
        self.selling_history = set()
        self.selling_houses = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int8)
        self.paid_rent_on = []

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        if value >= 0:
            self._money = value
        else:
            self.strategy.get_money()
            self._money = value

    def __str__(self):
        return self.playername

    def __repr__(self):
        return self.playername

    def move(self):
        newpos = (self.current_position + randint(1, 6) + randint(1, 6)) % len(self.game.board)
        if newpos < self.current_position:  # passed go
            self.money += 200
        self.current_position = newpos



    def is_owned(self, square):
        return square in self.game.board[not pd.isnull(self.game.board.owner)].index

    def should_i_sell_a_house(money_to_gain = None):
        pass

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
            # print('player {} owns {}'.format(self.playername, idxlist))
            if idxlist == []:
                self.loss = True
                self.active = False
                print('Player {} loses'.format(self.playername))
                return False
            idx = choice(idxlist)
            self.sell(idx)
        return True

    def sell(self, square=None):
        if square is None:  # this is good for testing purposes
            square = self.current_position
        if (self.game.board.houses.iloc[square]) < 0:
            print("ERROR somewhere ERROR")

        elif (self.game.board.houses.iloc[square]) > 0:
            # print('{} selling house #{} at {}'.format(self, self.game.board.houses.iloc[pos], pos))
            self.money += self.game.house_cost
            self.game.board.houses.iloc[square] -= 1
            if self.money > 0:
                return
            else:
                self.sell(square)
                return
        # print('{} selling property {}'.format(self, pos))
        self.money += self.game.board.cost.iloc[square]
        self.game.board.owner.iloc[square] = None

    def house_buying_strategy(self, square):
        return self.strategy.house_buying_strategy(square)
