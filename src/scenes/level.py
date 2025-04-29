""" Contains the Level scene class, which manages the game level."""

from constants import SceneName, TileType, InputAction, Settings
from scenes.scene import Scene

from sprites.block import Block
from sprites.player import Player
from sprites.placeable import Placeable
from sprites.enemy import Enemy
from sprites.end import End
from sprites.tile_cursor import TileCursor

from game.map import Map
from game.sprites import Sprites
from game.timer import Timer
from game.level_data import LevelData
from game.endscreen_data import EndScreenData

from ui.level_ui import LevelUI


class Level(Scene):
    """ Scene for the game level.

    Manages the game level, including the map, input, gamerules, sprites, and user interface.
    """

    def __init__(self, level: LevelData):
        """Initialize the Level scene.

        Args:
            level (LevelData): The level data to be loaded.
        """
        super().__init__()

        self._level = level
        self._map = Map(level.data)

        self._map_objects = {}
        self._sprites = Sprites()

        self._timer = Timer(level.id)
        self._level_ui = LevelUI(level.name)

        self._initialize_sprites()

    def _initialize_sprites(self):
        """ Create and place all sprites based on the map data. """
        for cell_x, cell_y, tile_id in self._map.iterate_cells():

            world_x, world_y = self._map.cell_index_to_world_pos(
                (cell_x, cell_y))

            if tile_id == TileType.BLOCK:
                self._sprites.add(Block(world_x, world_y))
            elif tile_id == TileType.PLACEABLE:
                placeable = Placeable(world_x, world_y)
                self._sprites.add(placeable)
                self._map_objects[(cell_x, cell_y)] = placeable
            elif tile_id == TileType.ENEMY:
                self._sprites.add(Enemy(world_x, world_y))
            elif tile_id == TileType.SPAWN:
                self._sprites.add(Player(world_x, world_y))
            elif tile_id == TileType.END:
                self._sprites.add(End(world_x, world_y))

        self._sprites.add(TileCursor(
            Settings.CURSOR_TILE_RANGE * self._map.tile_size))

    def draw(self, display):
        """ Draw the level and all sprites to the display. 

        Args:
            display (pygame.Surface): The display surface to draw on.
        """
        self._sprites.draw(display)
        self._level_ui.draw(display, self._sprites.player.charges, self._timer)

    def input_key(self, key):
        """ Handle keyboard input for player movement and actions.

        Args:
            key (InputAction): The key pressed.
        """
        self._timer.activate()

        if key == InputAction.LEFT:
            self._sprites.player.add_input(-1, 0)
        elif key == InputAction.RIGHT:
            self._sprites.player.add_input(1, 0)
        elif key == InputAction.JUMP:
            self._sprites.player.add_input(0, -1)
        elif key == InputAction.DOWN:
            self._sprites.player.add_input(0, 1)

    def input_mouse(self, click, pos):
        """ Handle mouse input for placing and removing objects and UI interactions.

        Args:
            click (InputAction): The mouse button clicked.
            pos (tuple[int,int]): The position of the mouse click.
        """

        self._update_cursor(pos)

        if click == InputAction.MOUSE_LEFT and self._level_ui.is_back_clicked(pos):
            self.set_next_scene(SceneName.LEVEL_LIST, False)

        cell_x, cell_y = self._map.screen_to_cell_index(pos)

        if not self._map.cell_in_bounds(cell_x, cell_y):
            return

        if not self._sprites.cursor.in_range:
            return

        if click == InputAction.MOUSE_LEFT:
            self._add_placeable_to_world(cell_x, cell_y)
        elif click == InputAction.MOUSE_RIGHT:
            self._remove_placeable_from_world(cell_x, cell_y)

    def update(self, dt, mouse_pos):
        """ Update the level state and all sprites.

        Args:
            dt (float): The delta time since the last frame.
            mouse_pos (tuple[int,int]): The current mouse position.
        """

        self._timer.update(dt)
        self._level_ui.update(mouse_pos)

        self._sprites.player.move(dt, self._sprites.blocks)
        self._sprites.enemies.update(
            dt, self._sprites.blocks, self._sprites.player.rect)

        self._update_cursor(mouse_pos)

        self._check_entities_in_bounds()
        self._check_enemy_collisions()
        self._check_end_collisions()

    def cleanup(self):
        """ Cleanup the level scene. """
        self._sprites.cleanup()

    def _update_cursor(self, pos):
        """ Update the tile cursor position and range check.

        Args:
            pos (tuple[int,int]): The current mouse position.
        """
        self._sprites.cursor.update(
            self._map.snap_to_grid(pos), self._sprites.player.rect)

    def _add_placeable_to_world(self, cell_x, cell_y):
        """ Attempt to add a placeable object to the world at the specified cell position.

        This will only succeed if the cell is empty and the player has charges remaining.
        If successful, the object is added to the world and the player's charges are decreased.

        Args:
            cell_x (int): The x index of the cell.
            cell_y (int): The y index of the cell.
        """
        if self._sprites.player.charges <= 0:
            return

        if self._sprites.cursor_collides_with_world():
            return

        if (cell_x, cell_y) in self._map_objects:
            return

        # add placeable to world
        world_x, world_y = self._map.cell_index_to_world_pos((cell_x, cell_y))
        placeable = Placeable(world_x, world_y)
        self._map_objects[(cell_x, cell_y)] = placeable

        self._sprites.add(placeable)

        # decrease inventory
        self._sprites.player.charges -= 1

    def _remove_placeable_from_world(self, cell_x, cell_y):
        """ Attempt to remove a placeable object from the world at the specified cell position.

        This will only succeed if the cell contains a placeable object.
        If successful, the object is removed from the world and the player's charges are increased.

        Args:
            cell_x (int): The x index of the cell.
            cell_y (int): The y index of the cell.
        """
        # check if cell has a removable object
        placeable = self._map_objects.get((cell_x, cell_y))

        if not placeable:
            return

        # kill
        placeable.kill()
        del self._map_objects[(cell_x, cell_y)]

        # increase inventory
        self._sprites.player.charges += 1

    def _check_enemy_collisions(self):
        """ Check for collisions between the player and enemies.

            If a collision is detected, the level is reset.
        """
        if self._sprites.player_collides_with_enemy():
            self.set_next_scene(SceneName.LEVEL, self._level)

    def _check_end_collisions(self):
        """ Check for collisions between the player and the level end.

            If a collision is detected, the level is completed scene is changed to the end screen.
            The timer is finished and passed along with the level data to the end screen.
        """
        if self._sprites.player_collides_with_end():
            self._timer.finish()

            self.set_next_scene(SceneName.END_SCREEN, EndScreenData(
                level=self._level, timer=self._timer))

    def _check_entities_in_bounds(self):
        """ Check if the player and enemies are within the screen bounds.

            If player is out of bounds, the level is reset.
            If an enemy is out of bounds, it is removed from the game.
        """
        left = self._sprites.player.rect.left
        right = self._sprites.player.rect.right
        top = self._sprites.player.rect.top
        if right < 0 or \
            left > Settings.SCREEN_WIDTH or \
                top > Settings.SCREEN_HEIGHT:
            self.set_next_scene(SceneName.LEVEL, self._level)

        for sprite in self._sprites.enemies:
            if sprite.rect.right < 0 or \
                sprite.rect.left > Settings.SCREEN_WIDTH or \
                    sprite.rect.top > Settings.SCREEN_HEIGHT:
                sprite.kill()
