import pygame


class Button:
    def __init__(self, text, font, x, y, width, height, hover_color=(200, 200, 200), bg_color=(64, 64, 64), text_color=(255, 150, 25)):
        self._rect = pygame.Rect(x, y, width, height)
        self._text = text
        self._font = font
        self._bg_color = bg_color
        self._hover_color = hover_color
        self._text_color = text_color
        self._color = bg_color

    def draw(self, display):
        pygame.draw.rect(display, self._color, self._rect, border_radius=5)
        text_surface = self._font.render(self._text, True, self._text_color)
        text_rect = text_surface.get_rect(center=self._rect.center)
        display.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        if self._rect.collidepoint(mouse_pos):
            self._color = self._hover_color
        else:
            self._color = self._bg_color

    def is_clicked(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)
