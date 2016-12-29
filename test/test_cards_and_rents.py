import unittest
from cards_and_rents import *
from players import Player
import numpy as np


class FirstTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        """setUp is called before every test"""
        self.g1 = Gameinfo()
        self.g1.playerlist.append(Player(self.g1, 'John', 100))  # john buys 100 percent of the time
        self.g1.playerlist.append(Player(self.g1, 'Anna', 100))  # anna buys 100 percent of the time
        self.p1 = self.g1.playerlist[0]
        self.p2 = self.g1.playerlist[1]

    def test_how_much_rent(self):
        self.assertEqual(self.g1.how_much_rent(0, self.p2), (self.p2, 0))
        self.p1.buy((self.g1, 0), 100)
        self.assertEqual(self.g1.how_much_rent(0, self.p2), (self.p1, 2))
        self.p1.buy((self.g1, 0), 100)
        self.assertEqual(self.g1.how_much_rent(0, self.p2), (self.p1, 10))


class OwnedPropertyTests(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.g1 = Gameinfo()
        self.g1.playerlist.append(Player(self.g1, 'John', 100))  # john buys 100 percent of the time
        self.g1.playerlist.append(Player(self.g1, 'Anna', 100))  # anna buys 100 percent of the time
        self.p1 = self.g1.playerlist[0]
        self.p2 = self.g1.playerlist[1]

        self.p1.buy((self.g1, 0), 100)
        self.p1.buy((self.g1, 3), 100)
        self.p1.buy((self.g1, 6), 100)
        self.p1.buy((self.g1, 9), 100)

        self.p2.buy((self.g1, 10), 100)
        self.p2.buy((self.g1, 12), 100)
        self.p2.buy((self.g1, 25), 100)

    def test_owned_properties(self):
        self.assertNotEqual(self.g1.owned_properties(), [0, 3, 6, 9])
        self.assertEqual(list(self.g1.owned_properties()), [0, 3, 6, 9, 10, 12, 25])

    def test_owned_by(self):
        self.assertEqual(self.g1.owned_by(idx=0), self.p1)
        self.assertFalse(self.g1.owned_by(idx=0) == self.p2)
        self.assertEqual(self.g1.owned_by(idx=10), self.p2)


class HowMuchRentTests(unittest.TestCase):
    def setUp(self):
        self.g1 = Gameinfo()
        self.g1.playerlist.append(Player(self.g1, 'John', 100))  # John buys 100 percent of the time
        self.g1.playerlist.append(Player(self.g1, 'Anna', 100))  # Anna buys 100 percent of the time
        self.p1 = self.g1.playerlist[0]
        self.p2 = self.g1.playerlist[1]
        self.p1.buy((self.g1, 0), 100)
        self.p1.buy((self.g1, 7), 100)

    def test_how_much_rent(self):
        self.assertEqual(self.g1.how_much_rent(0, self.p2), (self.p1, 2))
        self.p1.buy((self.g1, 0), 100)
        self.p1.buy((self.g1, 2), 100)

        self.assertEqual(self.g1.how_much_rent(0, self.p2), (self.p1, 10))
        self.assertEqual(self.g1.how_much_rent(2, self.p2), (self.p1, 25))  # it's a railroad
        self.p1.buy((self.g1, 10), 100)
        self.assertEqual(self.g1.how_much_rent(2, self.p2), (self.p1, 50))  # it's a railroad
        self.p1.buy((self.g1, 17), 100)
        self.assertEqual(self.g1.how_much_rent(2, self.p2), (self.p1, 100))  # it's a railroad
        self.p1.buy((self.g1, 25), 100)
        self.assertEqual(self.g1.how_much_rent(2, self.p2), (self.p1, 200))  # it's a railroad
        self.p1.buy((self.g1, 2), 100)
        self.assertNotEqual(self.g1.how_much_rent(2, self.p2), (self.p1, 50))  # it's a railroad
        a, b = self.g1.how_much_rent(7, self.p2)

        self.assertLessEqual(b, 120)  # it's a utility
        self.assertGreaterEqual(b, 20)  # it's a utility


class HowMuchDoubleRentTests(unittest.TestCase):
    def setUp(self):
        self.g1 = Gameinfo()
        self.g1.playerlist.append(Player(self.g1, 'John', 100))  # john buys 100 percent of the time
        self.g1.playerlist.append(Player(self.g1, 'Anna', 100))  # anna buys 100 percent of the time
        self.p1 = self.g1.playerlist[0]
        self.p2 = self.g1.playerlist[1]
        self.p1.buy((self.g1, 0), 100)
        self.p1.buy((self.g1, 1), 100)
        self.p1.buy((self.g1, 3), 100)
        self.p1.buy((self.g1, 4), 100)


    def test_double_rent(self):
        self.assertEqual(self.g1.how_much_rent(0, self.p2), (self.p1, 4))
        self.assertEqual(self.g1.how_much_rent(3, self.p2), (self.p1, 6)) #only pay single
        self.p1.buy((self.g1, 5), 100)  #till p1 buys all 3 properties
        self.assertEqual(self.g1.how_much_rent(3, self.p2), (self.p1, 12)) #then the rent is doubled

class RunGame(unittest.TestCase):
    def setUp(self):
        self.g1 = Gameinfo()
        self.g1.playerlist.append(Player(self.g1, 'John', 100))  # john buys 100 percent of the time
        self.g1.playerlist.append(Player(self.g1, 'Anna', 100))  # anna buys 100 percent of the time
        self.p1 = self.g1.playerlist[0]
        self.p2 = self.g1.playerlist[1]
        self.g1.turn(self.p1)
        # self.p1.buy((self.g1, 0),100)
        # self.p2.buy((self.g1, 1),100)

    def test_owned_properties_(self):
        self.assertGreaterEqual(len(self.g1.owned_properties()), 1)

class SellingProperties(unittest.TestCase):
    def setUp(self):
        self.g1 = Gameinfo()
        self.g1.playerlist.append(Player(self.g1, 'John', 100))  # john buys 100 percent of the time
        self.g1.playerlist.append(Player(self.g1, 'Anna', 100))  # anna buys 100 percent of the time
        self.p1 = self.g1.playerlist[0]
        self.p2 = self.g1.playerlist[1]

    def test_sell_properties(self):
        self.p1.buy((self.g1, 15), 100)
        self.p1.buy((self.g1, 16), 100)
        self.p1.buy((self.g1, 17), 100)
        self.p1.buy((self.g1, 18), 100)
        self.p1.buy((self.g1, 19), 100)
        self.p1.buy((self.g1, 20), 100)
        self.p1.buy((self.g1, 21), 100)
        self.p1.buy((self.g1, 22), 100)
        self.p1.buy((self.g1, 23), 100)
        self.p1.buy((self.g1, 24), 100)
        self.p1.buy((self.g1, 25), 100)
        self.p1.buy((self.g1, 26), 100)
        self.p1.buy((self.g1, 27), 100)
        self.assertEqual(self.p1.money,170)
        self.assertSetEqual(set(self.g1.owned_properties()), set([15, 16, 17, 18, 19, 20]))

#
# File "/Users/jlangley/Documents/code/monopoly/cards_and_rents.py", line 209, in start
# self.turn()
# File "/Users/jlangley/Documents/code/monopoly/cards_and_rents.py", line 200, in turn
# player.pay_rent()#owns, self.how_much_rent(player.pos, player=player))
# File "/Users/jlangley/Documents/code/monopoly/players.py", line 103, in pay_rent
# can_pay = self.get_money_by_selling()
# File "/Users/jlangley/Documents/code/monopoly/players.py", line 91, in get_money_by_selling
# self.sell(idx)
# File "/Users/jlangley/Documents/code/monopoly/players.py", line 72, in sell
# if self.board.iloc[pos]['houses'] > 0:


if __name__ == '__main__':
    unittest.main()
