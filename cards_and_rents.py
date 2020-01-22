import logging
from copy import deepcopy
from datetime import datetime as dt
from pathlib import Path
from random import randint

import numpy as np
import pandas as pd

from exceptions import BrokeBankError

log = logging.getLogger('SEC')


class Gameinfo:
    max_houses = 4

    # TODO: ADD PLAYERS TO THE GAME
    def __init__(self, player_count=2, rounds=1):
        self.bank_money = 15140
        self.rounds_to_play = rounds

        self.timeout = False

        # set up board
        self.board = pd.read_json(Path('board.json').read_text())
        self.board.index.name = 'square'
        self.board.sort_index(inplace=True)
        self.board.index = self.board.index.map(np.int8)

        self.starting_playerlist = []
        self.house_cost = 150
        self.board.houses = 0

        self.owners = self.board.owner.tolist()
        self.houses = self.board.houses.tolist()

    def reset_game_with_same_players(self):
        self.players_still_in_game = deepcopy(self.starting_playerlist)
        self.bank_money = 15140
        self.owners = self.board.owner.tolist()
        self.houses = self.board.houses.tolist()

    @property
    def bank_money(self):
        return self._bank_money

    @bank_money.setter
    def bank_money(self, value):
        if value >= 0:
            self._bank_money = value
        else:
            raise BrokeBankError

    def owned_by(self, square=0):
        return self.owners[square]

    def get_all_owned_by(self, player):
        return [c for c, x in enumerate(self.owners) if x == player]

    def is_buyable(self, player, square):
        """can you buy the place?"""
        return (self.owners[square] == None) and (player.money >= self.board.cost.iloc[square])

    def is_property(self, square):
        return self.board.type[square] == 'property'

    def is_house_buyable(self, player, square):
        """assumes you are asking about squares you own"""
        return (self.houses[square] <= self.max_houses) and (player == self.owners[square]) and (
                player.money >= self.house_cost)

    def buy_property(self, player, square):
        if self.is_buyable(player, square) and player.strategy.should_i_buy_property(player=player, square=square):
            print(f'player: {player} is buying {self.board.name.iloc[square]}')
            cost = self.board.cost.iloc[square]
            player.money -= cost
            self.bank_money += cost
            self.owners[square] = player
            player.buying_property_history.add(square)
            return True
        return False

    def buy_house(self, player, square):
        """ mutates state, buying a house"""
        if self.is_house_buyable(player, square) and player.should_i_buy_house(square):
            self.houses[square] += 1
            player.money -= self.house_cost
            self.bank_money += self.house_cost
            player.buying_houses_history[square] += 1
            return True
        return False

    def whom_do_i_pay_rent(self, square):
        return self.owned_by(square)

    def check_money(self, player, rent):
        """does the player have money to pay"""
        if player.money > rent:
            return True
        else:
            return False

    def pay_rent(self, square, player):
        owner, rent = self.how_much_rent(square, player)
        # print('{} pay {} rent on {}'.format(player, rent, player.current_position))
        # print('before player: {} has {}'.format(player, player.money))
        if self.check_money(player, rent):
            if owner == 'gov':  # don't act on this extra money
                pass
            else:
                owner.money += rent
                player.money -= rent
                # print('owner was {} \n has {} \nplayer: {}\n has {}\n   rent was {}'.format(owner, owner.money, player, player.money, rent))
                return True

        else:
            print(player.money, rent)

            if player.money < 0:
                while (True):
                    can_pay = player.get_money_by_selling()
                    print('can pay was reached by player {} with money = {}'.format(player, player.money))
                    if can_pay:
                        try:
                            owner.money += rent
                            # print('after player: {} has {}'.format(player, player.money))

                        except TypeError as e:
                            print(owner.money)
                            print(rent)
                            print('error was {}'.format(e))
                            sys.exit()
                        return True
                    else:
                        player.active = False
                        return False

    def utility_rent(self):
        if len(set([self.owned_by(12), self.owned_by(28)])) == 2:
            return (randint(2, 12) * 4)
        else:
            return (randint(2, 12) * 10)

    def how_much_rent(self, square, player=None):  # n is board index
        """Paying Rent
        When you land on a property that is owned by another player,
        the owner collects rent from you in accordance with the list
        printed on its Title Deed card. If the property is mortgaged,
        no rent can be collected. When a property is mortgaged, its
        Title Deed card is placed face down in front of the owner.
        It is an advantage to hold all the Title Deed cards in a color-group
        (i.e., Boardwalk and Park Place, or Connecticut, Vermont and Oriental Avenues)
        because the owner may then charge double rent for
        unimproved properties in that color-group. This rule
        applies to unmortgaged properties even if another property
        in that color-group is mortgaged.
        It is even more advantageous to have houses or hotels
        on properties because rents are much higher than for
        unimproved properties. The owner may not collect the
        rent if they fail to ask for it before the second player following throws the dice.
        :return How_much, to_whom
        """
        # if nobody owns the square we wouldn't have gotten here (see turn())
        # if owned by the player we wouldn't have gotten here (see turn())
        #if someone else owns the square
        if self.owned_by(square) != player and self.owned_by(square) != 'gov' :
            #do they own all squares of that color and are unimproved?
            # TODO: put that here
            return self.owned_by(square), self.board.rent.iloc[square]

        owner = self.owned_by(square)
        if self.board.type.iloc[square] == 'gov':
            if square == 4:  # landed on Income Tax
                tax = max(int(player.money * 0.10), 200)  # greater of 200 or 10%
                return 'gov', tax
            return 'gov', 0

        # railroads and utilities have to come first because they don't have a color
        elif self.board.type[square] == 'railroad':
            # add players Railroad cards
            owns_rr = self.board.owner[self.board.type == 'railroad']
            how_many_rr_does_player_own = (owns_rr == owner).sum()

            return owner, list(self.board.rent[square])[how_many_rr_does_player_own - 1]

        elif self.board.type[square] == 'utility':
            return owner, self.utility_rent()
        elif owner != player and \
                len(set(
                    self.board.owner[self.board[self.board.color == self.board.color[
                        square]].index])) == 1:  # player owns all of a color
            return owner, self.board.rent[square][self.board.houses.iloc[square]] * 2
        else:  # properties
            try:
                rent_payment = self.board.rent.iloc[square][self.board.houses.iloc[square]]
            except BaseException:
                print('there was an error')
                print('square: {}'.format(square))
                print('self.board.rent.iloc[square]: {}'.format(self.board.rent.iloc[square]))
                print('self.board.name.iloc[square]: {}'.format(self.board.name.iloc[square]))
                print('self.board.houses.iloc[square]: {}'.format(self.board.houses.iloc[square]))
                print('self.board.iloc[square]: {}'.format(self.board.iloc[square]))
            return owner, rent_payment

    def display_second_stats(self):
        for player in self.playerlist:
            print(player.playername, player.current_position, int(player.money), player.active)

    def display_player_stats(self):
        pass
        # for player in self.playerlist:
        #     print(player.playername, player.current_position, int(player.money), player.active)

        # print(self.board.owner)

    def chance(self):
        # TODO: fix chance()
        pass

    def community_chest(self):
        # TODO: fix community chest in Game_info.turn
        pass

    def turn(self, player):
        print('player {} has {}'.format(player, player.money))
        player.move()
        if player.current_position in (7, 22, 36):  # chance squares
            self.chance()
            return
        elif player.current_position in (2, 17, 33):
            self.community_chest()
            return
        elif self.owned_by(player.current_position) == 'gov':
            return
            # TODO: fix the gov utilities and jail and free parking etc...
        elif self.owned_by(player.current_position) is None:
            is_recently_bought = self.buy_property(player, player.current_position)
            if is_recently_bought:
                return
        elif self.owned_by(player.current_position) == player:
            is_house_bought = self.buy_house(player.current_position)
            if is_house_bought:
                return
        else:
            self.pay_rent(square=player.current_position, player=player)

        self.display_player_stats()

    def collect_stats(self):
        pass
        # for player in self.playerlist:
        #     if player.active: #the winner
        #         self.buying_property_history  #set()
        #         self.buying_houses_history # np.array([0]*38)
        #         self.selling_history = # set()
        #         self.selling_houses = # np.array([0]*38)
        #         self.paid_rent_on # []
        #         self.money # 1500

    def start_rounds(self):
        self.players_still_in_game = deepcopy(self.starting_playerlist)

        for game_number in range(self.rounds_to_play):
            self.start_game()
            # game finishes here
            self.collect_stats()
            self.reset_game_with_same_players()

    def start_game(self):

        self.starttime = dt.now()
        # self.force_game_over = self.starttime.shift(seconds=10)

        self.loop_forever()
        print('Player {} Wins'.format([x for x in self.playerlist if x.active]))

    def loop_forever(self):
        """ loop over each player and check if there are more than 1 player that is active
        and make sure the game doesn't go long.
        """

        while True:
            the_time = dt.now()
            for player in self.players_still_in_game:
                # if the_time.replace(seconds=the_time.timetuple().tm_sec+1) == arrow.utcnow():
                #     self.display_second_stats()
                the_time = dt.now()
                # if self.force_game_over >= the_time and \
                if len(self.players_still_in_game) > 1:
                    self.turn(player)
                else:
                    raise OvertimeError("Game went too long")

    def player_is_out(self, player):
        # should be sold out but just in case
        for square in self.owned_by(player):
            player.sell(square=square)

    def __enter__(self):
        if Path('monopoly_data.json').exists():
            self.stats = pd.read_json(Path('monopoly_data.json').read_text())

        else:
            self.stats = pd.DataFrame(
                columns=['game_no', 'player', 'lap', 'bought_or_sold', 'house', 'property_location'])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.timeout:
            print('timeout')
            return
        else:
            with open('monopoly_stats.json', 'w') as statsfile:
                statsfile.write(pd.DataFrame.to_json(self.stats))

                # I should have information about the winners and losers
                # what properties I had on which lap they bought particular properties,
                # which lap they bought particular houses on properties.
