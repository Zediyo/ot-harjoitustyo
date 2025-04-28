import unittest
from unittest.mock import patch, MagicMock
import constants
import pygame

from scenes.level_editor import LevelEditor


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

        self.data = constants.TEST_LEVEL
        self.editor = LevelEditor(
            {"id": "1", "name": "potato", "data": self.data})

        data = self.editor._map._data

        self.spawn_location = [(x, y) for y in range(len(data)) for x in range(
            len(data[0])) if data[y][x] == constants.TILE_SPAWN]
        self.end_location = [(x, y) for y in range(len(data)) for x in range(
            len(data[0])) if data[y][x] == constants.TILE_END]
        self.spawn_screen_location = [
            (x * constants.TILE_SIZE, y * constants.TILE_SIZE) for x, y in self.spawn_location]
        self.end_screen_location = [
            (x * constants.TILE_SIZE, y * constants.TILE_SIZE) for x, y in self.end_location]

        self.editor.update(0.01, (0, 0))
        self.editor._hand = 1

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
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertNotEqual(
            self.editor._map.get_tile_at_cell(4, 4), constants.TILE_END)

        self.editor.input_mouse_hold("right", self.end_screen_location[0])
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": False})

        self.editor.input_mouse_hold(
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            4, 4), constants.TILE_END)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

    def test_input_remove_and_add_spawn(self):

        # cant add spawn (already exists)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_4)])
        self.editor.input_mouse_hold(
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertNotEqual(self.editor._map.get_tile_at_cell(
            4, 4), constants.TILE_SPAWN)

        self.editor.input_mouse_hold("right", self.spawn_screen_location[0])
        self.assertEqual(self.editor._has_required, {
                         "spawn": False, "end": True})

        self.editor.input_mouse_hold(
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            4, 4), constants.TILE_SPAWN)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

    def test_input_add_and_remove_enemy(self):
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_3)])
        self.editor.input_mouse_hold(
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            4, 4), constants.TILE_ENEMY)

        self.editor.input_mouse_hold(
            "right", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), 0)

    def test_input_add_and_remove_placeable(self):
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)])
        self.editor.input_mouse_hold(
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            4, 4), constants.TILE_PLACEABLE)

        self.editor.input_mouse_hold(
            "right", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), 0)

    def test_input_add_and_remove_block(self):
        # cant add block on top of spawn
        self.editor.input_raw(
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)])
        (screen_x, screen_y) = self.spawn_screen_location[0]
        (x, y) = self.spawn_location[0]
        self.editor.input_mouse_hold("left", (screen_x, screen_y))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            x, y), constants.TILE_SPAWN)
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

        self.editor.input_mouse_hold(
            "left", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(
            4, 4), constants.TILE_BLOCK)

        self.editor.input_mouse_hold(
            "right", (4 * constants.TILE_SIZE, 4 * constants.TILE_SIZE))
        self.assertEqual(self.editor._map.get_tile_at_cell(4, 4), 0)

    def test_remove_large_tile(self):
        # remove spawn (2x2) tile
        self.assertEqual(self.editor._has_required, {
                         "spawn": True, "end": True})

        (screen_x, screen_y) = self.spawn_screen_location[0]
        screen_x += constants.TILE_SIZE + 1
        screen_y += constants.TILE_SIZE + 1

        (x, y) = self.spawn_location[0]

        self.editor.input_mouse_hold("right", (screen_x, screen_y))

        self.assertEqual(self.editor._map.get_tile_at_cell(x + 1, y + 1), 0)
        self.assertEqual(self.editor._has_required, {
                         "spawn": False, "end": True})
