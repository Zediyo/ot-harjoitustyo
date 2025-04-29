""" Contains the Block sprite class, used for basic static tiles. """

import pygame

from tools.asset_helpers import load_image


class Block(pygame.sprite.Sprite):
    """ A basic static solid tile used in the game.

    Does not have any special properties or behaviors.
    Collides with the player and other objects.

    Attributes:
        image (pygame.Surface): The image representing the block.
        rect (pygame.Rect): The rectangle representing the block's position and size.
    """

    def __init__(self, x=0, y=0):
        """ Initialize the Block sprite.

        Args:
            x (int, optional): The x world coordinate of the block. Defaults to 0.
            y (int, optional): The y world coordinate of the block. Defaults to 0.
        """
        super().__init__()

        self.image = load_image("pl_block.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
