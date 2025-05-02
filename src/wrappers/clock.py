""" Clock wrapper for Pygame """
import pygame


class Clock:
    """ A simple wrapper around Pygame's clock functionality. """

    def __init__(self):
        """ Initialize the clock. """
        self._clock = pygame.time.Clock()

    def tick(self, fps):
        """ Tick the clock with the specified frames per second.

        Args:
            fps (int): The desired frames per second.
        """
        self._clock.tick(fps)

    def get_dt(self):
        """ Get the time since the last tick in seconds.

        Returns:
            float: The time since the last tick in seconds.
        """
        return self._clock.get_time() / 1000.0
