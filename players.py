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
        self.active = True  # if the player is still in the game

    def __str__(self):
        return self.playername

    def __repr__(self):
        return self.playername

    def move(self):
        # print('player move')
        newpos = (self.pos + randint(2, 12)) % len(self.board)
        if newpos < self.pos:  # passed go
            self.money += 200
        self.pos = newpos

    def buy(self, game_pos=(None, None), percentage_in_whole_numbers=25):
        """buy a property or house on the current position
        percentage_in_whole_numbers = 25(%)"""
        print('player buy {}'.format(game_pos[1]))
        if game_pos:
            game, pos = game_pos
        if pos is None:
            pos = self.pos
        if randint(1, 100) > percentage_in_whole_numbers:
            print('returning because this did not buy')
            return

        if game.owned_by(pos) == self:
            # build or revel in the fact that you own it
            if (self.board.type.loc[pos] == 'railroad' or self.board.type.loc[pos] == 'utility'):
                # can't build on it
                pass
            elif self.owners.houses.iloc[pos] < 5:
                if self.money >= self.game.house_cost and self.owners.houses.iloc[pos] < 6:
                    self.owners.houses.iloc[pos] += 1
                self.money -= self.game.house_cost
                return
            else:
                # you have an apartment on the property what else do you want
                pass

        elif pd.isnull(game.owned_by(pos)):
            # buy it if you can
            if self.money > self.board.cost[pos]:
                self.money -= self.board.cost[pos]
                self.owners.owner.iloc[pos] = self
                return
            else:
                pass  # too expensive.

        else:
            # you don't own it
            # pay rent
            self.pay_rent()

    def pay_rent(self):
        print('{} pay rent: {}'.format(self.playername, self.pos))
        owner = self.owners.owner.iloc[self.pos]
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
                        print('PLAYER LOSES: {}'.format(self))
                        self.active == False
                        return False
        else:
            # you own it
            pass

    def _find_property_indexes(self):
        return list(self.owners[self.owners.owner == self].index)

    def get_money_by_selling(self):
        """find a owned property on the board pick one randomly and sell it"""

        while (self.money < 0):
            idxlist = self._find_property_indexes()
            if idxlist == []:
                self.loss = True
                return False
            idx = choice(idxlist)
            self.sell(idx)
        return True

    def sell(self, pos=None):
        print('selling {}'.format(pos))

        if pos is None:  # this is good for testing purposes
            pos = self.pos
        if (self.owners.houses.iloc[pos]) > 0:

            self.money += self.game.house_cost
            self.owners.houses.iloc[pos] -= 1
            if self.money > 0:
                return
            else:
                self.sell(pos)
        self.money += self.board.cost.iloc[pos]
        self.owners.owner.iloc[pos] = None


if __name__ == '__main__':
    with Gameinfo() as gi:
        gi.playerlist.append(Player(gi, 'John', 100))  # john buys 100 percent of the time
        gi.playerlist.append(Player(gi, 'Anna', 100))  # anna buys 100 percent of the time
        p1 = gi.playerlist[0]
        p2 = gi.playerlist[1]

        assert (p1.money == 1500)
        p1.buy((gi, 0), percentage_in_whole_numbers=100)
        assert (p1.money == 1440)
        # print('cost is: {}'.format(board[0]['cost']))
        # print(house_cost)
        p1.buy((gi, 0), percentage_in_whole_numbers=100)
        assert (p1.money == 1440 - 150)
        # print('player1 bought the house: {}'.format(player1.money))
        # print(board[0]['cost'])
        # player1.sell(0)
        # print(player1.money)
        p2.pay_rent()
        # print(player2.money)
        p1.buy((gi, 0))
        p1.buy((gi, 3))
        p1.buy((gi, 6))
        p1.buy((gi, 9))
        # print(owned_properties(player1))
