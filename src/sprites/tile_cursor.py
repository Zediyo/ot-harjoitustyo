import pygame

from tools.asset_path import get_asset_path


class TileCursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            get_asset_path("pl_block_placeable.png"))
        self.image.set_alpha(128)
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
