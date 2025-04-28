import unittest
from unittest.mock import patch, MagicMock
import constants

from scenes.level import Level


class TestLevel(unittest.TestCase):
    def setUp(self):
        patch_ui = patch("scenes.level.LevelUI")
        self.ui = patch_ui.start()
        self.addCleanup(patch_ui.stop)

        self.data = constants.TEST_LEVEL
        self.level = Level({"id": "1", "name": "potato", "data": self.data})

        self.enemies = sum(row.count(constants.TILE_ENEMY)
                           for row in self.data)
        self.blocks = sum(row.count(constants.TILE_BLOCK) for row in self.data)
        self.placeable = sum(row.count(constants.TILE_PLACEABLE)
                             for row in self.data)

        self.enemy_location = [(x, y) for y in range(len(self.data)) for x in range(
            len(self.data[0])) if self.data[y][x] == constants.TILE_ENEMY]
        self.end_location = [(x, y) for y in range(len(self.data)) for x in range(
            len(self.data[0])) if self.data[y][x] == constants.TILE_END]
        self.enemy_screen_location = [
            (x * constants.TILE_SIZE, y * constants.TILE_SIZE) for x, y in self.enemy_location]
        self.end_screen_location = [
            (x * constants.TILE_SIZE, y * constants.TILE_SIZE) for x, y in self.end_location]

        self.level.update(0.01, (0, 0))

    def test_init(self):
        self.assertEqual(self.level.level["id"], "1")
        self.assertEqual(self.level.level["name"], "potato")
        self.assertEqual(self.level._map._data, self.data)
        self.assertEqual(self.level._map._width, len(self.data[0]))
        self.assertEqual(self.level._map._height, len(self.data))
        self.assertIsNotNone(self.level._timer)

        self.assertIsNotNone(self.level._sprites.player)
        self.assertIsNotNone(self.level._sprites.end)
        self.assertIsNotNone(self.level._sprites.cursor)
        self.assertIsNotNone(self.level._sprites.blocks)
        self.assertIsNotNone(self.level._sprites.enemies)
        self.assertIsNotNone(self.level._sprites.world)

        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)

        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)

        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_key(self):
        # timer is deactivated before first input_key is called
        self.assertEqual(self.level._timer._active, False)

        self.level.input_key("left")

        self.assertEqual(self.level._timer._active, True)
        self.assertEqual(self.level._sprites.player.body._input, [-1, 0])

        self.level.input_key("right")
        self.level.input_key("right")
        self.assertEqual(self.level._sprites.player.body._input, [1, 0])

        self.level.input_key("jump")
        self.assertEqual(self.level._sprites.player.body._input, [1, -1])

        self.level.input_key("down")
        self.level.input_key("down")
        self.assertEqual(self.level._sprites.player.body._input, [1, 1])

    def test_input_mouse_add_placeable_valid(self):
        self.level.input_mouse("left", (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable + 1)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable + 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 3)
        self.assertEqual(self.level._sprites.player.charges, 2)

    def test_input_mouse_add_placeable_out_of_bounds(self):
        self.level.input_mouse("left", (-1, -1))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_add_placeable_out_of_range(self):
        self.level.input_mouse("left", (256, 256))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_add_placeable_occupied(self):
        self.level.input_mouse("left", (1, 1))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_add_placeable_no_charges(self):
        self.level._sprites.player.charges = 0
        self.level.input_mouse("left", (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)
        self.assertEqual(self.level._sprites.player.charges, 0)

    def test_input_mouse_add_placeable_duplicate_placement(self):
        self.level.input_mouse("left", (80, 80))
        self.level.input_mouse("left", (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable + 1)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable + 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 3)

    def test_input_mouse_remove_placeable_valid(self):
        self.level.input_mouse("left", (80, 80))
        self.level.input_mouse("right", (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_remove_placeable_out_of_range(self):
        self.level.input_mouse("left", (80, 80))
        self.level._sprites.player.rect.x = 256
        self.level._sprites.player.rect.y = 256
        self.level.input_mouse("right", (256, 256))
        self.assertEqual(len(self.level._map_objects), self.placeable + 1)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable + 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 3)
        self.assertEqual(self.level._sprites.player.charges, 2)

    def test_input_mouse_remove_placeable_duplicate_removal(self):
        self.level.input_mouse("left", (80, 80))
        self.level.input_mouse("right", (80, 80))
        self.level.input_mouse("right", (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.blocks + self.placeable)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_check_enemy_collisions(self):
        self.assertEqual(self.level.is_done(), False)
        self.level._check_enemy_collisions()
        self.assertEqual(self.level.is_done(), False)

        self.level._sprites.player.rect.x = self.enemy_screen_location[0][0]
        self.level._sprites.player.rect.y = self.enemy_screen_location[0][1]
        self.level._check_enemy_collisions()
        self.assertEqual(self.level.is_done(), True)

    def test_check_end_collisions(self):
        self.assertEqual(self.level.is_done(), False)
        self.level._check_end_collisions()
        self.assertEqual(self.level.is_done(), False)

        self.level._sprites.player.rect.x = self.end_screen_location[0][0]
        self.level._sprites.player.rect.y = self.end_screen_location[0][1]
        self.level._check_end_collisions()
        self.assertEqual(self.level.is_done(), True)

    def test_check_entities_in_bounds_player_horizontal(self):
        self.assertEqual(self.level.is_done(), False)

        self.level._sprites.player.rect.x = 0
        self.level._sprites.player.rect.y = 0
        self.level._check_entities_in_bounds()
        self.assertEqual(self.level.is_done(), False)

        # left horizontal limit
        self.level._sprites.player.rect.x = -40
        self.level._check_entities_in_bounds()
        self.assertEqual(self.level.is_done(), True)

    def test_check_entities_in_bounds_enemy_horizontal(self):
        enemy = self.level._sprites.enemies.sprites()[0]

        enemy.rect.x = 0
        enemy.rect.y = 0
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)

        # right horizontal limit
        enemy.rect.x = 1500
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies - 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 1)

    def test_check_entities_in_bounds_enemy_vertical(self):
        enemy = self.level._sprites.enemies.sprites()[0]

        enemy.rect.x = 0
        enemy.rect.y = 0
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)

        # out of bounds above is fine
        enemy.rect.y = -400
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 2)

        # below limit
        enemy.rect.y = 1500
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies - 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.enemies + self.blocks + self.placeable + 1)
