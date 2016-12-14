from random import randint, choice
from cards_and_rents import *


class Player():
    def __init__(self, game, playername='john', percentage=100):
        self.money = 1500
        self.pos = 0
        self.playername = playername
        self.percentage = percentage
        self.game = game
        self.board = self.game.board
        self.owners = self.game.owners


    def __str__(self):
        return self.playername

    def __repr__(self):
        return self.playername

    def move(self):
        #print('player move')
        newpos = (self.pos + randint(2, 12)) % len(self.board)
        if newpos<self.pos: #passed go
            self.money += 200
        self.pos = newpos


    def buy(self, game_pos=(None,None), percentage_in_whole_numbers=25):
        """buy a property or house on the current position
        percentage_in_whole_numbers = 25(%)"""
        #print('player buy {}'.format(game_pos))
        if game_pos:
            game, pos = game_pos
        if pos is None:
            pos = self.pos
        if randint(1, 100) > percentage_in_whole_numbers:
            print('returning because this did not buy')
            return

        if game.owned_by(pos) == self:
            #build or revel in the fact that you own it
            if (self.board.type.loc[pos] == 'railroad' or self.board.type.loc[pos] =='utility'):
                #can't build on it
                pass
            else:
                if self.money >= self.game.house_cost and self.owners.houses.iloc[pos] < 6:
                    self.owners.houses.iloc[pos] += 1
                self.money -= self.game.house_cost
                return

        elif pd.isnull(game.owned_by(pos)):
            #buy it if you can
            if self.money > self.board.cost[pos]:
                self.money -= self.board.cost[pos]
                self.owners.owner.iloc[pos] = self
                return
            else:
                pass  # too expensive.

        else:
            #you don't own it
            #pay rent
            self.pay_rent()

    def sell(self, pos=None):
        print('selling {}'.format(pos))

        if pos is None:  # this is good for testing purposes
            pos = self.pos
        if self.board.iloc[pos]['houses'] > 0:

            self.money += self.game.house_cost
            self.board[pos]['houses'] -= 1
            return
        self.money += self.board[pos]['cost']
        self.owners.owner.iloc[pos] = None

    def _find_property_indexes(self):
        return list(self.owners[self.owners == self].index)

    def get_money_by_selling(self):
        """find a owned property on the board pick one randomly and sell it"""

        while (self.money < 0):
            idxlist = self._find_property_indexes()
            if idxlist == 0:
                self.loss = True
                return False
            idx = choice(idxlist)
            self.sell(idx)
        return True

    def pay_rent(self):
        #print('pay rent')
        owner = self.owners.iloc[self.pos]
        if owner is not None and owner is not self:
            rent = self.game.how_much_rent(self.pos)[1]

            self.money = self.money - rent
            if self.money < 0:
                while (True):
                    can_pay = self.get_money_by_selling()
                    if can_pay:
                        owner.money += rent
                        return True
                    else:
                        return False
        else:
            # you own it
            pass


if __name__ == '__main__':
    player1 = Player('Buy25Percent', 100)
    assert (player1.money == 1500)
    player1.buy(pos=0, percentage_in_whole_numbers=100)
    assert (player1.money == 1440)
    # print('cost is: {}'.format(board[0]['cost']))
    # print(house_cost)
    player1.buy(pos=0, percentage_in_whole_numbers=100)
    assert (player1.money == 1440 - 150)
    # print('player1 bought the house: {}'.format(player1.money))
    # print(board[0]['cost'])
    # player1.sell(0)
    # print(player1.money)
    player2 = Player('Buy85Percent', 100)
    player2.pay_rent()
    # print(player2.money)
    player1.buy(0)
    player1.buy(3)
    player1.buy(6)
    player1.buy(9)
    # print(owned_properties(player1))
