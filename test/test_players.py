import unittest
from cards_and_rents import *
from players import Player, Generic_Strategy
import numpy as np


class Players(unittest.TestCase):
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

    def test_move(self):
        self.assertEqual(self.p1.current_position,0)
        self.p1.move()
        self.assertNotEqual(self.p1.current_position,0)
        self.assertLessEqual(self.p1.current_position,12)

    def test_pass_go(self):
        self.p1.current_position = 39
        the_money = self.p1.money
        self.p1.move()
        self.assertEqual(self.p1.money, the_money+200)

    def test_is_owned(self):
        self.g1.buy_property(player=self.p1, square=1)
        self.assertEqual(self.p1.is_owned(square=1), True)


