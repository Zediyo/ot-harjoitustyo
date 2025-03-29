import pygame
import constants

from sprites.block import Block
from sprites.player import Player
from sprites.placeable import Placeable
from sprites.enemy import Enemy
from sprites.end import End


class Level:
	def __init__(self, level_data, tile_size=16):
		self.level = level_data
		self.width = len(level_data[0])
		self.height = len(level_data)

		self.tile_size = tile_size

		self.player = None
		self.blocks = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()

		self.all_sprites = pygame.sprite.Group()

		self._initialize_sprites()

	def _initialize_sprites(self):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.level[y][x]

				world_x = x * self.tile_size
				world_y = y * self.tile_size

				if tile == constants.TILE_BLOCK:
					self.blocks.add(Block(world_x, world_y))
				elif tile == constants.TILE_PLACEABLE:
					self.blocks.add(Placeable(world_x, world_y))
				elif tile == constants.TILE_ENEMY:
					self.enemies.add(Enemy(world_x, world_y))
				elif tile == constants.TILE_SPAWN:
					self.player = Player(world_x, world_y)
				elif tile == constants.TILE_END:
					self.blocks.add(End(world_x, world_y))

		self.all_sprites.add(
            self.blocks,
            self.enemies,
            self.player,
        )
			