""" Contains the Sprites class, which manages all sprites used during a game level."""

import pygame
from pygame.sprite import Sprite, Group

from sprites.block import Block
from sprites.placeable import Placeable
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.end import End
from sprites.tile_cursor import TileCursor


class Sprites:
    """Container for all sprite groups and sprite references used during a level.

    Handles adding sprites to the appropriate drawing layers and collision groups.
    Provides methods for drawing sprites, checking collisions, and cleaning up sprites.
    """

    def __init__(self):
        """Initialize the Sprites class."""
        self._player = None
        self._cursor = None
        self._end = None

        self._blocks = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()
        self._world = pygame.sprite.Group()

        self._draw_sprites = pygame.sprite.LayeredUpdates()

    @property
    def player(self) -> Sprite | None:
        """Get the player sprite.
        
        Returns:
            Sprite | None: The player sprite or None if not set.
        """
        return self._player

    @property
    def cursor(self) -> Sprite | None:
        """Get the tile selection cursor sprite.
        
        Returns:
            Sprite | None: The tile selection cursor sprite or None if not set.
        """
        return self._cursor

    @property
    def end(self) -> Sprite | None:
        """Get the level end/goal sprite.
        
        Returns:
            Sprite | None: The level end/goal sprite or None if not set.
        """
        return self._end

    @property
    def blocks(self) -> Group:
        """Get the group of block and placeable sprites.
        
        Returns:
            Group: The group of block and placeable sprites.
        """
        return self._blocks

    @property
    def enemies(self) -> Group:
        """Get the group of enemy sprites.
        
        Returns:
            Group: The group of enemy sprites.
        """
        return self._enemies

    @property
    def world(self) -> Group:
        """Get the group of all sprites in the game world.
        
        Returns:
            Group: The group of all sprites in the game world (excluding cursor).
        """
        return self._world

    def add(self, sprite):
        """Add a sprite to the appropriate group and layer.

        Args:
            sprite (Sprite): The sprite to add.
        """
        if isinstance(sprite, (Block, Placeable)):
            self._add_block(sprite)
        elif isinstance(sprite, Enemy):
            self._add_enemy(sprite)
        elif isinstance(sprite, Player):
            self._add_player(sprite)
        elif isinstance(sprite, End):
            self._add_end(sprite)
        elif isinstance(sprite, TileCursor):
            self._add_cursor(sprite)

    def _add_block(self, sprite):
        self._blocks.add(sprite)
        self._world.add(sprite)
        self._draw_sprites.add(sprite, layer=10)

    def _add_enemy(self, sprite):
        self._enemies.add(sprite)
        self._world.add(sprite)
        self._draw_sprites.add(sprite, layer=20)

    def _add_player(self, sprite):
        self._player = sprite
        self._world.add(sprite)
        self._draw_sprites.add(sprite, layer=30)

    def _add_end(self, sprite):
        self._end = sprite
        self._world.add(sprite)
        self._draw_sprites.add(sprite, layer=40)

    def _add_cursor(self, sprite):
        self._cursor = sprite
        self._draw_sprites.add(sprite, layer=50)

    def draw(self, display):
        """Draw all sprites to the display.

        Args:
            display (pygame.Surface): The display surface to draw on.
        """
        self._draw_sprites.draw(display)

    def cleanup(self):
        """Remove all sprites from the groups and clear references."""

        for sprite in self._draw_sprites:
            sprite.kill()

        self._player = None
        self._cursor = None
        self._end = None
        self._blocks.empty()
        self._enemies.empty()
        self._world.empty()
        self._draw_sprites.empty()

    def player_collides_with_enemy(self):
        """Check if the player collides with any enemies.
        
        Returns:
            bool: True if the player collides with an enemy, False otherwise.
        """
        if self._player is None:
            return False
        return pygame.sprite.spritecollide(self._player, self._enemies, False)

    def player_collides_with_end(self):
        """Check if the player collides with the end sprite.
        
        Returns:
            bool: True if the player collides with the end, False otherwise.
        """
        if self._player is None or self._end is None:
            return False
        return pygame.sprite.spritecollide(self._player, [self._end], False)

    def cursor_collides_with_world(self):
        """Check if the cursor collides with any world sprites.
        
        Returns:
            bool: True if the cursor collides with a world sprite, False otherwise.
        """
        if self._cursor is None:
            return False
        return pygame.sprite.spritecollide(self._cursor, self._world, False)
