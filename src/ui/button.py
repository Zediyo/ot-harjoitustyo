"""Button class for creating buttons for the game UI."""

import pygame
from typing import Callable


class Button:
    """A clickable button UI element with optional hover state and preview image."""

    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 rect: tuple[int, int, int, int],
                 hover_color: tuple[int, int, int] = (200, 200, 200),
                 bg_color: tuple[int, int, int] = (64, 64, 64),
                 text_color: tuple[int, int, int] = (255, 150, 25),
                 preview: pygame.Surface | None = None,
                 on_click: Callable | None = None
                 ):
        """Initialize a new button.

        Args:
            text (str): The label to display on the button.
            font (pygame.font.Font): Font object used to render text.
            rect (tuple): Button position and size as (x, y, width, height).
            hover_color (tuple): Button color when hovered. Defaults to (200, 200, 200).
            bg_color (tuple): Default background color. Defaults to (64, 64, 64).
            text_color (tuple): Color of the button label. Defaults to (255, 150, 25).
            preview (pygame.Surface, optional): Optional preview image next to the button.
            on_click (Callable, optional): Function to call when the button is clicked.
        """
        self._rect = pygame.Rect(rect)
        self._font = font
        self._bg_color = bg_color
        self._hover_color = hover_color
        self._text_color = text_color
        self._color = bg_color
        self._preview = preview
        self._text = font.render(text, True, text_color)
        self._above_text = None

        self._active = True
        self._on_click = on_click

    def draw(self, display, offset_y=0):
        """Draw the button on the display surface.

        Args:
            display (pygame.Surface): Surface to draw the button on.
            offset_y (int): Vertical offset for scrolling effects. Defaults to 0.
        """
        y_bottom, y_top = self.get_y_minmax()
        if y_bottom + offset_y < 0 or y_top + offset_y > display.get_height():
            return

        if not self._active:
            return

        rect = self._rect.copy()
        rect.y += offset_y

        pygame.draw.rect(display, self._color, rect, border_radius=5)

        text_rect = self._text.get_rect(center=rect.center)
        display.blit(self._text, text_rect)

        if self._preview:
            preview_rect = self._preview.get_rect()
            preview_rect.midleft = rect.midright
            preview_rect.x += 10
            display.blit(self._preview, preview_rect)

        if self._above_text:
            above_text_rect = self._above_text.get_rect()
            above_text_rect.midbottom = rect.midtop
            above_text_rect.y -= 5
            display.blit(self._above_text, above_text_rect)

    def update(self, mouse_pos, offset_y=0):
        """Update the hover color based on mouse position.

        Args:
            mouse_pos (tuple): Mouse position as (x, y).
            offset_y (int): Vertical scroll offset. Defaults to 0.
        """
        if not self._active:
            self._color = self._bg_color
            return

        if self._rect.collidepoint((mouse_pos[0], mouse_pos[1] - offset_y)):
            self._color = self._hover_color
        else:
            self._color = self._bg_color

    def is_clicked(self, mouse_pos, offset_y=0):
        """Check if the button is clicked at a given mouse position.

        Args:
            mouse_pos (tuple): Mouse position as (x, y).
            offset_y (int): Vertical scroll offset. Defaults to 0.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        if not self._active:
            return False

        return self._rect.collidepoint((mouse_pos[0], mouse_pos[1] - offset_y))

    def click(self):
        """Call the assigned on_click function."""
        if self._on_click:
            self._on_click()

    def set_on_click(self, on_click: Callable):
        """Set the function to call when the button is clicked.

        Args:
            on_click (Callable): The function to call when the button is clicked.
        """
        self._on_click = on_click

    def set_above_text(self, text, color):
        """Set optional text to render above the button.

        Args:
            text (str): The text to render.
            color (tuple): Color of the text.
        """
        self._above_text = self._font.render(text, True, color)

    def set_text(self, text):
        """Update the button label.

        Args:
            text (str): New label text.
        """
        self._text = self._font.render(text, True, self._text_color)

    def get_y_minmax(self):
        """Return the top and bottom Y values for the button area.

        Returns:
            tuple[int, int]: (bottom_y, top_y) values for layout checks.
        """
        if self._preview:
            height = max(self._preview.get_height(), self._rect.height)
            return self._rect.centery + height // 2, self._rect.centery - height // 2

        return self._rect.bottom, self._rect.top

    def set_active(self, active):
        """Enable or disable the button.

        Args:
            active (bool): Whether the button should respond to input and draw.
        """
        self._active = active
