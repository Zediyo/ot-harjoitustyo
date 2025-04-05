import pygame
import constants

from sprites.block import Block
from sprites.player import Player
from sprites.placeable import Placeable
from sprites.enemy import Enemy
from sprites.end import End
from sprites.tile_cursor import TileCursor
from scenes.scene import Scene


class Level(Scene):
	def __init__(self, level_data, tile_size=constants.TILE_SIZE):
		super().__init__()

		self._map = level_data
		self._width = len(level_data[0])
		self._height = len(level_data)

		self._tile_size = tile_size

		self._player = None
		self._tile_cursor = None

		self._map_objects = {}
		self._blocks = pygame.sprite.Group()
		self._enemies = pygame.sprite.Group()

		self._all_sprites = pygame.sprite.Group()

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
					self._blocks.add(placeable)
					self._map_objects[(x, y)] = placeable
				elif tile == constants.TILE_ENEMY:
					self._enemies.add(Enemy(grid_x, grid_y))
				elif tile == constants.TILE_SPAWN:
					self._player = Player(grid_x, grid_y)
				elif tile == constants.TILE_END:
					self._blocks.add(End(grid_x, grid_y))

		self._tile_cursor = TileCursor()
		self._all_sprites.add(
            self._player,
			self._blocks,
            self._enemies,
			self._tile_cursor,
        )

	def draw(self, display):
		self._all_sprites.draw(display)

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
		grid_x, grid_y = self._screen_pos_to_grid(pos)
		cell_x, cell_y = self._grid_pos_to_cell((grid_x, grid_y))

		if click == "left":
			self._add_placeable_to_world(grid_x, grid_y, cell_x, cell_y)
		elif click == "right":
			self._remove_placeable_from_world(cell_x, cell_y)


	def update(self, dt, mouse_pos):
		self._tile_cursor.update(self._screen_pos_to_grid(mouse_pos))

		self._player.move(dt, self._blocks)
	
	def cleanup(self):
		for sprite in self._all_sprites:
			sprite.kill()

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
	
	def _add_placeable_to_world(self, grid_x, grid_y, cell_x, cell_y):
		#check if player has placeable blocks in inventory

		#check if player is in range

		#check if cell is in bounds
		if cell_x < 0 or cell_x >= self._width or cell_y < 0 or cell_y >= self._height:
			return

		#check if cell is empty
		if self._map[cell_y][cell_x] != constants.TILE_EMPTY:
			return
			
		#create + add
		self._map[cell_y][cell_x] = constants.TILE_PLACEABLE

		placeable = Placeable(grid_x, grid_y)
		self._map_objects[(cell_x, cell_y)] = placeable

		self._blocks.add(placeable)
		self._all_sprites.add(placeable)

	def _remove_placeable_from_world(self, cell_x, cell_y):
		#check if player is in range

		#check if cell is in bounds
		if cell_x < 0 or cell_x >= self._width or cell_y < 0 or cell_y >= self._height:
			return

		#check if cell has a removable object
		if self._map[cell_y][cell_x] != constants.TILE_PLACEABLE:
			return
		
		#kill + remove
		self._map[cell_y][cell_x] = constants.TILE_EMPTY
		placeable = self._map_objects.get((cell_x, cell_y))
		
		if placeable:
			placeable.kill()

			del self._map_objects[(cell_x, cell_y)]
			self._blocks.remove(placeable)
			self._all_sprites.remove(placeable)

		#add +1 to inventory
	
			