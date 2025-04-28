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
        self.assertEqual(self.map._height, self.height)
        self.assertEqual(self.map._width, self.width)
        self.assertEqual(self.map._data, self.map_data)

    def test_point_in_bounds_inside(self):
        self.assertTrue(self.map.cell_in_bounds(5, 5))
        self.assertTrue(self.map.cell_in_bounds(18, 8))
        self.assertTrue(self.map.cell_in_bounds(11, 3))

    def test_point_in_bounds_edge(self):
        self.assertTrue(self.map.cell_in_bounds(0, 0))
        self.assertTrue(self.map.cell_in_bounds(19, 9))
        self.assertTrue(self.map.cell_in_bounds(19, 0))
        self.assertTrue(self.map.cell_in_bounds(0, 9))

    def test_point_in_bounds_outside(self):
        self.assertFalse(self.map.cell_in_bounds(-1, 5))
        self.assertFalse(self.map.cell_in_bounds(5, -1))
        self.assertFalse(self.map.cell_in_bounds(20, 5))
        self.assertFalse(self.map.cell_in_bounds(5, 10))

    def test_snap_to_grid(self):
        test_pos = (1627, 3243)
        expected_pos = (1627 // self.test_tilesize * self.test_tilesize,
                        3243 // self.test_tilesize * self.test_tilesize)
        self.assertEqual(self.map.snap_to_grid(test_pos), expected_pos)

    def test_screen_to_cell_index(self):
        test_pos = (1627, 3243)
        expected_pos = (1627 // self.test_tilesize, 3243 // self.test_tilesize)
        self.assertEqual(self.map.screen_to_cell_index(test_pos), expected_pos)

    def test_cell_index_to_world_pos(self):
        test_pos = (5, 5)
        expected_pos = (5 * self.test_tilesize, 5 * self.test_tilesize)
        self.assertEqual(self.map.cell_index_to_world_pos(
            test_pos), expected_pos)

    def test_expand_map(self):
        screen_w = 1400
        screen_h = 1600
        old_map_data = self.map._data.copy()
        old_width = self.map._width
        old_height = self.map._height

        self.map.expand_map(screen_w, screen_h)

        new_width = screen_w // self.test_tilesize
        new_height = screen_h // self.test_tilesize

        offset_x = (new_width - self.width) // 2
        offset_y = (new_height - self.height) // 2

        self.assertEqual(self.map._width, new_width)
        self.assertEqual(self.map._height, new_height)
        self.assertNotEqual(self.map._data, old_map_data)
        self.assertNotEqual(self.map._width, old_width)
        self.assertNotEqual(self.map._height, old_height)

        # check if new map data is correct (0s in the new area)
        for y in range(new_height):
            for x in range(new_width):
                if x < offset_x or x >= offset_x + old_width or y < offset_y or y >= offset_y + old_height:
                    self.assertEqual(self.map._data[y][x], 0)
                else:
                    self.assertEqual(
                        self.map._data[y][x], old_map_data[y - offset_y][x - offset_x])

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

        self.assertEqual(test_map._width, start_width)
        self.assertEqual(test_map._height, start_height)

        test_map.shrink_map()

        self.assertEqual(test_map._width, start_width - 6)
        self.assertEqual(test_map._height, start_height - 6)

        # should only have 1s left
        for y in range(test_map._height):
            for x in range(test_map._width):
                self.assertEqual(test_map._data[y][x], 1)

    def test_single_cell_operations(self):
        # test insert + get
        self.assertTrue(self.map.set_tile_at_cell(5, 5, 2))
        self.assertEqual(self.map.get_tile_at_cell(5, 5), 2)

        # test remove + get
        self.assertTrue(self.map.set_tile_at_cell(5, 5, 0))
        self.assertEqual(self.map.get_tile_at_cell(5, 5), 0)

    def test_invalid_single_cell_operations(self):
        start_map_data = self.map._data.copy()

        # test invalid insert (out of bounds)
        self.assertFalse(self.map.set_tile_at_cell(-1, -1, 2))
        self.assertFalse(self.map.set_tile_at_cell(
            self.width + 1, self.height + 1, 2))

        # test invalid remove (out of bounds)
        self.assertFalse(self.map.set_tile_at_cell(-1, -1, 0))
        self.assertFalse(self.map.set_tile_at_cell(
            self.width + 1, self.height + 1, 0))

        # test invalid get (out of bounds)
        self.assertIsNone(self.map.get_tile_at_cell(-1, 0))
        self.assertIsNone(self.map.get_tile_at_cell(0, -1))
        self.assertIsNone(self.map.get_tile_at_cell(-1, -1))
        self.assertIsNone(self.map.get_tile_at_cell(
            self.width + 1, self.height + 1))

        # map should not have changed
        self.assertEqual(self.map._data, start_map_data)

    def test_map_validity_checks(self):
        self.assertFalse(self.map.is_map_viable())
        self.assertFalse(self.map.contains_tile(constants.TILE_SPAWN))
        self.map.set_tile_at_cell(5, 5, constants.TILE_SPAWN)
        self.assertTrue(self.map.contains_tile(constants.TILE_SPAWN))

        self.assertFalse(self.map.is_map_viable())
        self.assertFalse(self.map.contains_tile(constants.TILE_END))
        self.map.set_tile_at_cell(10, 5, constants.TILE_END)
        self.assertTrue(self.map.contains_tile(constants.TILE_END))

        self.assertTrue(self.map.is_map_viable())
        self.map.set_tile_at_cell(10, 5, 0)
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
                self.assertTrue(self.map.is_area_in_bounds(
                    start_x, start_y, depth))

                # test start condition + add area
                self.assertTrue(self.map.is_empty_area(
                    start_x, start_y, depth))
                self.assertTrue(self.map.add_multi_tile(
                    start_x, start_y, tile, depth))
                self.assertFalse(self.map.is_empty_area(
                    start_x, start_y, depth))

                # test each cell in the area is correct + corner finding
                for i in range(depth[1]):
                    for j in range(depth[0]):
                        if i == 0 and j == 0:  # top left corner is positive
                            self.assertEqual(self.map.get_tile_at_cell(
                                start_x + j, start_y + i), tile)
                            self.assertEqual(self.map.find_nearest_tile_corner(
                                start_x + j, start_y + i, tile, depth), (start_x, start_y))
                        else:  # rest of the connected cells are negative
                            self.assertEqual(self.map.get_tile_at_cell(
                                start_x + j, start_y + i), -tile)
                            self.assertEqual(self.map.find_nearest_tile_corner(
                                start_x + j, start_y + i, -tile, depth), (start_x, start_y))

                # test removing the area
                self.assertTrue(self.map.remove_multi_tile(
                    start_x, start_y, depth))
                self.assertTrue(self.map.is_empty_area(
                    start_x, start_y, depth))

    def test_invalid_map_area_operations(self):
        start_map_data = self.map._data.copy()

        # test invalid area in bounds (out of bounds)
        self.assertFalse(self.map.is_area_in_bounds(-1, -1, (2, 2)))
        self.assertFalse(self.map.is_area_in_bounds(
            0, 0, (self.width + 1, self.height + 1)))

        # test invalid corner finding (not able to find and going out of bounds)
        self.assertIsNone(
            self.map.find_nearest_tile_corner(4, 4, -2, (10, 10)))

        # test invalid add tile (not enough space)
        self.assertFalse(self.map.add_multi_tile(
            2, 2, 2, (self.width, self.height)))

        # test invalid remove tile (out of bounds)
        self.assertFalse(self.map.remove_multi_tile(-1, -1, (2, 2)))
        self.assertFalse(self.map.remove_multi_tile(
            0, 0, (self.width + 1, self.height + 1)))

        # map should not have changed
        self.assertEqual(self.map._data, start_map_data)
