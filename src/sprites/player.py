import pygame
from tools.asset_path import get_asset_path

from game.body import Body


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(get_asset_path("pl_player.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.body = Body(self.rect, x, y)

    def move(self, dt, colliders):
        self.body.move(dt, colliders)

    def add_input(self, dx, dy):
        self.body.add_input(dx, dy)
