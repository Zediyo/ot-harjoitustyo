""" Contains the LevelEditor scene class, which allows users to create and edit levels. """

import pygame

from constants import TileType, SceneName, InputAction, Settings
from tools.preview_generator import generate_level_preview
from tools.db import save_level

from scenes.scene import Scene
from ui.editor_ui import EditorUI
from sprites.tile_cursor import TileCursor
from game.map import Map
from game.level_data import LevelData


class LevelEditor(Scene):
    """ Scene for creating and editing levels.

    Allows users to create and edit levels by placing and removing tiles.
    Tiles can be placed in a grid, and the editor checks for valid placements.
    """

    _BACKGROUND_COLOR = (128, 128, 128)

    _SINGLE_TILES_NO_LIMIT = (TileType.BLOCK, TileType.PLACEABLE)
    _SINGLE_TILES = (TileType.BLOCK, TileType.PLACEABLE, TileType.END)
    _MULTI_TILES = (TileType.SPAWN, TileType.ENEMY)
    _MULTI_TILE_SIZE = (2, 2)

    def __init__(self, level: LevelData):
        """Initialize the LevelEditor scene.

        Args:
            level (LevelData): The level data to load into the editor.
        """
        super().__init__()

        self._level = level
        self._ui = EditorUI(level.name)
        self._map = Map(level.data)
        self._map.expand_map()
        self._hand = TileType.EMPTY

        self._has_required = {"spawn": False, "end": False}
        self._image = None
        self._update_image()
        self._update_required()

        self._cursor = TileCursor()

    def draw(self, display):
        """Draw the level editor scene.

        Args:
            display (pygame.Surface): The surface to draw on.
        """
        display.fill(self._BACKGROUND_COLOR)
        display.blit(self._image, (0, 0))
        display.blit(self._cursor.image, self._cursor.rect)
        self._ui.draw(display, self._hand, self._has_required)

    def input_mouse(self, click, pos):
        """Handle mouse button input for buttons.

        Args:
            click (InputAction): The mouse input action (e.g., InputAction.MOUSE_LEFT).
            pos (tuple[int, int]): The mouse position (x, y) on screen.
        """
        if click == InputAction.MOUSE_LEFT and self._ui.is_back_clicked(pos):
            self.set_next_scene(SceneName.LEVEL_LIST, True)

        if click == InputAction.MOUSE_LEFT and self._ui.is_save_clicked(pos):
            self._map.shrink_map()
            if self._map.is_map_viable():
                save_level(LevelData(-1, self._level.name, self._map.data))
            self.set_next_scene(SceneName.LEVEL_LIST, True)

    def input_mouse_hold(self, click, pos):
        """Handle mouse button hold input for placing and removing tiles.

        Args:
            click (InputAction): The mouse input action held down.
            pos (tuple[int, int]): The mouse position (x, y) on screen.
        """
        if self._hand == TileType.EMPTY:
            return

        if click == InputAction.MOUSE_LEFT:
            self._add_to_map(pos)
        elif click == InputAction.MOUSE_RIGHT:
            self._remove_from_map(pos)

    def input_raw(self, events):
        """Handle raw keyboard input for tile selection.

        Args:
            events (list[pygame.event.Event]): List of Pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._hand = TileType.BLOCK
                elif event.key == pygame.K_2:
                    self._hand = TileType.PLACEABLE
                elif event.key == pygame.K_3:
                    self._hand = TileType.ENEMY
                elif event.key == pygame.K_4:
                    self._hand = TileType.SPAWN
                elif event.key == pygame.K_5:
                    self._hand = TileType.END

    def update(self, dt, mouse_pos):
        """Update the level editor scene and its components.

        Args:
            dt (float): Time delta since the last frame.
            mouse_pos (tuple[int, int]): Current mouse position.
        """
        self._ui.update(mouse_pos)
        self._cursor.update(self._map.snap_to_grid(mouse_pos), None)

    def cleanup(self):
        """Clean up the level editor scene."""
        self._cursor.kill()

    def _add_to_map(self, pos):
        """ Attempts to add a tile to the map at the specified position.

        Args:
            pos (tuple[int, int]): The position (x, y) on screen.
        """
        x, y = self._map.screen_to_cell_index(pos)

        updated = self._add_tile_to_map(x, y, self._hand)

        if updated:
            self._update_image()
            self._update_required()

    def _add_tile_to_map(self, x, y, tile):
        """ Internal method to add a tile to the map based on its type. 

        Args:
            x (int): The x index of the cell in the grid.
            y (int): The y index of the cell in the grid.
            tile (TileType): The type of tile to add.
        """
        # 1x1 tiles - no limit
        if tile in self._SINGLE_TILES_NO_LIMIT:
            if self._map.get_tile_at_cell(x, y) == 0:
                return self._map.set_tile_at_cell(x, y, tile)

        # player spawn - 2x2 max 1
        if tile == TileType.SPAWN:
            if not self._map.contains_tile(TileType.SPAWN) \
                    and self._map.is_empty_area(x, y, self._MULTI_TILE_SIZE):
                return self._map.add_multi_tile(x, y, tile, self._MULTI_TILE_SIZE)

        # enemy spawn - 2x2 no limit
        if tile == TileType.ENEMY:
            if self._map.is_empty_area(x, y, self._MULTI_TILE_SIZE):
                return self._map.add_multi_tile(x, y, tile, self._MULTI_TILE_SIZE)

        # end - 1x1 max 1
        if tile == TileType.END:
            if not self._map.contains_tile(TileType.END) \
                    and self._map.get_tile_at_cell(x, y) == 0:
                return self._map.set_tile_at_cell(x, y, tile)

        return False

    def _remove_from_map(self, pos):
        """ Attempts to remove a tile from the map at the specified position.

        Args:
            pos (tuple[int, int]): The position (x, y) on screen.
        """
        x, y = self._map.screen_to_cell_index(pos)

        updated = self._remove_tile_from_map(x, y)

        if updated:
            self._update_image()
            self._update_required()

    def _remove_tile_from_map(self, x, y):
        """ Internal method to remove a tile from the map based on its type.

        Args:
            x (int): The x index of the cell in the grid.
            y (int): The y index of the cell in the grid.
        """
        tile = self._map.get_tile_at_cell(x, y)
        if tile == 0:
            return False

        # 1x1 tiles
        if tile in self._SINGLE_TILES:
            return self._map.set_tile_at_cell(x, y, 0)

        # 2x2 tiles
        if tile in self._MULTI_TILES:
            return self._map.remove_multi_tile(x, y, self._MULTI_TILE_SIZE)

        if tile < 0 and abs(tile) in self._MULTI_TILES:
            res = self._map.find_nearest_tile_corner(
                x, y, tile, self._MULTI_TILE_SIZE)
            if res is None:
                return False
            corner_x, corner_y = res
            return self._map.remove_multi_tile(corner_x, corner_y, self._MULTI_TILE_SIZE)

        return False

    def _update_image(self):
        """ Regenerates the level preview image based on the current map data. """
        self._image = generate_level_preview(
            self._map.data, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def _update_required(self):
        """ Update the status of required tiles for the level. """
        self._has_required["spawn"] = self._map.contains_tile(TileType.SPAWN)
        self._has_required["end"] = self._map.contains_tile(TileType.END)
