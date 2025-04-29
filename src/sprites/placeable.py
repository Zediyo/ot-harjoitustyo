"""Contains the Placeable sprite class, representing placeable blocks in the game."""

import pygame

from tools.asset_helpers import load_image


class Placeable(pygame.sprite.Sprite):
    """ A placeable block that the player can interact with.

    The block can be placed and removed during the level, typically
    used to reach areas or solve puzzles.
    Collides with the player and enemy sprites.
    The block is not affected by gravity and does not move.

    Attributes:
        image (pygame.Surface): The image representing the placeable block.
        rect (pygame.Rect): The rectangle representing the placeable block's position and size.
    """

    def __init__(self, x=0, y=0):
        """ Initialize the Placeable sprite.

        Args:
            x (int): The initial x world position of the placeable block.
            y (int): The initial y world position of the placeable block.
        """
        super().__init__()

        self.image = load_image("pl_block_placeable.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
