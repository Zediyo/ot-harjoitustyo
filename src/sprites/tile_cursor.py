"""Contains the TileCursor sprite class, representing the players cursor for placing tiles."""

import pygame

from tools.asset_helpers import load_image


class TileCursor(pygame.sprite.Sprite):
    """ A cursor snapped to the tile grid that indicates where a tile can be placed. 

    The cursor is semi-transparent and changes color based on whether placement is valid.
    It does not interact with the game world and is only used for visual feedback.

    Attributes:
        image (pygame.Surface): The image representing the cursor.
        rect (pygame.Rect): The rectangle representing the cursor's position and size.
        in_range (bool): Indicates whether the cursor is within the valid placement range.
    """

    def __init__(self, max_range=0):
        """ Initialize the TileCursor sprite.

        Args:
            max_range (int, optional):
                The maximum distance from player in tile units to allow placement.
                Defaults to 0, which means no range limit.
        """
        super().__init__()

        self.image = load_image("pl_block_placeable.png")
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

    def update(self, pos, player_rect=None):
        """ Update the cursor position and check if it's in range.

        Args:
            pos (tuple): The (x, y) position to place the cursor.
            player_rect (pygame.Rect, optional):
                The player's rectangle used for range checking.
                Defaults to None, which means no range limit.
        """
        self.in_range = True

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if self._max_range > 0 and player_rect is not None:
            if (
                player_rect.top - self._max_range > self.rect.bottom
                or player_rect.bottom + self._max_range < self.rect.top
                or player_rect.left - self._max_range > self.rect.right
                or player_rect.right + self._max_range < self.rect.left
            ):
                self.image = self._out_of_range_image
                self.in_range = False
            else:
                self.image = self._original_image
