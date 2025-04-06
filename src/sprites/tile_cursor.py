import pygame

from tools.asset_path import get_asset_path


class TileCursor(pygame.sprite.Sprite):
    def __init__(self, max_range=0):
        super().__init__()
        self.image = pygame.image.load(
            get_asset_path("pl_block_placeable.png"))
        self.image.set_alpha(128)
        self.rect = self.image.get_rect()
        self._max_range = max_range
        self.in_range = False

        self._original_image = self.image.copy()
        self._original_image.fill(
            (128, 128, 128, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self._original_image.fill(
            (0, 200, 0, 255), special_flags=pygame.BLEND_RGBA_ADD)

        self._out_of_range_image = self.image.copy()
        self._out_of_range_image.fill(
            (128, 128, 128, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self._out_of_range_image.fill(
            (200, 0, 0, 255), special_flags=pygame.BLEND_RGBA_ADD)

    def update(self, pos, player_rect):
        self.in_range = True

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if self._max_range > 0:
            if player_rect.top - self._max_range > self.rect.bottom or \
                player_rect.bottom + self._max_range < self.rect.top or \
                    player_rect.left - self._max_range > self.rect.right or \
                    player_rect.right + self._max_range < self.rect.left:
                self.image = self._out_of_range_image
                self.in_range = False
                # change to red overlay
            else:
                self.image = self._original_image
                # change to normal color
