import pygame

import constants

from scenes.scene import Scene
from ui.editor_ui import EditorUI
from game.map import Map

from tools.preview_generator import generate_level_preview
from tools.db import save_level

from sprites.tile_cursor import TileCursor


class LevelEditor(Scene):

    def __init__(self, level):
        super().__init__()

        self._level = level
        self._ui = EditorUI(level["name"])
        self._map = Map(self._level["data"])
        self._map.expand_map()
        self._hand = 0

        self._has_required = {"spawn": False, "end": False}
        self.image = None
        self._update_image()
        self._update_required()

        self._cursor = TileCursor()

    def draw(self, display):
        display.fill((128, 128, 128))
        display.blit(self.image, (0, 0))
        display.blit(self._cursor.image, self._cursor.rect)
        self._ui.draw(display, self._hand, self._has_required)

    def input_mouse(self, click, pos):
        if click == "left" and self._ui.is_back_clicked(pos):
            self.set_next_scene("level_list", "editor")

        if click == "left" and self._ui.is_save_clicked(pos):
            self._map.shrink_map()
            if self._map.is_map_viable():
                save_level(self._level["name"], self._map.data)
            self.set_next_scene("level_list", "editor")

    def input_mouse_hold(self, click, pos):
        if self._hand == 0:
            return

        if click == "left":
            self._add_to_map(pos)
        elif click == "right":
            self._remove_from_map(pos)

    def input_raw(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._hand = constants.TILE_BLOCK
                elif event.key == pygame.K_2:
                    self._hand = constants.TILE_PLACEABLE
                elif event.key == pygame.K_3:
                    self._hand = constants.TILE_ENEMY
                elif event.key == pygame.K_4:
                    self._hand = constants.TILE_SPAWN
                elif event.key == pygame.K_5:
                    self._hand = constants.TILE_END

    def update(self, dt, mouse_pos):
        self._ui.update(mouse_pos)
        self._cursor.update(self._map.screen_pos_to_grid(mouse_pos), None)

    def cleanup(self):
        return self._cursor.kill()

    def _add_to_map(self, pos):
        x, y = self._map.screen_pos_to_cell(pos)

        updated = self._add_tile_to_map(x, y, self._hand)

        if updated:
            self._update_image()
            self._update_required()

    def _add_tile_to_map(self, x, y, tile):
        # normal, placeable - 1x1 no limit
        if tile in (constants.TILE_BLOCK, constants.TILE_PLACEABLE):
            if self._map.get_cell(x, y) == 0:
                return self._map.insert_cell(x, y, tile)

        # player spawn - 2x2 max 1
        if tile == constants.TILE_SPAWN:
            if not self._map.has_spawn() and self._map.has_empty_area(x, y, (2, 2)):
                return self._map.add_tile(x, y, tile, (2, 2))

        # enemy spawn - 2x2 no limit
        if tile == constants.TILE_ENEMY:
            if self._map.has_empty_area(x, y, (2, 2)):
                return self._map.add_tile(x, y, tile, (2, 2))

        # end - 1x1 max 1
        if tile == constants.TILE_END:
            if not self._map.has_end() and self._map.get_cell(x, y) == 0:
                return self._map.insert_cell(x, y, tile)

        return False

    def _remove_from_map(self, pos):
        x, y = self._map.screen_pos_to_cell(pos)

        updated = self._remove_tile_from_map(x, y)

        if updated:
            self._update_image()
            self._update_required()

    def _remove_tile_from_map(self, x, y):
        tile = self._map.get_cell(x, y)
        if tile == 0:
            return False

        # 1x1 tiles
        if tile in (constants.TILE_BLOCK, constants.TILE_PLACEABLE, constants.TILE_END):
            return self._map.remove_cell(x, y)

        # 2x2 tiles
        if tile in (constants.TILE_SPAWN, constants.TILE_ENEMY):
            return self._map.remove_tile(x, y, (2, 2))

        if tile < 0:
            if abs(tile) in (constants.TILE_SPAWN, constants.TILE_ENEMY):
                res = self._map.find_nearest_corner(x, y, tile, (2, 2))
                if res is None:
                    return False
                corner_x, corner_y = res
                return self._map.remove_tile(corner_x, corner_y, (2, 2))

        return False

    def _update_image(self):
        self.image = generate_level_preview(
            self._map.data, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    def _update_required(self):
        self._has_required["spawn"] = self._map.has_spawn()
        self._has_required["end"] = self._map.has_end()
