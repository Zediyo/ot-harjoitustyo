from map import Map
import unittest

class TestMap(unittest.TestCase):
    def setUp(self):
        self.width = 20
        self.height = 10
        
        #wall of 1s around empty map of 0s
        self.map_data = [[0] * self.width for _ in range(self.height)]
        for i in range(self.width):
            self.map_data[0][i] = 1
            self.map_data[self.height - 1][i] = 1
        for i in range(self.height):
            self.map_data[i][0] = 1
            self.map_data[i][self.width - 1] = 1

        self.map = Map(self.map_data)

    def test_init(self):
        self.assertEqual(self.map.height, self.height)
        self.assertEqual(self.map.width, self.width)
        self.assertEqual(self.map.data, self.map_data)

    def test_point_in_bounds_inside(self):
        self.assertTrue(self.map.point_in_bounds(5, 5))
        self.assertTrue(self.map.point_in_bounds(18, 8))
        self.assertTrue(self.map.point_in_bounds(11, 3))

    def test_point_in_bounds_edge(self):
        self.assertTrue(self.map.point_in_bounds(0, 0))
        self.assertTrue(self.map.point_in_bounds(19, 9))
        self.assertTrue(self.map.point_in_bounds(19, 0))
        self.assertTrue(self.map.point_in_bounds(0, 9))

    def test_point_in_bounds_outside(self):
        self.assertFalse(self.map.point_in_bounds(-1, 5))
        self.assertFalse(self.map.point_in_bounds(5, -1))
        self.assertFalse(self.map.point_in_bounds(20, 5))
        self.assertFalse(self.map.point_in_bounds(5, 10))

