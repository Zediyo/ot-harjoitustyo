import pygame

from tools.asset_path import get_asset_path

class Player(pygame.sprite.Sprite):
	def __init__(self, x=0, y=0):
		super().__init__()

		self.image = pygame.image.load(get_asset_path("pl_player.png"))
		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

	def move(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy