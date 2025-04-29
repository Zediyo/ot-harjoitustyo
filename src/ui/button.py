import pygame
from typing import Callable


class Button:
    def __init__(
        self, text, font, rect: tuple[int, int, int, int],
        hover_color=(200, 200, 200),
        bg_color=(64, 64, 64), text_color=(255, 150, 25),
        preview=None,
        on_click: Callable | None = None
    ):
        """Create a button."""
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
        # check if button is on screen.
        y_bottom, y_top = self.get_y_minmax()
        if y_bottom + offset_y < 0 or y_top + offset_y > display.get_height():
            return

        if not self._active:
            return

        self._rect.y += offset_y
        pygame.draw.rect(display, self._color, self._rect, border_radius=5)
        self._rect.y -= offset_y

        text_rect = self._text.get_rect(center=self._rect.center)
        text_rect.y += offset_y
        display.blit(self._text, text_rect)

        if self._preview:
            preview_rect = self._preview.get_rect()
            preview_rect.midleft = self._rect.midright
            preview_rect.x += 10
            preview_rect.y += offset_y
            display.blit(self._preview, preview_rect)

        if self._above_text:
            above_text_rect = self._above_text.get_rect()
            above_text_rect.midbottom = self._rect.midtop
            above_text_rect.y -= 5
            above_text_rect.y += offset_y
            display.blit(self._above_text, above_text_rect)

    def update(self, mouse_pos, offset_y=0):
        if not self._active:
            self._color = self._bg_color
            return

        if self._rect.collidepoint((mouse_pos[0], mouse_pos[1] - offset_y)):
            self._color = self._hover_color
        else:
            self._color = self._bg_color

    def is_clicked(self, mouse_pos, offset_y=0):
        if not self._active:
            return False

        return self._rect.collidepoint((mouse_pos[0], mouse_pos[1] - offset_y))

    def click(self):
        if self._on_click:
            self._on_click()

    def set_on_click(self, on_click: Callable):
        """Set the function to call when the button is clicked.

        Args:
            on_click (Callable): The function to call when the button is clicked.
        """
        self._on_click = on_click

    def set_above_text(self, text, color):
        self._above_text = self._font.render(text, True, color)

    def set_text(self, text):
        self._text = self._font.render(text, True, self._text_color)

    def get_y_minmax(self):
        if self._preview:
            height = max(self._preview.get_height(), self._rect.height)
            return self._rect.centery + height // 2, self._rect.centery - height // 2

        return self._rect.bottom, self._rect.top

    def set_active(self, active):
        self._active = active
