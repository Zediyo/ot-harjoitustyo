""" Contains the Timer class for tracking level completion times and best times."""

from tools.db import get_best_time, save_level_time


class Timer:
    """ Timer to track the level time and best time.

    Tracks the elapsed time for a level and compares it to the best time.
    If the current time is better than the best time, it is saved.
    """

    def __init__(self, level_id):
        """ Initialize the Timer class.

        Args:
            level_id (int): The ID of the level to track time for.
        """
        self._time = 0.0
        self._level_id = level_id
        self._best_time = get_best_time(level_id)

        self._active = False

    def reset_time(self):
        """ Reset the current elapsed time to zero."""
        self._time = 0.0

    def update(self, dt):
        """ Increment the elapsed time by the delta time if the timer is active.

        Args:
            dt (float): The delta time since the last frame.
        """
        if self._active:
            self._time += dt

    def get_time(self):
        """ Get the current elapsed time.

        Returns:
            float: The current elapsed time in seconds.
        """
        return self._time

    def is_best_time(self):
        """ Check if the current time is a new best time.

        Returns:
            bool: True if the current time is better than the best time, False otherwise.
        """
        return self._best_time is None or self._time < self._best_time

    def get_best_time(self):
        """ Get the best time for the level.

        Returns:
            float or None: The best time in seconds, or None if no best time is set.
        """
        return self._best_time

    def activate(self):
        """ Start or resume the timer."""
        self._active = True

    def deactivate(self):
        """ Pause the timer."""
        self._active = False

    def finish(self):
        """ Stop the timer and save the time if it's a new best time."""
        self._active = False
        if self.is_best_time():
            save_level_time(self._level_id, self._time)
