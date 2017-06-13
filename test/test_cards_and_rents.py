import unittest
from cards_and_rents import *
from players import Player, Generic_Strategy
import numpy as np


class FirstTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        """setUp is called before every test"""
        self.g1 = Gameinfo()
        self.p1 = Player(playername='John', game=self.g1)
        self.p1.strategy = Generic_Strategy(game=self.g1, player=self.p1)
        self.p2 = Player('Anna')
        self.p2.strategy = Generic_Strategy(game=self.g1, player=self.p2)
        self.g1.playerlist.append(self.p1)
        self.g1.playerlist.append(self.p2)

    def test_how_much_rent(self):
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p2, 0))  # answer is player 2 has 0 rent to pay
        self.g1.buy(self.p1, 1)
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 2))
        self.g1.buy_house(self.p1, 1)
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 10))


class HowMuchRentTests(unittest.TestCase):
    def setUp(self):
        self.g3 = Gameinfo()
        self.p1 = Player(playername='John', game=self.g3)
        self.p1.strategy = Generic_Strategy(game=self.g3, player=self.p1)
        self.p2 = Player('Anna')
        self.p2.strategy = Generic_Strategy(game=self.g3, player=self.p2)
        self.g3.playerlist.append(self.p1)
        self.g3.playerlist.append(self.p2)
        self.g3.buy(self.p1, 1)
        self.g3.buy(self.p1, 7)

    def test_how_much_rent(self):
        self.assertEqual(self.g3.how_much_rent(1, self.p2), (self.p1, 2))

        self.g3.buy_house(self.p1, 1)

        self.assertEqual(self.g3.how_much_rent(1, self.p2), (self.p1, 10))

        self.g3.buy(self.p1, 5)
        self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 25))  # it's a railroad

        self.g3.buy(self.p1, 15)
        self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 50))  # it's a railroad

        self.g3.buy(self.p1, 25)
        self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 100))  # it's a railroad

        self.assertNotEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 50))  # it's a railroad
        self.g3.buy(self.p1, 28)
        self.g3.buy(self.p1, 12)

        a, b = self.g3.how_much_rent(12, self.p2)

        self.assertLessEqual(b, 120)  # it's a utility
        self.assertGreaterEqual(b, 20)  # it's a utility


class OwnedPropertyTests(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.g2 = Gameinfo()
        self.p1 = Player(game=self.g2, playername='John')
        self.p1.strategy = Generic_Strategy(game=self.g2, player=self.p1)
        self.p2 = Player(game=self.g2, playername='Anna')
        self.p2.strategy = Generic_Strategy(game=self.g2, player=self.p2)
        self.g2.playerlist.append(self.p1)  # john buys 100 percent of the time
        self.g2.playerlist.append(self.p2)  # anna buys 100 percent of the time
        self.g2.buy(self.p1, 1)
        self.g2.buy(self.p1, 3)
        self.g2.buy(self.p1, 6)
        self.g2.buy(self.p1, 9)

        self.g2.buy(self.p1, 11)
        self.g2.buy(self.p1, 12)
        self.g2.buy(self.p1, 25)

    # def test_owned_properties(self):
    #     self.assertNotEqual(self.g2.owned_properties(), [1, 3, 6, 9])
    #     self.assertEqual(list(self.g2.owned_properties()), [1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 17, 20, 22, 25, 30, 33, 36]) #'gov' + player2

    def test_owned_by(self):
        self.assertEqual(self.g2.owned_by(square=1), self.p1)
        self.assertFalse(self.g2.owned_by(square=1) == self.p2)
        self.assertNotEqual(self.g2.owned_by(square=11), self.p2)


class HowMuchDoubleRentTests(unittest.TestCase):
    def setUp(self):
        self.g4 = Gameinfo()
        self.p1 = Player(game=self.g4, playername='John')
        self.p1.strategy = Generic_Strategy(game=self.g4, player=self.p1)
        self.p2 = Player(game=self.g4, playername='Anna')
        self.p2.strategy = Generic_Strategy(game=self.g4, player=self.p2)
        self.g4.playerlist.append(self.p1)
        self.g4.playerlist.append(self.p2)

        self.g4.buy(self.p1, 1)
        self.g4.buy_house(self.p1, 1)
        self.g4.buy(self.p1, 3)
        self.g4.buy(self.p1, 4)

    def test_double_rent(self):
        self.assertEqual(self.g4.how_much_rent(1, self.p2), (self.p1, 20))
        self.assertEqual(self.g4.how_much_rent(3, self.p2), (self.p1, 8))  # only pay single
        self.g4.buy(self.p1, 5)  # till p1 buys all 3 properties
        self.assertEqual(self.g4.how_much_rent(3, self.p2), (self.p1, 8))  # then the rent is doubled


class SellingProperties(unittest.TestCase):
    def setUp(self):
        self.g5 = Gameinfo()
        self.p1 = Player(game=self.g5, playername='John')
        self.p1.strategy = Generic_Strategy(game=self.g5, player=self.p1)
        self.p2 = Player(game=self.g5, playername='Anna')
        self.p2.strategy = Generic_Strategy(game=self.g5, player=self.p2)
        self.g5.playerlist.append(self.p1)
        self.g5.playerlist.append(self.p2)

    def test_sell_properties(self):
        self.g5.buy(self.p1, 15)
        self.g5.buy(self.p1, 16)
        self.g5.buy(self.p1, 17)
        self.g5.buy(self.p1, 18)
        self.g5.buy(self.p1, 19)
        self.g5.buy(self.p1, 20)
        self.g5.buy(self.p1, 21)
        self.g5.buy(self.p1, 22)
        self.g5.buy(self.p1, 23)
        self.g5.buy(self.p1, 24)
        self.g5.buy(self.p1, 25)
        self.g5.buy(self.p1, 26)
        self.g5.buy(self.p1, 27)
        self.assertEqual(self.p1.money, 60)


class test_stats(unittest.TestCase):
    def setUp(self):
        self.g6 = Gameinfo()
        self.p1 = Player(game=self.g6, playername='John')
        self.p1.strategy = Generic_Strategy(game=self.g6, player=self.p1)
        self.p2 = Player(game=self.g6, playername='Anna')
        self.p2.strategy = Generic_Strategy(game=self.g6, player=self.p2)
        self.g6.playerlist.append(self.p1)
        self.g6.playerlist.append(self.p2)

    def test_1buy(self):
        self.g6.buy(self.p1, 1)
        self.g6.buy_house(self.p1, 1)
        # should have a property and a house.
        self.assertSetEqual(self.p1.buying_property_history, set([1]))
        np.testing.assert_array_equal(self.p1.buying_houses_history,
                                      np.array([0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        self.g6.buy_house(self.p1, 1)
        np.testing.assert_array_equal(self.p1.buying_houses_history,
                                      np.array([0., 2., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        self.g6.buy_house(self.p1, 1)
        np.testing.assert_array_equal(self.p1.buying_houses_history,
                                      np.array([0., 3., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        self.g6.buy_house(self.p1, 1)
        np.testing.assert_array_equal(self.p1.buying_houses_history,
                                      np.array([0., 4., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        self.g6.buy_house(self.p1, 1)
        np.testing.assert_array_equal(self.p1.buying_houses_history,
                                      np.array([0., 5., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        # won't buy another house
        self.g6.buy_house(self.p1, 1)
        np.testing.assert_array_equal(self.p1.buying_houses_history,
                                      np.array([0., 5., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))


class GameInfoTurn(unittest.TestCase):
    @classmethod
    def setUp(self):
        """setUp is called before every test"""
        self.g8 = Gameinfo()
        self.p1 = Player(playername='John', game=self.g8)
        self.p1.strategy = Generic_Strategy(game=self.g8, player=self.p1)
        self.p2 = Player('Anna')
        self.p2.strategy = Generic_Strategy(game=self.g8, player=self.p2)
        self.g8.playerlist.append(self.p1)
        self.g8.playerlist.append(self.p2)

    def test_turn(self):
        old_position = self.p1.current_position
        self.g8.turn(self.p1)
        self.assertGreater(self.p1.current_position, old_position)


class BuyProperties(unittest.TestCase):
    @classmethod
    def setUp(self):
        """setUp is called before every test"""
        self.g9 = Gameinfo()
        self.p1 = Player(playername='John', game=self.g9)
        self.p1.strategy = Generic_Strategy(game=self.g9, player=self.p1)
        self.p2 = Player('Anna')
        self.p2.strategy = Generic_Strategy(game=self.g9, player=self.p2)
        self.g9.playerlist.append(self.p1)
        self.g9.playerlist.append(self.p2)
        self.p1.money = 100000

    def test_buy(self):
        for square in range(39):
            self.g9.buy(player=self.p1, square=square)
            print("square = {}, self.p1.money = {}".format(square, self.p1.money))
        self.assertEqual(abs(self.p1.money - 10000), self.g9.board.cost.sum())


if __name__ == '__main__':
    unittest.main()
