""" User Input Wrapper for Pygame"""
import pygame


class UserInput:
    """ A simple wrapper around Pygame's user input functionality. """

    def get_events(self):
        """ Get all user input events from Pygame.

        Returns:
            list[pygame.event.Event]: List of Pygame events.
        """
        return pygame.event.get()

    def get_pressed(self):
        """ Get the current state of all keyboard buttons.

        Returns:
            list[bool]: List of boolean values representing the state of each key.
        """
        return pygame.key.get_pressed()

    def get_mouse_pos(self):
        """ Get the current position of the mouse cursor.

        Returns:
            tuple[int, int]: The current mouse position (x, y) on screen.
        """
        return pygame.mouse.get_pos()

    def get_mouse_pressed(self):
        """ Get the current state of mouse buttons.

        Returns:
            list[bool]: List of boolean values representing the state of each mouse button.
        """
        return pygame.mouse.get_pressed()
