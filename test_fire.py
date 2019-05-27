import unittest

import fire_lib

class MainTests(unittest.TestCase):
    def testDist(self):
        print "testing dist"
        self.assertEqual(1, fire_lib.dist(0,0,1,0))
        self.assertEqual(3, fire_lib.dist(0,0,1,2))
        self.assertEqual(3, fire_lib.dist(5,0,6,2))
        self.assertEqual(4, fire_lib.dist(10,10,8,8))
        self.assertEqual(10, fire_lib.dist(10,0,8,8))

    def testPickTop(self):
        choices = ['A', 'B', 'C']
        values = [3,2,1]

        self.assertEqual('A', fire_lib.pick_top(choices, values))
        values = [2,1,3]
        self.assertEqual('C', fire_lib.pick_top(choices, values))
        values = [2,3,3]
        self.assertEqual('B', fire_lib.pick_top(choices, values))
        
    def testPickSpot(self):
        troops = []
        spot_list = []
        self.assertEqual((-1,-1), fire_lib.pick_spot(troops, spot_list))
        spot_list.append((2,2))
        self.assertEqual((2,2), fire_lib.pick_spot(troops, spot_list))
        spot_list = [(3,4), (1,1), (2,3)]
        fire_lib.randomizer = lambda lst: lst[0]
        self.assertEqual((3,4), fire_lib.pick_spot(troops, spot_list))
    
        troops.append((1, 1, 1, 0, 10, 10))
        troops.append((1, 1, 1, 0, 3, 4))
        self.assertEqual((1,1), fire_lib.pick_spot(troops, spot_list))
    
        troops.append((1, 1, 1, 0, 1, 1))
        self.assertEqual((2,3), fire_lib.pick_spot(troops, spot_list))
    
    def testValidMove(self):
        board = []
        board.append(list("............."))
        board.append(list(".#..........."))
        board.append(list("..H.........."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))

        self.assertEqual(True, fire_lib.valid_move(board, 0, 0))
        self.assertEqual(True, fire_lib.valid_move(board, 10, 0))
        self.assertEqual(False, fire_lib.valid_move(board, 12, 0))
        self.assertEqual(False, fire_lib.valid_move(board, 10, -10))
        self.assertEqual(False, fire_lib.valid_move(board, 1, 1))
        self.assertEqual(False, fire_lib.valid_move(board, 2, 2))

    def testListOwnedSpots(self):

        board = []
        board.append(list("OOO.........."))
        board.append(list(".#O.........."))
        board.append(list("..H.........."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))

        self.assertEqual([(0,0), (1,0), (2,0), (2, 1), (2,2)], 
                fire_lib.list_owned_spots(board))

    def testListNotOwnedSpots(self):
        board = []
        board.append(list("OOO.........."))
        board.append(list(".#O.........."))
        board.append(list("..H.........."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))

        self.assertEqual(12*12-6, len(fire_lib.list_not_owned_spots(board)))

    def testListOwnedAdjSpots(self):
        board = []
        board.append(list("OOO.........."))
        board.append(list(".#O.........."))
        board.append(list("..H.........."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))
        board.append(list("............."))

        expected = [(3,0), (0,1), (3, 1), (1,2), (3,2), (2, 3)]
        self.assertEqual(expected, fire_lib.list_owned_adj_spots(board))

    def testFindClosesSpot(self):
        x,y = 2,2
        spots = [(10,5), (5,7)]
        self.assertEqual((5,7), fire_lib.find_closest_spot(x, y, spots))


if __name__ == '__main__':
    unittest.main()