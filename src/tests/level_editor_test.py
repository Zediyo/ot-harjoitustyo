import unittest
from unittest.mock import patch, MagicMock

import pygame
from constants import TEST_LEVEL_DATA, TileType, Settings, InputAction
from scenes.level_editor import LevelEditor
from game.level_data import LevelData


class TestLevelEditor(unittest.TestCase):
    def setUp(self):
        patch_ui = patch("scenes.level_editor.EditorUI")
        patch_preview = patch("scenes.level_editor.generate_level_preview")
        self.ui = patch_ui.start()
        self.preview = patch_preview.start()
        self.addCleanup(patch_ui.stop)
        self.addCleanup(patch_preview.stop)

        ui_instance = self.ui.return_value
        ui_instance.is_save_clicked.return_value = False

        self.data = TEST_LEVEL_DATA
        self.editor = LevelEditor(LevelData(1, "potato", TEST_LEVEL_DATA))

        data = self.editor._map._data

        self.spawn_location = [(x, y) for y in range(len(data)) for x in range(
            len(data[0])) if data[y][x] == TileType.SPAWN]

        self.end_location = [(x, y) for y in range(len(data)) for x in range(
            len(data[0])) if data[y][x] == TileType.END]

        self.spawn_screen_location = [
            (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE) for x, y in self.spawn_location]

        self.end_screen_location = [
            (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE) for x, y in self.end_location]

        self.editor.update(0.01, (0, 0))
        self.editor._hand = TileType.BLOCK

    def test_init(self):
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

    def test_input_remove_and_add_end(self):
        # cant add end (already exists)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_5)])
        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertNotEqual(
            self.editor._map.get_tile_at_cell(4, 4), TileType.END)

        self.editor.input_mouse_hold(
            InputAction.MOUSE_RIGHT, self.end_screen_location[0])
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": False})

        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), TileType.END)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

    def test_input_remove_and_add_spawn(self):

        # cant add spawn (already exists)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_4)])
        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertNotEqual(
            self.editor._map.get_tile_at_cell(4, 4), TileType.SPAWN)

        self.editor.input_mouse_hold(
            InputAction.MOUSE_RIGHT, self.spawn_screen_location[0])
        self.assertEqual(self.editor._has_required, {
                         "spawn": False, "end": True})

        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(
            self.editor._map.get_tile_at_cell(4, 4), TileType.SPAWN)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

    def test_input_add_and_remove_enemy(self):
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_3)])

        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(
            self.editor._map.get_tile_at_cell(4, 4), TileType.ENEMY)

        self.editor.input_mouse_hold(
            InputAction.MOUSE_RIGHT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), 0)

    def test_input_add_and_remove_placeable(self):
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)])

        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            4, 4), TileType.PLACEABLE)

        self.editor.input_mouse_hold(
            InputAction.MOUSE_RIGHT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), 0)

    def test_input_add_and_remove_block(self):
        # cant add block on top of spawn
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)])

        (screen_x, screen_y) = self.spawn_screen_location[0]
        (x, y) = self.spawn_location[0]

        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (screen_x, screen_y))
        self.assertEqual(
            self.editor._map.get_tile_at_cell(x, y), TileType.SPAWN)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

        self.editor.input_mouse_hold(
            InputAction.MOUSE_LEFT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(
            self.editor._map.get_tile_at_cell(4, 4), TileType.BLOCK)

        self.editor.input_mouse_hold(
            InputAction.MOUSE_RIGHT, (4 * Settings.TILE_SIZE, 4 * Settings.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), 0)

    def test_remove_large_tile(self):
        # remove spawn (2x2) tile
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

        (screen_x, screen_y) = self.spawn_screen_location[0]
        screen_x += Settings.TILE_SIZE + 1
        screen_y += Settings.TILE_SIZE + 1

        (x, y) = self.spawn_location[0]

        self.editor.input_mouse_hold(
            InputAction.MOUSE_RIGHT, (screen_x, screen_y))

        self.assertEqual(self.editor._map.get_tile_at_cell(x + 1, y + 1), 0)
        self.assertEqual(self.editor._has_required, {
                         "spawn": False, "end": True})
