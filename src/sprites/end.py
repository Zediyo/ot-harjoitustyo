import pygame

from tools.asset_helpers import load_image


class End(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = load_image("pl_end.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
