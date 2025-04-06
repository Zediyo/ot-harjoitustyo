import pygame
import constants

from sprites.block import Block
from sprites.player import Player
from sprites.placeable import Placeable
from sprites.enemy import Enemy
from sprites.end import End
from sprites.tile_cursor import TileCursor
from scenes.scene import Scene
from map import Map


class Level(Scene):
    def __init__(self, level_data, tile_size=constants.TILE_SIZE):
        super().__init__()
        self._map = Map(level_data, tile_size)

        self._player = None
        self._tile_cursor = None
        self._end = None

        self._map_objects = {}
        self._blocks = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()

        self._all_sprites = pygame.sprite.Group()

        self._initialize_sprites()

    def _initialize_sprites(self):
        for y in range(self._map.height):
            for x in range(self._map.width):
                tile = self._map.data[y][x]

                grid_x, grid_y = self._map.cell_pos_to_grid((x, y))

                if tile == constants.TILE_BLOCK:
                    self._blocks.add(Block(grid_x, grid_y))
                elif tile == constants.TILE_PLACEABLE:
                    placeable = Placeable(grid_x, grid_y)
                    self._blocks.add(placeable)
                    self._map_objects[(grid_x, grid_y)] = placeable
                elif tile == constants.TILE_ENEMY:
                    self._enemies.add(Enemy(grid_x, grid_y))
                elif tile == constants.TILE_SPAWN:
                    self._player = Player(grid_x, grid_y)
                elif tile == constants.TILE_END:
                    self._end = End(grid_x, grid_y)

        self._tile_cursor = TileCursor(3 * self._map.tile_size)
        self._all_sprites.add(
            self._player,
            self._blocks,
            self._enemies,
            self._end,
        )

    def draw(self, display):
        self._all_sprites.draw(display)
        display.blit(self._tile_cursor.image, self._tile_cursor.rect)

    def input_key(self, key):
        if key == "left":
            self._player.add_input(-1, 0)
        elif key == "right":
            self._player.add_input(1, 0)
        elif key == "jump":
            self._player.add_input(0, -1)
        elif key == "down":
            self._player.add_input(0, 1)

    def input_mouse(self, click, pos):
        grid_x, grid_y = self._map.screen_pos_to_grid(pos)

        # check if click is in bounds
        if not self._map.tile_in_bounds(grid_x, grid_y):
            return

        # check if click is in range
        if not self._tile_cursor.in_range:
            return

        if click == "left":
            self._add_placeable_to_world(grid_x, grid_y)
        elif click == "right":
            self._remove_placeable_from_world(grid_x, grid_y)

    def update(self, dt, mouse_pos):
        self._player.move(dt, self._blocks)
        self._enemies.update(dt, self._blocks, self._player.rect)

        self._tile_cursor.update(
            self._map.screen_pos_to_grid(mouse_pos), self._player.rect)

        self._check_enemy_collisions()
        self._check_end_collisions()

    def cleanup(self):
        for sprite in self._all_sprites:
            sprite.kill()

    def _add_placeable_to_world(self, grid_x, grid_y):
        # check if player has placeable blocks in inventory

        # check if area is empty
        if pygame.sprite.spritecollide(self._tile_cursor, self._all_sprites, False):
            return

        if (grid_x, grid_y) in self._map_objects:
            return

        # add placeable to world
        placeable = Placeable(grid_x, grid_y)
        self._map_objects[(grid_x, grid_y)] = placeable

        self._blocks.add(placeable)
        self._all_sprites.add(placeable)

    def _remove_placeable_from_world(self, grid_x, grid_y):
        # check if cell has a removable object
        placeable = self._map_objects.get((grid_x, grid_y))

        if not placeable:
            return

        # kill
        placeable.kill()
        del self._map_objects[(grid_x, grid_y)]

        # add +1 to inventory

    def _check_enemy_collisions(self):
        if pygame.sprite.spritecollide(self._player, self._enemies, False):
            self._end_scene = True
            self._next_scene = "level"

    def _check_end_collisions(self):
        if pygame.sprite.spritecollide(self._player, [self._end], False):
            self._end_scene = True
            self._next_scene = "mainmenu"
