"""ConfirmBox UI component for yes/no confirmations."""

import pygame
from ui.button import Button
from typing import Callable


class ConfirmBox:
    """ A confirmation dialog box with yes/no buttons. """

    _COLOR_STATIC_TEXT = (255, 150, 25)
    _COLOR_YES = (0, 255, 0)
    _COLOR_NO = (255, 0, 0)
    _COLOR_TEXT = (200, 50, 50)

    def __init__(self, font, x, y, width, height):
        """Initialize the ConfirmBox.

        Args:
            font (pygame.font.Font): Font used to render text.
            x (int): X position of the box.
            y (int): Y position of the box.
            width (int): Width of the box.
            height (int): Height of the box.
        """
        self._font = font
        self._rect = pygame.Rect(x, y, width, height)

        self._static_text = font.render(
            "Are you sure?", True, self._COLOR_STATIC_TEXT)
        self._static_text_rect = self._static_text.get_rect(
            center=(self._rect.centerx, self._rect.centery - 46))

        self._yes_button = Button(
            "Yes", font,
            (x, y + height // 2, width // 2 - 10, height // 2),
            text_color=self._COLOR_YES
        )
        self._no_button = Button(
            "No", font,
            (x + width // 2 + 10, y + height // 2, width // 2 - 10, height // 2),
            text_color=self._COLOR_NO
        )

        self._text = None
        self._active = False
        self._action = None

    def draw(self, display):
        """Draw the confirm box and its contents.

        Args:
            display (pygame.Surface): The display surface to draw to.
        """
        if not self._active:
            return

        if self._text:
            text_surface = self._font.render(
                self._text, True, self._COLOR_TEXT)
            text_rect = text_surface.get_rect(
                center=(self._rect.centerx, self._rect.centery - 20)
            )
            display.blit(text_surface, text_rect)

        display.blit(self._static_text, self._static_text_rect)
        self._yes_button.draw(display)
        self._no_button.draw(display)

    def handle_events(self, events):
        """Handle mouse events for clicking buttons or hover states.

        Args:
            events (list[pygame.event.Event]): List of Pygame events.
        """
        if not self._active:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._yes_button.is_clicked(event.pos):
                    self.confirm()
                elif self._no_button.is_clicked(event.pos):
                    self.cancel()
            elif event.type == pygame.MOUSEMOTION:
                self._yes_button.update(event.pos)
                self._no_button.update(event.pos)
        return

    def set_text(self, text):
        """Set the dynamic text displayed inside the box.

        Args:
            text (str): Text to display above the buttons.
        """
        self._text = text

    def set_action(self, action: Callable):
        """Set the action to execute if 'Yes' is clicked.

        Args:
            action (Callable): Function to call on confirmation.
        """
        self._action = action

    def confirm(self):
        """Trigger the confirmation action and deactivate the box."""
        self._yes_button.update((-1, -1))  # clear hover
        self._active = False
        if self._action:
            self._action()

    def cancel(self):
        """Cancel the confirmation and deactivate the box."""
        self._no_button.update((-1, -1))  # clear hover
        self._active = False

    def set_active(self, active):
        """Enable or disable the confirm box.

        Args:
            active (bool): Whether the box should be visible and interactive.
        """
        self._active = active

    def is_active(self):
        """Return whether the confirm box is currently active.

        Returns:
            bool: True if active, False otherwise.
        """
        return self._active
