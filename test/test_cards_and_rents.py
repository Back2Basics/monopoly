import unittest
from cards_and_rents import *
from players import Player, Generic_Strategy
import numpy as np
import pandas.util.testing as pdt


class HowMuchRentTests(unittest.TestCase):
    def setUp(self):
        """setUp is called before every test"""
        self.g1 = Gameinfo()
        self.p1 = Player(playername='John', game=self.g1)
        self.p1.strategy = Generic_Strategy(game=self.g1, player=self.p1)
        self.p2 = Player(playername='Anna', game=self.g1)
        self.p2.strategy = Generic_Strategy(game=self.g1, player=self.p2)
        self.g1.playerlist.append(self.p1)
        self.g1.playerlist.append(self.p2)

    def tearDown(self):
        del (self.g1)

    def test_how_much_rent(self):
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p2, 0))  # answer is player 2 has 0 rent to pay
        self.g1.buy(self.p1, 1)
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 2))
        self.g1.buy_house(self.p1, 1)
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 10))

    def test_how_much_rent(self):

        self.g1.buy(self.p1, 1)
        self.g1.buy(self.p1, 7)

        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 2))

        self.g1.buy_house(self.p1, 1)

        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 10))

        self.g1.buy(self.p1, 5)
        self.assertEqual(self.g1.how_much_rent(5, self.p2), (self.p1, 25))  # it's a railroad

        self.g1.buy(self.p1, 15)
        self.assertEqual(self.g1.how_much_rent(5, self.p2), (self.p1, 50))  # it's a railroad

        self.g1.buy(self.p1, 25)
        self.assertEqual(self.g1.how_much_rent(5, self.p2), (self.p1, 100))  # it's a railroad

        self.assertNotEqual(self.g1.how_much_rent(5, self.p2), (self.p1, 50))  # it's a railroad
        self.g1.buy(self.p1, 28)
        self.g1.buy(self.p1, 12)

        a, b = self.g1.how_much_rent(12, self.p2)

        self.assertLessEqual(b, 120)  # it's a utility
        self.assertGreaterEqual(b, 20)  # it's a utility

    def test_owned_by(self):
        self.g1.buy(self.p1, 1)
        self.g1.buy(self.p1, 3)
        self.g1.buy(self.p1, 6)
        self.g1.buy(self.p1, 9)

        self.g1.buy(self.p1, 11)
        self.g1.buy(self.p1, 12)
        self.g1.buy(self.p1, 25)
        self.assertEqual(self.g1.owned_by(square=1), self.p1)
        self.assertFalse(self.g1.owned_by(square=1) == self.p2)
        self.assertNotEqual(self.g1.owned_by(square=11), self.p2)

    def test_double_rent(self):
        self.g1.buy(self.p1, 1)
        self.g1.buy_house(self.p1, 1)
        self.g1.buy(self.p1, 3)
        self.g1.buy(self.p1, 4)

        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 20))
        self.assertEqual(self.g1.how_much_rent(3, self.p2), (self.p1, 8))  # only pay single
        self.g1.buy(self.p1, 5)  # till p1 buys all 3 properties
        self.assertEqual(self.g1.how_much_rent(3, self.p2), (self.p1, 8))  # then the rent is doubled

    def test_sell_properties(self):
        self.g1.buy(self.p1, 15)
        self.g1.buy(self.p1, 16)
        self.g1.buy(self.p1, 17)
        self.g1.buy(self.p1, 18)
        self.g1.buy(self.p1, 19)
        self.g1.buy(self.p1, 20)
        self.g1.buy(self.p1, 21)
        self.g1.buy(self.p1, 22)
        self.g1.buy(self.p1, 23)
        self.g1.buy(self.p1, 24)
        self.g1.buy(self.p1, 25)
        self.g1.buy(self.p1, 26)
        self.g1.buy(self.p1, 27)
        self.assertEqual(self.p1.money, 60)

    def test_house_buying_and_history(self):
        """tests buying property/houses on each square"""
        self.p1.money = 1000000000

        for property in range(len(self.g1.board)):
            self.g1.buy(self.p1, property)
            rotation = property
            test_array = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int8)
            last_turn = np.zeros(40, dtype=np.int8)
            for house in range(1, 6):  # treat apartments like houses
                self.g1.buy_house(self.p1, property)
                # should have a property and a house.
                np.testing.assert_array_equal(self.p1.buying_houses_history,
                                              ((self.g1.board.type == 'property') * 1).values * house *
                                              np.roll(test_array, property)+ last_turn
                                              )

            self.p1.buying_houses_history = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int8)
            # won't buy another house
            self.g1.buy_house(self.p1, 1)
            np.testing.assert_array_equal(self.p1.buying_houses_history,
                                          ((self.g1.board.type == 'property') * 1).values * test_array * 5  # not 6
                                          )

    def test_turn(self):
        old_position = self.p1.current_position
        self.g1.turn(self.p1)
        self.assertGreater(self.p1.current_position, old_position)

    def test_buy_every_square(self):
        '''give player 1 the money to buy every square available'''
        self.p1.money = 100000
        my_list = []
        for square in range(len(self.g1.board)):
            self.g1.buy(player=self.p1, square=square)
            my_list.append(abs(self.p1.money - 100000))
        compare = pd.Series(my_list, name='cost')
        pdt.assert_series_equal(compare, self.g1.board.cost.cumsum())
