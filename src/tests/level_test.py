import unittest
from unittest.mock import patch, MagicMock

from constants import TileType, InputAction, TEST_LEVEL_DATA, Settings
from scenes.level import Level
from game.level_data import LevelData


class TestLevel(unittest.TestCase):
    def setUp(self):
        patch_ui = patch("scenes.level.LevelUI")
        self.ui = patch_ui.start()
        self.addCleanup(patch_ui.stop)

        self.level = Level(LevelData(1, "potato", TEST_LEVEL_DATA))

        self.enemies = sum(row.count(TileType.ENEMY)
                           for row in TEST_LEVEL_DATA)
        self.blocks = sum(row.count(TileType.BLOCK) for row in TEST_LEVEL_DATA)
        self.placeable = sum(row.count(TileType.PLACEABLE)
                             for row in TEST_LEVEL_DATA)
        self.total_blocks = self.blocks + self.placeable
        self.world_objects = self.enemies + self.blocks + \
            self.placeable + 2  # player and end

        self.enemy_location = [(x, y) for y in range(len(TEST_LEVEL_DATA)) for x in range(
            len(TEST_LEVEL_DATA[0])) if TEST_LEVEL_DATA[y][x] == TileType.ENEMY]

        self.end_location = [(x, y) for y in range(len(TEST_LEVEL_DATA)) for x in range(
            len(TEST_LEVEL_DATA[0])) if TEST_LEVEL_DATA[y][x] == TileType.END]

        self.enemy_screen_location = [
            (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE) for x, y in self.enemy_location]

        self.end_screen_location = [
            (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE) for x, y in self.end_location]

        self.level.update(0.01, (0, 0))

    def test_init(self):
        self.assertEqual(self.level._level.id, 1)
        self.assertEqual(self.level._level.name, "potato")
        self.assertEqual(self.level._map._data, TEST_LEVEL_DATA)
        self.assertEqual(self.level._map._width, len(TEST_LEVEL_DATA[0]))
        self.assertEqual(self.level._map._height, len(TEST_LEVEL_DATA))
        self.assertIsNotNone(self.level._timer)

        self.assertIsNotNone(self.level._sprites.player)
        self.assertIsNotNone(self.level._sprites.end)
        self.assertIsNotNone(self.level._sprites.cursor)
        self.assertIsNotNone(self.level._sprites.blocks)
        self.assertIsNotNone(self.level._sprites.enemies)
        self.assertIsNotNone(self.level._sprites.world)

        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)

        self.assertEqual(len(self.level._sprites.world), self.world_objects)

        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_key(self):
        # timer is deactivated before first input_key is called
        self.assertEqual(self.level._timer._active, False)

        self.level.input_key(InputAction.LEFT)

        self.assertEqual(self.level._timer._active, True)
        self.assertEqual(self.level._sprites.player._body._input, [-1, 0])

        self.level.input_key(InputAction.RIGHT)
        self.level.input_key(InputAction.RIGHT)
        self.assertEqual(self.level._sprites.player._body._input, [1, 0])

        self.level.input_key(InputAction.JUMP)
        self.assertEqual(self.level._sprites.player._body._input, [1, -1])

        self.level.input_key(InputAction.DOWN)
        self.level.input_key(InputAction.DOWN)
        self.assertEqual(self.level._sprites.player._body._input, [1, 1])

    def test_input_mouse_add_placeable_valid(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable + 1)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.total_blocks + 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.world_objects + 1)
        self.assertEqual(self.level._sprites.player.charges, 2)

    def test_input_mouse_add_placeable_out_of_bounds(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (-1, -1))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_add_placeable_out_of_range(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (256, 256))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_add_placeable_occupied(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (1, 1))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_add_placeable_no_charges(self):
        self.level._sprites.player.charges = 0
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)
        self.assertEqual(self.level._sprites.player.charges, 0)

    def test_input_mouse_add_placeable_duplicate_placement(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable + 1)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.total_blocks + 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.world_objects + 1)

    def test_input_mouse_remove_placeable_valid(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.level.input_mouse(InputAction.MOUSE_RIGHT, (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)
        self.assertEqual(self.level._sprites.player.charges, 3)

    def test_input_mouse_remove_placeable_out_of_range(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.level._sprites.player.rect.x = 256
        self.level._sprites.player.rect.y = 256
        self.level.input_mouse(InputAction.MOUSE_RIGHT, (256, 256))
        self.assertEqual(len(self.level._map_objects), self.placeable + 1)
        self.assertEqual(len(self.level._sprites.blocks),
                         self.total_blocks + 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.world_objects + 1)
        self.assertEqual(self.level._sprites.player.charges, 2)

    def test_input_mouse_remove_placeable_duplicate_removal(self):
        self.level.input_mouse(InputAction.MOUSE_LEFT, (80, 80))
        self.level.input_mouse(InputAction.MOUSE_RIGHT, (80, 80))
        self.level.input_mouse(InputAction.MOUSE_RIGHT, (80, 80))
        self.assertEqual(len(self.level._map_objects), self.placeable)
        self.assertEqual(len(self.level._sprites.blocks), self.total_blocks)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)
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
        self.assertEqual(len(self.level._sprites.world), self.world_objects)

        # right horizontal limit
        enemy.rect.x = 1500
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies - 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.world_objects - 1)

    def test_check_entities_in_bounds_enemy_vertical(self):
        enemy = self.level._sprites.enemies.sprites()[0]

        enemy.rect.x = 0
        enemy.rect.y = 0
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)

        # out of bounds above is fine
        enemy.rect.y = -400
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies)
        self.assertEqual(len(self.level._sprites.world), self.world_objects)

        # below limit
        enemy.rect.y = 1500
        self.level._check_entities_in_bounds()
        self.assertEqual(len(self.level._sprites.enemies), self.enemies - 1)
        self.assertEqual(len(self.level._sprites.world),
                         self.world_objects - 1)
