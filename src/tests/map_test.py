from game.map import Map
import unittest

import constants


class TestMap(unittest.TestCase):
    def setUp(self):
        self.width = 20
        self.height = 10
        self.test_tilesize = 28  # default is 16

        # wall of 1s around empty map of 0s
        self.map_data = [[0] * self.width for _ in range(self.height)]
        for i in range(self.width):
            self.map_data[0][i] = 1
            self.map_data[self.height - 1][i] = 1
        for i in range(self.height):
            self.map_data[i][0] = 1
            self.map_data[i][self.width - 1] = 1

        self.map = Map(self.map_data, self.test_tilesize)

    def test_init(self):
        self.assertEqual(self.map.height, self.height)
        self.assertEqual(self.map.width, self.width)
        self.assertEqual(self.map.data, self.map_data)

    def test_point_in_bounds_inside(self):
        self.assertTrue(self.map.cell_in_bounds(5, 5))
        self.assertTrue(self.map.cell_in_bounds(18, 8))
        self.assertTrue(self.map.cell_in_bounds(11, 3))

        self.assertTrue(self.map.tile_in_bounds(
            5 * self.test_tilesize, 5 * self.test_tilesize))
        self.assertTrue(self.map.tile_in_bounds(
            18 * self.test_tilesize, 8 * self.test_tilesize))
        self.assertTrue(self.map.tile_in_bounds(
            11 * self.test_tilesize, 3 * self.test_tilesize))

    def test_point_in_bounds_edge(self):
        self.assertTrue(self.map.cell_in_bounds(0, 0))
        self.assertTrue(self.map.cell_in_bounds(19, 9))
        self.assertTrue(self.map.cell_in_bounds(19, 0))
        self.assertTrue(self.map.cell_in_bounds(0, 9))

        self.assertTrue(self.map.tile_in_bounds(0, 0))
        self.assertTrue(self.map.tile_in_bounds(
            19 * self.test_tilesize, 9 * self.test_tilesize))
        self.assertTrue(self.map.tile_in_bounds(19 * self.test_tilesize, 0))
        self.assertTrue(self.map.tile_in_bounds(0, 9 * self.test_tilesize))

    def test_point_in_bounds_outside(self):
        self.assertFalse(self.map.cell_in_bounds(-1, 5))
        self.assertFalse(self.map.cell_in_bounds(5, -1))
        self.assertFalse(self.map.cell_in_bounds(20, 5))
        self.assertFalse(self.map.cell_in_bounds(5, 10))

        self.assertFalse(self.map.tile_in_bounds(-1 *
                         self.test_tilesize, 5 * self.test_tilesize))
        self.assertFalse(self.map.tile_in_bounds(
            5 * self.test_tilesize, -1 * self.test_tilesize))
        self.assertFalse(self.map.tile_in_bounds(
            20 * self.test_tilesize, 5 * self.test_tilesize))
        self.assertFalse(self.map.tile_in_bounds(
            5 * self.test_tilesize, 10 * self.test_tilesize))

    def test_screen_pos_to_grid(self):
        test_pos = (1627, 3243)
        expected_pos = (1627 // self.test_tilesize * self.test_tilesize,
                        3243 // self.test_tilesize * self.test_tilesize)
        self.assertEqual(self.map.screen_pos_to_grid(test_pos), expected_pos)

    def test_screen_pos_to_cell(self):
        test_pos = (1627, 3243)
        expected_pos = (1627 // self.test_tilesize, 3243 // self.test_tilesize)
        self.assertEqual(self.map.screen_pos_to_cell(test_pos), expected_pos)

    def test_cell_pos_to_grid(self):
        test_pos = (5, 5)
        expected_pos = (5 * self.test_tilesize, 5 * self.test_tilesize)
        self.assertEqual(self.map.cell_pos_to_grid(test_pos), expected_pos)

    def test_expand_map(self):
        screen_w = 1400
        screen_h = 1600
        old_map_data = self.map.data.copy()
        old_width = self.map.width
        old_height = self.map.height

        self.map.expand_map(screen_w, screen_h)

        new_width = screen_w // self.test_tilesize
        new_height = screen_h // self.test_tilesize

        offset_x = (new_width - self.width) // 2
        offset_y = (new_height - self.height) // 2

        self.assertEqual(self.map.width, new_width)
        self.assertEqual(self.map.height, new_height)
        self.assertNotEqual(self.map.data, old_map_data)
        self.assertNotEqual(self.map.width, old_width)
        self.assertNotEqual(self.map.height, old_height)

        # check if new map data is correct (0s in the new area)
        for y in range(new_height):
            for x in range(new_width):
                if x < offset_x or x >= offset_x + old_width or y < offset_y or y >= offset_y + old_height:
                    self.assertEqual(self.map.data[y][x], 0)
                else:
                    self.assertEqual(
                        self.map.data[y][x], old_map_data[y - offset_y][x - offset_x])

    def test_shrink_map(self):
        # map of 1's with wall of 3 0's around it
        start_width = 30
        start_height = 40
        map_data = [[1] * start_width for _ in range(start_height)]
        for x in range(start_width):
            for y in range(3):
                map_data[y][x] = 0
                map_data[-y-1][x] = 0

        for y in range(start_height):
            for x in range(3):
                map_data[y][x] = 0
                map_data[y][-x-1] = 0

        test_map = Map(map_data, self.test_tilesize)

        self.assertEqual(test_map.width, start_width)
        self.assertEqual(test_map.height, start_height)

        test_map.shrink_map()

        self.assertEqual(test_map.width, start_width - 6)
        self.assertEqual(test_map.height, start_height - 6)

        # should only have 1s left
        for y in range(test_map.height):
            for x in range(test_map.width):
                self.assertEqual(test_map.data[y][x], 1)

    def test_single_cell_operations(self):
        # test insert + get
        self.assertTrue(self.map.insert_cell(5, 5, 2))
        self.assertEqual(self.map.get_cell(5, 5), 2)

        # test remove + get
        self.assertTrue(self.map.remove_cell(5, 5))
        self.assertEqual(self.map.get_cell(5, 5), 0)

    def test_invalid_single_cell_operations(self):
        start_map_data = self.map.data.copy()

        # test invalid insert (out of bounds)
        self.assertFalse(self.map.insert_cell(-1, -1, 2))
        self.assertFalse(self.map.insert_cell(
            self.width + 1, self.height + 1, 2))

        # test invalid remove (out of bounds)
        self.assertFalse(self.map.remove_cell(-1, -1))
        self.assertFalse(self.map.remove_cell(self.width + 1, self.height + 1))

        # test invalid get (out of bounds)
        self.assertIsNone(self.map.get_cell(-1, 0))
        self.assertIsNone(self.map.get_cell(0, -1))
        self.assertIsNone(self.map.get_cell(-1, -1))
        self.assertIsNone(self.map.get_cell(self.width + 1, self.height + 1))

        # map should not have changed
        self.assertEqual(self.map.data, start_map_data)

    def test_map_validity_operations(self):
        # test invalid map -> no spawn -> yes spawn
        self.assertFalse(self.map.is_map_viable())
        self.assertFalse(self.map.has_spawn())
        self.map.insert_cell(5, 5, constants.TILE_SPAWN)
        self.assertTrue(self.map.has_spawn())

        # test invalid map -> no end -> yes end -> map valid (spawn + end)
        self.assertFalse(self.map.is_map_viable())
        self.assertFalse(self.map.has_end())
        self.map.insert_cell(10, 5, constants.TILE_END)
        self.assertTrue(self.map.has_end())

        self.assertTrue(self.map.is_map_viable())
        self.map.remove_cell(10, 5)
        self.assertFalse(self.map.is_map_viable())

    def test_map_area_operations(self):
        tile = 2
        start_x = 5
        start_y = 5
        # all operations combinations from 1x1 to 4x4
        for y in range(4):
            for x in range(4):
                depth = (x+1, y+1)

                # test area in bounds
                self.assertTrue(self.map.area_in_bounds(
                    start_x, start_y, depth))

                # test start condition + add area
                self.assertTrue(self.map.has_empty_area(
                    start_x, start_y, depth))
                self.assertTrue(self.map.add_tile(
                    start_x, start_y, tile, depth))
                self.assertFalse(self.map.has_empty_area(
                    start_x, start_y, depth))

                # test each cell in the area is correct + corner finding
                for i in range(depth[1]):
                    for j in range(depth[0]):
                        if i == 0 and j == 0:  # top left corner is positive
                            self.assertEqual(self.map.get_cell(
                                start_x + j, start_y + i), tile)
                            self.assertEqual(self.map.find_nearest_corner(
                                start_x + j, start_y + i, tile, depth), (start_x, start_y))
                        else:  # rest of the connected cells are negative
                            self.assertEqual(self.map.get_cell(
                                start_x + j, start_y + i), -tile)
                            self.assertEqual(self.map.find_nearest_corner(
                                start_x + j, start_y + i, -tile, depth), (start_x, start_y))

                # test removing the area
                self.assertTrue(self.map.remove_tile(start_x, start_y, depth))
                self.assertTrue(self.map.has_empty_area(
                    start_x, start_y, depth))

    def test_invalid_map_area_operations(self):
        start_map_data = self.map.data.copy()

        # test invalid area in bounds (out of bounds)
        self.assertFalse(self.map.area_in_bounds(-1, -1, (2, 2)))
        self.assertFalse(self.map.area_in_bounds(
            0, 0, (self.width + 1, self.height + 1)))

        # test invalid corner finding (not able to find and going out of bounds)
        self.assertIsNone(self.map.find_nearest_corner(4, 4, -2, (10, 10)))

        # test invalid add tile (not enough space)
        self.assertFalse(self.map.add_tile(2, 2, 2, (self.width, self.height)))

        # test invalid remove tile (out of bounds)
        self.assertFalse(self.map.remove_tile(-1, -1, (2, 2)))
        self.assertFalse(self.map.remove_tile(
            0, 0, (self.width + 1, self.height + 1)))

        # map should not have changed
        self.assertEqual(self.map.data, start_map_data)
