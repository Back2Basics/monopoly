import os
from random import randint
import pandas as pd
from copy import deepcopy
import arrow
import numpy as np
basePath = os.path.dirname(os.path.abspath(__file__))

class Gameinfo:
    def __init__(self):
        self.rounds_to_play = 1
        self.timeout = False
        self.board = pd.read_json(basePath + os.sep + 'board.json')
        self.board.index = self.board.index.map(int)
        #self.board.cost = self.board.cost.map(int)
        self.board.type = self.board.type.map(str)
        self.board.sort_index(inplace=True)
        self.playerlist = []
        self.house_cost = 150
        self.board.houses = 0

    # TODO: Fix the headings: one column for owners and the other for houses


    def utility_rent(self):
        if len(set([self.owned_by(7), self.owned_by(20)])) == 2:
            return randint(2, 12) * 10
        else:
            return randint(2, 12) * 4

    def how_much_rent(self, idx, player=None):  # n is board index
        """question is how much rent do I need to pay and to whom
        so pass in player = self
        """
        if self.owned_by(idx) == player or pd.isnull(
                self.board.owner.iloc[idx]):  # the player or nobody owns it
            return player, 0
        owner = self.owned_by(idx)
        if self.board.type[idx] == 'gov':
            return 'gov', 0

        # railroads and utilities have to come first because they don't have a color
        if self.board.type[idx] == 'railroad':
            # add players Railroad cards
            owns_rr = self.board.owner[self.board.type == 'railroad']
            how_many_rr_does_player_own = (owns_rr == owner).sum()

            return owner, list(self.board.rent[idx])[how_many_rr_does_player_own - 1]

        elif self.board.type[idx] == 'utility':
            return owner, self.utility_rent()
        elif owner != player and \
                        len(set(
                            self.board.owner[self.board[self.board.color == self.board.color[
                                idx]].index])) == 1:  # player owns all of a color
            return owner, self.board.rent[idx][self.board.houses.iloc[idx]] * 2
        else: # properties

            try:
                something = self.board.rent.iloc[idx][self.board.houses.iloc[idx]]
            except BaseException:
                print('idx: {}'.format(idx))
                print('self.board.rent.iloc[idx]: {}'.format(self.board.rent.iloc[idx]))
                print('self.board.name.iloc[idx]: {}'.format(self.board.name.iloc[idx]))
                print('self.board.houses.iloc[idx]: {}'.format(self.board.houses.iloc[idx]))
            return owner, something

    def owned_properties(self):
        return self.board[self.board.owner.isnull() == False].index

    def owned_by(self, idx=0):
        return self.board.owner.iloc[idx]

    def turn(self, player):
        player.move()
        owns = self.owned_by(player.pos)
        if owns == 'gov':
            return
        if player == owns or pd.isnull(owns):
            player.buy((self, player.pos), player.percentage)
        else:
            player.pay_rent()  # owns, self.how_much_rent(player.pos, player=player))

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
        players_copy = self.playerlist
        for game in range(self.rounds_to_play):
            self.playerlist = players_copy
            self.start_game()
            #game finishes here
            self.collect_stats()
            players_copy = deepcopy(self.playerlist)


    def start_game(self):

        self.starttime = arrow.utcnow()
        self.force_game_over = self.starttime.shift(seconds=10)

        self.loop_forever()
        print('Player {} Wins'.format([x for x in self.playerlist if x.active]))

    def loop_forever(self):
        """loop over each player and check if there are more than 1 player that is active
        and make sure the game doesn't go long.
        """

        while True:
            for player in self.playerlist:
                the_time = arrow.utcnow()
                if self.force_game_over >= the_time and sum([True for x in self.playerlist if x.active]) > 1:
                    if player.active:
                        self.turn(player)
                    the_time = arrow.utcnow()
                else:

                    return

    def __enter__(self):
        if os.path.exists('monopoly_data.json'):
            self.stats = pd.read_json('monopoly_data.json')

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
