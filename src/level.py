import pygame
import constants

from sprites.block import Block
from sprites.player import Player
from sprites.placeable import Placeable
from sprites.enemy import Enemy
from sprites.end import End
from sprites.tile_cursor import TileCursor


class Level:
	def __init__(self, level_data, tile_size=constants.TILE_SIZE):
		self._map = level_data
		self._width = len(level_data[0])
		self._height = len(level_data)

		self._tile_size = tile_size

		self._player = None
		self._tile_cursor = None

		self._blocks = pygame.sprite.Group()
		self._enemies = pygame.sprite.Group()

		self._map_objects = {}
		self._placeables = pygame.sprite.Group()

		self.all_sprites = pygame.sprite.Group()

		self._initialize_sprites()

	def _initialize_sprites(self):
		for y in range(self._height):
			for x in range(self._width):
				tile = self._map[y][x]

				grid_x, grid_y = self._cell_pos_to_grid((x, y))

				if tile == constants.TILE_BLOCK:
					self._blocks.add(Block(grid_x, grid_y))
				elif tile == constants.TILE_PLACEABLE:
					placeable = Placeable(grid_x, grid_y)
					self._placeables.add(placeable)
					self._map_objects[(x, y)] = placeable
				elif tile == constants.TILE_ENEMY:
					self._enemies.add(Enemy(grid_x, grid_y))
				elif tile == constants.TILE_SPAWN:
					self._player = Player(grid_x, grid_y)
				elif tile == constants.TILE_END:
					self._blocks.add(End(grid_x, grid_y))

		self._tile_cursor = TileCursor()
		self.all_sprites.add(
            self._blocks,
            self._enemies,
            self._player,
			self._placeables,
			self._tile_cursor,
        )

	def input_key(self, key):
		dx, dy = 0, 0
		if key == "left":
			dx = -1
		elif key == "right":
			dx = 1
		elif key == "jump":
			dy = -1
		elif key == "down":
			dy = 1

		self._player.move(dx, dy)
	
	def input_mouse(self, click, pos):
		grid_x, grid_y = self._screen_pos_to_grid(pos)
		cell_x, cell_y = self._grid_pos_to_cell((grid_x, grid_y))

		if click == "left":
			if self._map[cell_y][cell_x] != constants.TILE_EMPTY:
				return
			
			self._map[cell_y][cell_x] = constants.TILE_PLACEABLE

			placeable = Placeable(grid_x, grid_y)
			self._map_objects[(cell_x, cell_y)] = placeable

			self._placeables.add(placeable)
			self.all_sprites.add(placeable)
		elif click == "right":
			if self._map[cell_y][cell_x] != constants.TILE_PLACEABLE:
				return
			
			self._map[cell_y][cell_x] = constants.TILE_EMPTY
			placeable = self._map_objects.get((cell_x, cell_y))
			
			if placeable:
				placeable.kill()

				del self._map_objects[(cell_x, cell_y)]
				self._placeables.remove(placeable)
				self.all_sprites.remove(placeable)

	def update(self, delta_time, mouse_pos):
		self._tile_cursor.update(self._screen_pos_to_grid(mouse_pos))

	def _screen_pos_to_grid(self, pos):
		x, y = pos
		ret_x = x // self._tile_size * self._tile_size
		ret_y = y // self._tile_size * self._tile_size

		return ret_x, ret_y
	
	def _grid_pos_to_cell(self, pos):
		x, y = pos
		ret_x = x // self._tile_size
		ret_y = y // self._tile_size

		return ret_x, ret_y
	
	def _cell_pos_to_grid(self, pos):
		x, y = pos
		ret_x = x * self._tile_size
		ret_y = y * self._tile_size

		return ret_x, ret_y
		
			