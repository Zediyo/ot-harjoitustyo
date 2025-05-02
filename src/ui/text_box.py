"""TextBox UI component for user text input."""

import pygame
from typing import Callable


class TextBox:
    """A text input box for user input."""

    _COLOR_INACTIVE = (100, 100, 100)

    def __init__(self,
                 font: pygame.font.Font,
                 rect: tuple[int, int, int, int],
                 hover_color: tuple[int, int, int] = (200, 200, 200),
                 bg_color: tuple[int, int, int] = (64, 64, 64),
                 text_color: tuple[int, int, int] = (255, 150, 25),
                 border_color: tuple[int, int, int] = (0, 0, 0),
                 max_length: int = 32,
                 on_submit: Callable | None = None,
                 ):
        """Initialize the text box.

        Args:
            font (pygame.font.Font): Font used for rendering text.
            rect (tuple[int, int, int, int]): Position and size of the text box.
            hover_color (tuple[int, int, int]): Background color on mouse hover. Defaults to (200, 200, 200).
            bg_color (tuple[int, int, int]): Normal background color. Defaults to (64, 64, 64).
            text_color (tuple[int, int, int]): Text color. Defaults to (255, 150, 25).
            border_color (tuple[int, int, int]): Border color when active. Defaults to (0, 0, 0).
            max_length (int): Maximum number of characters allowed.
            on_submit (Callable | None): Function to call when Enter is pressed.
        """
        self._rect = pygame.Rect(rect)
        self._font = font
        self._bg_color = bg_color
        self._hover_color = hover_color
        self._text_color = text_color
        self._color = bg_color
        self._border_color = border_color
        self._text = ""
        self._active = False
        self._overflow_offset = 0
        self._max_length = max_length
        self._error_text = None
        self._on_submit = on_submit

    def draw(self, display):
        """Render the text box and any error message.

        Args:
            display (pygame.Surface): The surface to draw on.
        """
        text = "Enter text..."if not self._text and not self._active else self._text
        color = self._text_color if self._active else self._COLOR_INACTIVE

        pygame.draw.rect(display, self._color, self._rect, border_radius=5)

        if self._active:
            pygame.draw.rect(display, self._border_color,
                             self._rect, border_radius=5, width=2)

        rendered_text = self._font.render(
            text[self._overflow_offset:], True, color)
        display.blit(rendered_text, (self._rect.x + 5, self._rect.y + 5))

        if self._error_text:
            error_surface = self._font.render(
                self._error_text, True, (255, 0, 0))
            display.blit(error_surface, (self._rect.x + 5,
                         self._rect.y + self._rect.height + 5))

    def is_clicked(self, mouse_pos):
        """Check if a clicked point is within the textbox.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse.

        Returns:
            bool: True if the box was clicked.
        """
        return self._rect.collidepoint(mouse_pos)

    def handle_events(self, events):
        """Handle keyboard and mouse events for the textbox.

        Args:
            events (list[pygame.event.Event]): Events to process.

        Returns:
            str | None: The text if submitted, otherwise None.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and self._active:
                if event.key == pygame.K_BACKSPACE:
                    self._text = self._text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self._on_submit:
                        self._on_submit(self._text)
                    return self._text
                elif len(self._text) < self._max_length:
                    self._text += event.unicode

                self._update_overflow_offset()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self._rect.collidepoint(event.pos):
                        self._active = True
                    else:
                        self._active = False
            elif event.type == pygame.MOUSEMOTION:
                if self._rect.collidepoint(event.pos):
                    self._color = self._hover_color
                else:
                    self._color = self._bg_color
        return None

    def _update_overflow_offset(self):
        """Adjusts overflow to keep the end of text visible if too long."""
        if self._overflow_offset >= len(self._text):
            self._overflow_offset = 0

        text_width = self._font.render(
            self._text[self._overflow_offset:], True, self._text_color).get_width()
        box_width = self._rect.width - 10

        if text_width > box_width:
            while text_width > box_width and self._overflow_offset < len(self._text):
                self._overflow_offset += 1
                text_width = self._font.render(
                    self._text[self._overflow_offset:], True, self._text_color).get_width()
        elif text_width < box_width:
            while self._overflow_offset > 0:
                self._overflow_offset -= 1
                text_width = self._font.render(
                    self._text[self._overflow_offset:], True, self._text_color).get_width()

                if text_width > box_width:
                    self._overflow_offset += 1
                    break

    def get_text(self):
        """Get the current text in the box.

        Returns:
            str: The current text.
        """
        return self._text

    def set_error_text(self, error_text):
        """Display error text below the textbox.

        Args:
            error_text (str): Error message to show.
        """
        self._error_text = error_text

    def clear_error_text(self):
        """Clear the error text."""
        self._error_text = None
