import pygame
from tools.asset_path import get_asset_path

class Player(pygame.sprite.Sprite):
	def __init__(self, x=0, y=0):
		super().__init__()

		self.image = pygame.image.load(get_asset_path("pl_player.png"))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		##constants variables
		self._gravity_constant = 800
		self._terminal_velocity = 1000
		self._movement_speed = 150.0
		self._jump_force = -285.0
		self._floor_gravity = 100.0

		#movement variables
		self._input = [0,0]
		self._gravity = 0.0
		self._velocity = pygame.Vector2(0, 0)
		self._position = pygame.Vector2(x, y)
		self._on_floor = False

	def move(self, dt, colliders):
		#update velocity + gravity
		self._velocity.x = self._input[0] * self._movement_speed
		#self._velocity.y = self._input[1] * self._movement_speed

		#jumping and walk off gravity
		if self._on_floor:
			if self._input[1] < 0:
				self._gravity = self._jump_force
			else:
				self._gravity = self._floor_gravity

		#gravity
		self._velocity.y = (self._gravity + dt * self._gravity_constant / 2)
		self._gravity += self._gravity_constant * dt

		self._gravity = min(self._gravity, self._terminal_velocity)

		#update position
		self._position += self._velocity * dt

		#reset input
		self._input[0] = 0
		self._input[1] = 0

		self._move_and_collide(colliders)

	def add_input(self, dx, dy):
		self._input[0] += dx
		self._input[1] += dy


	def _move_and_collide(self, colliders):
		self._on_floor = False

		#horizontal
		self.rect.x = self._position.x
		colliding = pygame.sprite.spritecollide(self, colliders, False)

		if colliding:
			for other in colliding:
				if self._velocity[0] > 0:
					self.rect.right = other.rect.left
				elif self._velocity[0] < 0:
					self.rect.left = other.rect.right
			
			self._velocity[0] = 0
			self._position.x = self.rect.x

		#vertical
		self.rect.y = self._position.y
		colliding = pygame.sprite.spritecollide(self, colliders, False)

		if colliding:
			for other in colliding:
				if self._velocity[1] > 0:
					self.rect.bottom = other.rect.top
					self._on_floor = True
				elif self._velocity[1] < 0:
					self.rect.top = other.rect.bottom
					self._gravity = 0

			self._velocity[1] = 0
			self._position.y = self.rect.y