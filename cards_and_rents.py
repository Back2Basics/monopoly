import os
from random import randint
import pandas as pd
import numpy as np
import arrow
import json


class Gameinfo():
    def __init__(self):
        self.timeout = False
        self.board = pd.read_json(
            '{"color":{"0":"purple","1":"purple","2":null,"3":"bluegrey","4":"bluegrey","5":"bluegrey","6":"maroon","7":null,"8":"maroon","9":"maroon","10":null,"11":"orange","12":"orange","13":"orange","14":"red","15":"red","16":"red","17":null,"18":"yellow","19":"yellow","20":null,"21":"yellow","22":"green","23":"green","24":"green","25":null,"26":"blue","27":"blue"},"cost":{"0":60,"1":80,"2":200,"3":100,"4":100,"5":120,"6":140,"7":150,"8":140,"9":160,"10":200,"11":180,"12":180,"13":200,"14":220,"15":220,"16":240,"17":200,"18":260,"19":260,"20":150,"21":280,"22":300,"23":300,"24":320,"25":200,"26":350,"27":400},"name":{"0":"Mediterranean Ave.","1":"Baltic Ave.","2":"Reading Railroad.","3":"Oriental Ave.","4":"Vermont Ave.","5":"Conneticut Ave.","6":"St. Charles Pl.","7":"Electric Company","8":"States Ave.","9":"Virginia Ave","10":"Pennsylvania Railroad","11":"St. James Pl.","12":"Tennessee Ave.","13":"New York Ave.","14":"Kentucky Ave.","15":"Indiana Ave.","16":"Illinois Ave.","17":"B&O Railroad","18":"Atlantic Ave.","19":"Ventnor Ave.","20":"Water Works","21":"Marvin Gardens","22":"Pacific Ave.","23":"North Carolina Ave.","24":"Pennsylvania Ave.","25":"Short Line Railroad","26":"Park Pl.","27":"Boardwalk"},"rent":{"0":[2,10,30,90,160,250],"1":[4,20,60,180,320,450],"2":[25,50,100,200],"3":[6,30,90,270,400,550],"4":[6,30,90,270,400,550],"5":[8,40,100,300,450,600],"6":[10,50,150,450,625,750],"7":"dice","8":[10,50,150,450,625,750],"9":[12,60,180,500,700,900],"10":[25,50,100,200],"11":[44,70,200,550,750,950],"12":[44,70,200,550,750,950],"13":[16,80,220,600,800,1000],"14":[18,90,250,700,875,1050],"15":[18,90,250,700,875,1050],"16":[20,100,300,750,925,1100],"17":[25,50,100,200],"18":[22,110,330,800,975,1150],"19":[22,110,330,800,975,1150],"20":"dice","21":[24,120,360,850,1025,1200],"22":[26,130,390,900,1100,1275],"23":[26,130,390,900,1100,1275],"24":[28,150,450,1000,1200,1400],"25":[25,50,100,200],"26":[35,175,500,1100,1300,1500],"27":[50,200,600,1400,1700,2000]},"type":{"0":"property","1":"property","2":"railroad","3":"property","4":"property","5":"property","6":"property","7":"utility","8":"property","9":"property","10":"railroad","11":"property","12":"property","13":"property","14":"property","15":"property","16":"property","17":"railroad","18":"property","19":"property","20":"utility","21":"property","22":"property","23":"property","24":"property","25":"railroad","26":"property","27":"property"},"owner":{"0":null,"1":null,"2":null,"3":null,"4":null,"5":null,"6":null,"7":null,"8":null,"9":null,"10":null,"11":null,"12":null,"13":null,"14":null,"15":null,"16":null,"17":null,"18":null,"19":null,"20":null,"21":null,"22":null,"23":null,"24":null,"25":null,"26":null,"27":null},"houses":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0,"24":0,"25":0,"26":0,"27":0}}'
        )
        self.board.index = self.board.index.map(int)
        self.board.cost = self.board.cost.map(int)
        self.board.type = self.board.type.map(str)
        self.playerlist = []
        self.house_cost = 150

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

        # railroads and utilities have to come first because they don't have a color
        if self.board.type[idx] == 'railroad':
            # add players Railroad cards
            owns_rr = self.board.owner[self.board.type == 'railroad']
            how_many_rr_does_player_own = (owns_rr == owner).sum()

            return owner, self.board.rent[idx][how_many_rr_does_player_own - 1]

        elif self.board.type[idx] == 'utility':
            return owner, self.utility_rent()
        elif owner != player and \
                        len(set(
                            self.board.owner[self.board[self.board.color == self.board.color[
                                idx]].index])) == 1:  # player owns all of a color
            return owner, self.board.rent[idx][self.board.houses.iloc[idx]] * 2
        else:
            # what is this again
            try:
                something = self.board.rent.iloc[idx][self.board.houses.iloc[idx]]
            except BaseException:
                print('idx: {}'.format(idx))
                print('self.board.houses.iloc[idx]: {}'.format(self.board.houses.iloc[idx]))
                print('sself.board.rent.iloc[idx]: {}'.format(self.board.rent.iloc[idx]))
            return owner, something

    def owned_properties(self):
        return self.board[self.board.owner.isnull() == False].index

    def owned_by(self, idx=0):
        return self.board.owner.iloc[idx]

    def turn(self, player):
        player.move()
        owns = self.owned_by(player.pos)
        if player == owns or pd.isnull(owns):
            player.buy((self, player.pos), player.percentage)
        else:
            player.pay_rent()  # owns, self.how_much_rent(player.pos, player=player))

    def start(self):

        self.starttime = arrow.utcnow()
        self.force_game_over = self.starttime.shift(seconds=60)

        self.loop_forever()

    def loop_forever(self):
        while (True):
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
