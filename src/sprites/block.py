import pygame

from tools.asset_path import get_asset_path


class Block(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(get_asset_path("pl_block.png"))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
