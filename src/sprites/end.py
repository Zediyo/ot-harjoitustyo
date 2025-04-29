""" Contains the End sprite class used for the level goal or end."""

import pygame

from tools.asset_helpers import load_image


class End(pygame.sprite.Sprite):
    """ A tile representing the end point of a level.

    Used to detect when the player has reached the end of a level.
    Does not collide with the player or other objects.

    Attributes:
        image (pygame.Surface): The image representing the end point.
        rect (pygame.Rect): The rectangle representing the end point's position and size.
    """

    def __init__(self, x=0, y=0):
        """ Initialize the End sprite.

        Args:
            x (int, optional): The x world coordinate of the end point. Defaults to 0.
            y (int, optional): The y world coordinate of the end point. Defaults to 0.
        """
        super().__init__()

        self.image = load_image("pl_end.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
