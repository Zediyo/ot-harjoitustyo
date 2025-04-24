import pygame
import constants

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

from ui.level_ui import LevelUI


class Level(Scene):
    def __init__(self, level, tile_size=constants.TILE_SIZE):
        super().__init__()

        self.level = level
        self._map = Map(level["data"], tile_size)

        self._map_objects = {}
        self._sprites = Sprites()

        self._timer = Timer(level["id"])
        self._level_ui = LevelUI(level["name"])

        self._initialize_sprites()

    def _initialize_sprites(self):
        for y in range(self._map.height):
            for x in range(self._map.width):
                tile = self._map.data[y][x]

                grid_x, grid_y = self._map.cell_pos_to_grid((x, y))

                if tile == constants.TILE_BLOCK:
                    self._sprites.blocks.add(Block(grid_x, grid_y))
                elif tile == constants.TILE_PLACEABLE:
                    placeable = Placeable(grid_x, grid_y)
                    self._sprites.blocks.add(placeable)
                    self._map_objects[(grid_x, grid_y)] = placeable
                elif tile == constants.TILE_ENEMY:
                    self._sprites.enemies.add(Enemy(grid_x, grid_y))
                elif tile == constants.TILE_SPAWN:
                    self._sprites.player = Player(grid_x, grid_y)
                elif tile == constants.TILE_END:
                    self._sprites.end = End(grid_x, grid_y)

        self._sprites.cursor = TileCursor(3 * self._map.tile_size)
        self._sprites.all.add(
            self._sprites.player,
            self._sprites.blocks,
            self._sprites.enemies,
            self._sprites.end,
        )

    def draw(self, display):
        self._sprites.all.draw(display)
        display.blit(self._sprites.cursor.image, self._sprites.cursor.rect)
        self._level_ui.draw(display, self._sprites.player.charges, self._timer)

    def input_key(self, key):
        self._timer.activate()

        if key == "left":
            self._sprites.player.add_input(-1, 0)
        elif key == "right":
            self._sprites.player.add_input(1, 0)
        elif key == "jump":
            self._sprites.player.add_input(0, -1)
        elif key == "down":
            self._sprites.player.add_input(0, 1)

    def input_mouse(self, click, pos):
        self._update_cursor(pos)

        if click == "left" and self._level_ui.is_back_clicked(pos):
            self.set_next_scene("level_list", "level")

        grid_x, grid_y = self._map.screen_pos_to_grid(pos)

        # check if click is in bounds
        if not self._map.tile_in_bounds(grid_x, grid_y):
            return

        # check if click is in range
        if not self._sprites.cursor.in_range:
            return

        if click == "left":
            self._add_placeable_to_world(grid_x, grid_y)
        elif click == "right":
            self._remove_placeable_from_world(grid_x, grid_y)

    def update(self, dt, mouse_pos):
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
        for sprite in self._sprites.all:
            sprite.kill()

    def _update_cursor(self, pos):
        self._sprites.cursor.update(
            self._map.screen_pos_to_grid(pos), self._sprites.player.rect)

    def _add_placeable_to_world(self, grid_x, grid_y):
        # check if player has placeable blocks in inventory
        if self._sprites.player.charges <= 0:
            return

        # check if area is empty
        if pygame.sprite.spritecollide(self._sprites.cursor, self._sprites.all, False):
            return

        if (grid_x, grid_y) in self._map_objects:
            return

        # add placeable to world
        placeable = Placeable(grid_x, grid_y)
        self._map_objects[(grid_x, grid_y)] = placeable

        self._sprites.blocks.add(placeable)
        self._sprites.all.add(placeable)

        # remove -1 from inventory
        self._sprites.player.charges -= 1

    def _remove_placeable_from_world(self, grid_x, grid_y):
        # check if cell has a removable object
        placeable = self._map_objects.get((grid_x, grid_y))

        if not placeable:
            return

        # kill
        placeable.kill()
        del self._map_objects[(grid_x, grid_y)]

        # add +1 to inventory
        self._sprites.player.charges += 1

    def _check_enemy_collisions(self):
        if pygame.sprite.spritecollide(self._sprites.player, self._sprites.enemies, False):
            self.set_next_scene("level", self.level)

    def _check_end_collisions(self):
        if pygame.sprite.spritecollide(self._sprites.player, [self._sprites.end], False):
            self._timer.finish()

            self.set_next_scene("endscreen", {
                "level": self.level,
                "timer": self._timer,
            })

    def _check_entities_in_bounds(self):
        # check if player is in bounds
        left = self._sprites.player.rect.left
        right = self._sprites.player.rect.right
        top = self._sprites.player.rect.top
        if right < 0 or \
            left > constants.SCREEN_WIDTH or \
                top > constants.SCREEN_HEIGHT:
            self.set_next_scene("level", self.level)

        for sprite in self._sprites.enemies:
            if sprite.rect.right < 0 or \
                sprite.rect.left > constants.SCREEN_WIDTH or \
                    sprite.rect.top > constants.SCREEN_HEIGHT:
                sprite.kill()
