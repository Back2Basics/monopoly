import unittest
from cards_and_rents import *
from players import Player, Generic_Strategy


class FirstTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        """setUp is called before every test"""
        self.g1 = Gameinfo()
        self.p1 = Player('John')
        self.p1.strategy(Generic_Strategy(self.g1))
        self.p2 = Player('Anna')
        self.p2.strategy(Generic_Strategy(game=self.g1))
        self.g1.playerlist.append(self.p1)
        self.g1.playerlist.append(self.p2)

    def test_how_much_rent(self):
        self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p2, 0))  # answer is player 2 has 0 rent to pay
        self.g1.buy(self.p1, 1)
        #
        # self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 2))
        # self.p1.buy((self.g1, 1), 100)
        # self.assertEqual(self.g1.how_much_rent(1, self.p2), (self.p1, 10))


# class HowMuchRentTests(unittest.TestCase):
#     def setUp(self):
#         self.g3 = Gameinfo()
#         self.g3.playerlist.append(Player(self.g3, 'John', 100))  # John buys 100 percent of the time
#         self.g3.playerlist.append(Player(self.g3, 'Anna', 100))  # Anna buys 100 percent of the time
#         self.p1 = self.g3.playerlist[0]
#         self.p2 = self.g3.playerlist[1]
#         self.p1.buy((self.g3, 1), 100)
#         self.p1.buy((self.g3, 7), 100)
#
#     def test_how_much_rent(self):
#         self.assertEqual(self.g3.how_much_rent(1, self.p2), (self.p1, 2))
#         self.p1.buy((self.g3, 1), 100)
#         self.p1.buy((self.g3, 5), 100)
#
#         self.assertEqual(self.g3.how_much_rent(1, self.p2), (self.p1, 10))
#         self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 25))  # it's a railroad
#         self.p1.buy((self.g3, 15), 100)
#         self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 50))  # it's a railroad
#         self.p1.buy((self.g3, 25), 100)
#         self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 100))  # it's a railroad
#         self.p1.buy((self.g3, 35), 100)
#         self.assertEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 200))  # it's a railroad
#         self.p1.buy((self.g3, 12), 100)
#         self.assertNotEqual(self.g3.how_much_rent(5, self.p2), (self.p1, 50))  # it's a railroad
#         a, b = self.g3.how_much_rent(12, self.p2)
#
#         self.assertLessEqual(b, 120)  # it's a utility
#         self.assertGreaterEqual(b, 20)  # it's a utility
#
#
# class OwnedPropertyTests(unittest.TestCase):
#     @classmethod
#     def setUp(self):
#         self.g2 = Gameinfo()
#         self.g2.playerlist.append(Player(self.g2, 'John', 100))  # john buys 100 percent of the time
#         self.g2.playerlist.append(Player(self.g2, 'Anna', 100))  # anna buys 100 percent of the time
#         self.p1 = self.g2.playerlist[0]
#         self.p2 = self.g2.playerlist[1]
#
#         self.p1.buy((self.g2, 1), 100)
#         self.p1.buy((self.g2, 3), 100)
#         self.p1.buy((self.g2, 6), 100)
#         self.p1.buy((self.g2, 9), 100)
#
#         self.p2.buy((self.g2, 11), 100)
#         self.p2.buy((self.g2, 12), 100)
#         self.p2.buy((self.g2, 25), 100)
#
#     def test_owned_properties(self):
#         self.assertNotEqual(self.g2.owned_properties(), [1, 3, 6, 9])
#         self.assertEqual(list(self.g2.owned_properties()), [1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 17, 20, 22, 25, 30, 33, 36]) #'gov' + player2
#
#     def test_owned_by(self):
#         self.assertEqual(self.g2.owned_by(idx=1), self.p1)
#         self.assertFalse(self.g2.owned_by(idx=1) == self.p2)
#         self.assertEqual(self.g2.owned_by(idx=11), self.p2)
#
#
# class HowMuchDoubleRentTests(unittest.TestCase):
#     def setUp(self):
#         self.g4 = Gameinfo()
#         self.g4.playerlist.append(Player(self.g4, 'John', 100))  # john buys 100 percent of the time
#         self.g4.playerlist.append(Player(self.g4, 'Anna', 100))  # anna buys 100 percent of the time
#         self.p1 = self.g4.playerlist[0]
#         self.p2 = self.g4.playerlist[1]
#         self.p1.buy((self.g4, 1), 100)
#         self.p1.buy((self.g4, 1), 100)
#         self.p1.buy((self.g4, 3), 100)
#         self.p1.buy((self.g4, 4), 100)
#
#
#     def test_double_rent(self):
#         self.assertEqual(self.g4.how_much_rent(1, self.p2), (self.p1, 20))
#         self.assertEqual(self.g4.how_much_rent(3, self.p2), (self.p1, 8)) #only pay single
#         self.p1.buy((self.g4, 5), 100)  #till p1 buys all 3 properties
#         self.assertEqual(self.g4.how_much_rent(3, self.p2), (self.p1, 8)) #then the rent is doubled
#
# class RunGame(unittest.TestCase):
#     def setUp(self):
#         self.g5 = Gameinfo()
#         self.g5.playerlist.append(Player(self.g5, 'John', 100))  # john buys 100 percent of the time
#         self.g5.playerlist.append(Player(self.g5, 'Anna', 100))  # anna buys 100 percent of the time
#         self.p1 = self.g5.playerlist[0]
#         self.p2 = self.g5.playerlist[1]
#         self.g5.turn(self.p1)
#         # self.p1.buy((self.g5, 0),100)
#         # self.p2.buy((self.g5, 1),100)
#
#     def test_owned_properties_(self):
#         self.assertGreaterEqual(len(self.g5.owned_properties()), 1)
#
# class SellingProperties(unittest.TestCase):
#     def setUp(self):
#         self.g6 = Gameinfo()
#         self.g6.playerlist.append(Player(self.g6, 'John', 100))  # john buys 100 percent of the time
#         self.g6.playerlist.append(Player(self.g6, 'Anna', 100))  # anna buys 100 percent of the time
#         self.p1 = self.g6.playerlist[0]
#         self.p2 = self.g6.playerlist[1]
#
#     def test_sell_properties(self):
#         self.p1.buy((self.g6, 15), 100)
#         self.p1.buy((self.g6, 16), 100)
#         self.p1.buy((self.g6, 17), 100)
#         self.p1.buy((self.g6, 18), 100)
#         self.p1.buy((self.g6, 19), 100)
#         self.p1.buy((self.g6, 20), 100)
#         self.p1.buy((self.g6, 21), 100)
#         self.p1.buy((self.g6, 22), 100)
#         self.p1.buy((self.g6, 23), 100)
#         self.p1.buy((self.g6, 24), 100)
#         self.p1.buy((self.g6, 25), 100)
#         self.p1.buy((self.g6, 26), 100)
#         self.p1.buy((self.g6, 27), 100)
#         self.assertEqual(self.p1.money, 60)
#         self.assertSetEqual(set(self.g6.owned_properties()), set([33, 2, 4, 36, 7, 10, 21, 22, 23, 24, 30, 15, 16, 17, 18, 19, 20]))

# class test_stats(unittest.TestCase):
#     def setUp(self):
#         self.g7 = Gameinfo()
#         self.g7.playerlist.append(Player(self.g7, 'John', 100))  # john buys 100 percent of the time
#         self.g7.playerlist.append(Player(self.g7, 'Anna', 100))  # anna buys 100 percent of the time
#         self.p1 = self.g7.playerlist[0]
#         self.p2 = self.g7.playerlist[1]
#
#     def test_1buy(self):
#         self.p1.buy((self.g7, 1), 100)
#         self.p1.buy((self.g7, 1), 100)
#         #should have a property and a house.
#         self.assertSetEqual(self.p1.buying_property_history, set([1]))
#         np.testing.assert_array_equal(self.p1.buying_houses_history, np.array([ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
#         self.p1.buy((self.g7, 1), 100)
#         np.testing.assert_array_equal(self.p1.buying_houses_history, np.array([ 0.,  2.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
#         self.p1.buy((self.g7, 1), 100)
#         np.testing.assert_array_equal(self.p1.buying_houses_history, np.array([ 0.,  3.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
#         self.p1.buy((self.g7, 1), 100)
#         np.testing.assert_array_equal(self.p1.buying_houses_history, np.array([ 0.,  4.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
#         self.p1.buy((self.g7, 1), 100)
#         np.testing.assert_array_equal(self.p1.buying_houses_history, np.array([ 0.,  5.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
#         self.p1.buy((self.g7, 1), 100)
#         np.testing.assert_array_equal(self.p1.buying_houses_history, np.array([ 0.,  6.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#                                                                                 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]))
#
#
#
if __name__ == '__main__':
    unittest.main()
