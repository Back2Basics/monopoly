import os
from random import randint
import pandas as pd
from copy import deepcopy
import arrow

basePath = os.path.dirname(os.path.abspath(__file__))


class Gameinfo:
    def __init__(self):
        self.rounds_to_play = 1
        self.timeout = False
        self.board = pd.read_json(basePath + os.sep + 'board.json')
        self.board.index = self.board.index.map(int)
        # self.board.cost = self.board.cost.map(int)
        self.board.type = self.board.type.map(str)
        self.board.sort_index(inplace=True)
        self.playerlist = []
        self.house_cost = 150
        self.board.houses = 0

    def owned_by(self, square=0):
        return self.board.owner.iloc[square]

    def is_buyable(self, square):
        """can you buy the place?"""
        if square in self.board[(self.board.type == 'gov')].index:
            return False
        elif self.owned_by(square) == None:
            return True
        else:
            return False

    def is_property(self, square):
        return self.board.type[square] == 'property'

    def is_house_buyable(self, player, square):
        if self.is_property(square) and \
                        square in self.board[((self.board.owner == player) & (self.board.houses < 5))].index:
            return True
        return False

    def buy(self, player, square):
        """ mutates state, buying a Property"""
        if self.is_buyable(square) and player.money > self.board.cost[square]:
            if player.should_i_buy_square(square) == True:
                player.money -= self.board.cost.iloc[square]
                self.board.owner[square] = player
                player.buying_property_history.add(square)
                return True
        return False

    def buy_house(self, player, square):
        """ mutates state, buying a house"""
        if self.is_house_buyable(player, square):
            if square in self.board[((self.board.owner == player) & (self.board.houses < 5))].index:
                if player.should_i_buy_house(square):
                    self.board.houses.iloc[square] += 1
                    player.money -= self.house_cost
                    print('player {} bought a house # {} at {}'.format(player, self.board.houses.iloc[square],
                                                                       self.board.name.iloc[square]))
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
        print('{} pay {} rent on {}'.format(player, rent, player.current_position))

        if self.check_money(player, rent):
            if owner == 'gov':  # don't act on this extra money
                pass
            else:
                owner.money += rent
                player.money = player.money - rent
        else:
            print(player.money, rent)

            if player.money < 0:
                while (True):
                    can_pay = player.get_money_by_selling()
                    if can_pay:
                        try:
                            owner.money += rent
                        except TypeError as e:
                            print(owner.money)
                            print(rent)
                            print('error was {}'.format(e))
                            sys.exit()
                        return True
                    else:
                        self.active = False
                        return False

    def utility_rent(self):
        if len(set([self.owned_by(12), self.owned_by(28)])) == 2:
            return (randint(2, 12) * 4)
        else:
            return (randint(2, 12) * 10)

    def how_much_rent(self, square, player=None):  # n is board index
        """question is how much rent do I need to pay and to whom
        so pass in player = self
        :return How_much, to_whom
        """
        # nobody owns the square
        if pd.isnull(self.board.owner.iloc[square]):
            return player, 0
        if self.owned_by(square) == player:  # the player owns it
            return player, 0

        owner = self.owned_by(square)
        if self.board.type.iloc[square] == 'gov':
            if square== 4: # landed on Income Tax
                tax = max(int(player.money*0.15), 50) #greater of 50 or 15% #TODO: I need to check the board
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
                print('square: {}'.format(square))
                print('self.board.rent.iloc[square]: {}'.format(self.board.rent.iloc[square]))
                print('self.board.name.iloc[square]: {}'.format(self.board.name.iloc[square]))
                print('self.board.houses.iloc[square]: {}'.format(self.board.houses.iloc[square]))
                print('self.board.iloc[square]: {}'.format(self.board.iloc[square]))
            return owner, rent_payment

    def display_player_stats(self):
        for player in self.playerlist:
            print(player.playername, player.current_position, int(player.money), player.active)

        print(self.board.owner)

    def turn(self, player):
        player.move()
        if player.current_position in (7,22,36): #chance squares
            #TODO: fix Chance in Game_info.turn
            return
        if player.current_position in (2,17,33):
            #TODO: fix community chest in Game_info.turn
            return

        is_recently_bought = self.buy(player, player.current_position)
        if is_recently_bought:
            return
        if self.owned_by(player.current_position) == player:
            is_house_bought = player.house_buying_strategy(player.current_position)
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
        players_copy = self.playerlist
        for game in range(self.rounds_to_play):
            self.playerlist = players_copy
            self.start_game()
            # game finishes here
            self.collect_stats()
            players_copy = deepcopy(self.playerlist)

    def start_game(self):

        self.starttime = arrow.utcnow()
        self.force_game_over = self.starttime.shift(seconds=10)

        self.loop_forever()
        print('Player {} Wins'.format([x for x in self.playerlist if x.active]))

    def loop_forever(self):
        """ loop over each player and check if there are more than 1 player that is active
        and make sure the game doesn't go long.
        """

        while True:
            for player in self.playerlist:
                the_time = arrow.utcnow()
                if self.force_game_over >= the_time and sum([1 for x in self.playerlist if x.active]) > 1:
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
