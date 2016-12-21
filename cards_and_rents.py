import os
from random import randint
import pandas as pd
import numpy as np
import arrow
import json


class Gameinfo():
    def __init__(self):
        self.timeout = False
        self.board = pd.DataFrame([{'color': 'purple',
                                    'cost': 60,
                                    'name': 'Mediterranean Ave.',
                                    'rent': [2, 10, 30, 90, 160, 250],
                                    'type': 'property'},
                                   {'color': 'purple',
                                    'cost': 80,
                                    'name': 'Baltic Ave.',
                                    'rent': [4, 20, 60, 180, 320, 450],
                                    'type': 'property'},
                                   {'cost': 200,
                                    'name': 'Reading Railroad.',
                                    'rent': [25, 50, 100, 200],
                                    'type': 'railroad'},
                                   {'color': 'bluegrey',
                                    'cost': 100,
                                    'name': 'Oriental Ave.',
                                    'rent': [6, 30, 90, 270, 400, 550],
                                    'type': 'property'},
                                   {'color': 'bluegrey',
                                    'cost': 100,
                                    'name': 'Vermont Ave.',
                                    'rent': [6, 30, 90, 270, 400, 550],
                                    'type': 'property'},
                                   {'color': 'bluegrey',
                                    'cost': 120,
                                    'name': 'Conneticut Ave.',
                                    'rent': [8, 40, 100, 300, 450, 600],
                                    'type': 'property'},
                                   {'color': 'maroon',
                                    'cost': 140,
                                    'name': 'St. Charles Pl.',
                                    'rent': [10, 50, 150, 450, 625, 750],
                                    'type': 'property'},
                                   {'cost': 150,
                                    'name': 'Electric Company',
                                    'rent': 'dice',
                                    'type': 'utility'},
                                   {'color': 'maroon',
                                    'cost': 140,
                                    'name': 'States Ave.',
                                    'rent': [10, 50, 150, 450, 625, 750],
                                    'type': 'property'},
                                   {'color': 'maroon',
                                    'cost': 160,
                                    'name': 'Virginia Ave',
                                    'rent': [12, 60, 180, 500, 700, 900],
                                    'type': 'property'},
                                   {'cost': 200,
                                    'name': 'Pennsylvania Railroad',
                                    'rent': [25, 50, 100, 200],
                                    'type': 'railroad'},
                                   {'color': 'orange',
                                    'cost': 180,
                                    'name': 'St. James Pl.',
                                    'rent': [44, 70, 200, 550, 750, 950],
                                    'type': 'property'},
                                   {'color': 'orange',
                                    'cost': 180,
                                    'name': 'Tennessee Ave.',
                                    'rent': [44, 70, 200, 550, 750, 950],
                                    'type': 'property'},
                                   {'color': 'orange',
                                    'cost': 200,
                                    'name': 'New York Ave.',
                                    'rent': [16, 80, 220, 600, 800, 1000],
                                    'type': 'property'},
                                   {'color': 'red',
                                    'cost': 220,
                                    'name': 'Kentucky Ave.',
                                    'rent': [18, 90, 250, 700, 875, 1050],
                                    'type': 'property'},
                                   {'color': 'red',
                                    'cost': 220,
                                    'name': 'Indiana Ave.',
                                    'rent': [18, 90, 250, 700, 875, 1050],
                                    'type': 'property'},
                                   {'color': 'red',
                                    'cost': 240,
                                    'name': 'Illinois Ave.',
                                    'rent': [20, 100, 300, 750, 925, 1100],
                                    'type': 'property'},
                                   {'cost': 200,
                                    'name': 'B&O Railroad',
                                    'rent': [25, 50, 100, 200],
                                    'type': 'railroad'},
                                   {'color': 'yellow',
                                    'cost': 260,
                                    'name': 'Atlantic Ave.',
                                    'rent': [22, 110, 330, 800, 975, 1150],
                                    'type': 'property'},
                                   {'color': 'yellow',
                                    'cost': 260,
                                    'name': 'Ventnor Ave.',
                                    'rent': [22, 110, 330, 800, 975, 1150],
                                    'type': 'property'},
                                   {'cost': 150,
                                    'name': 'Water Works',
                                    'rent': 'dice',
                                    'type': 'utility'},
                                   {'color': 'yellow',
                                    'cost': 280,
                                    'name': 'Marvin Gardens',
                                    'rent': [24, 120, 360, 850, 1025, 1200],
                                    'type': 'property'},
                                   {'color': 'green',
                                    'cost': 300,
                                    'name': 'Pacific Ave.',
                                    'rent': [26, 130, 390, 900, 1100, 1275],
                                    'type': 'property'},
                                   {'color': 'green',
                                    'cost': 300,
                                    'name': 'North Carolina Ave.',
                                    'rent': [26, 130, 390, 900, 1100, 1275],
                                    'type': 'property'},
                                   {'color': 'green',
                                    'cost': 320,
                                    'name': 'Pennsylvania Ave.',
                                    'rent': [28, 150, 450, 1000, 1200, 1400],
                                    'type': 'property'},
                                   {'cost': 200,
                                    'name': 'Short Line Railroad',
                                    'rent': [25, 50, 100, 200],
                                    'type': 'railroad'},
                                   {'color': 'blue',
                                    'cost': 350,
                                    'name': 'Park Pl.',
                                    'rent': [35, 175, 500, 1100, 1300, 1500],
                                    'type': 'property'},
                                   {'color': 'blue',
                                    'cost': 400,
                                    'name': 'Boardwalk',
                                    'rent': [50, 200, 600, 1400, 1700, 2000],
                                    'type': 'property'}])
        self.owners = self.make_owners()
        self.playerlist = []
        self.house_cost = 150

    def make_owners(self):
        return pd.DataFrame(list(zip([np.NaN] * len(self.board), [0] * len(self.board))), columns=['owner', 'houses'])

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
                self.owners.owner.iloc[idx]):  # the player or nobody owns it
            return player, 0
        owner = self.owned_by(idx)

        # railroads and utilities have to come first because they don't have a color
        if self.board.type[idx] == 'railroad':
            # add players Railroad cards
            owns_rr = self.owners[self.board.type == 'railroad'].owner
            how_many_rr_does_player_own = (owns_rr == owner).sum()

            return owner, self.board.rent[idx][how_many_rr_does_player_own - 1]

        elif self.board.type[idx] == 'utility':
            return owner, self.utility_rent()
        elif owner != player and \
                        len(set(
                            self.owners.owner[self.board[self.board.color == self.board.color[
                                idx]].index])) == 1:  # player owns all of a color
            return owner, self.board.rent[idx][self.owners.houses.iloc[idx]] * 2
        else:
            #what is this again
            try:
                something = self.board.rent.iloc[idx][self.owners.houses.iloc[idx]]
            except BaseException:
                print('idx: {}'.format(idx))
                print('self.owners.houses.iloc[idx]: {}'.format(self.owners.houses.iloc[idx]))
                print('sself.board.rent.iloc[idx]: {}'.format(self.board.rent.iloc[idx]))
            return owner, something

    def owned_properties(self):
        return self.owners[self.owners.owner.isnull() == False].index

    def owned_by(self, idx=0):
        return self.owners.owner.iloc[idx]

    def turn(self):
        for player in self.playerlist:
            player.move()
            owns = self.owned_by(player.pos)
            if player == owns or pd.isnull(owns):
                player.buy((self, player.pos), player.percentage)  # has pay_rent built in
            else:
                player.pay_rent()  # owns, self.how_much_rent(player.pos, player=player))

    def start(self):

        self.starttime = arrow.utcnow()
        self.force_game_over = self.starttime.shift(seconds=60)
        the_time = arrow.utcnow()
        while self.force_game_over >= the_time and sum([True for x in self.playerlist if x.active])>1:
            self.turn()
            the_time = arrow.utcnow()


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
            with open('monopoly_stats.json','w') as statsfile:
                statsfile.write(pd.DataFrame.to_json(self.stats))

            # I should have information about the winners and losers
            # what properties I had on which lap they bought particular properties,
            # which lap they bought particular houses on properties.
