import pygame


class Button:
    def __init__(self, text, font, x, y, width, height, hover_color=(200, 200, 200), bg_color=(64, 64, 64), text_color=(255, 150, 25), preview=None):
        self._rect = pygame.Rect(x, y, width, height)
        self._font = font
        self._bg_color = bg_color
        self._hover_color = hover_color
        self._text_color = text_color
        self._color = bg_color
        self._preview = preview
        self._text = font.render(text, True, text_color)
        self._above_text = None

    def draw(self, display, offset_y=0):
        if self._rect.bottom + offset_y < 0 or self._rect.top + offset_y > display.get_height():
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
        if self._rect.collidepoint((mouse_pos[0], mouse_pos[1] - offset_y)):
            self._color = self._hover_color
        else:
            self._color = self._bg_color

    def is_clicked(self, mouse_pos, offset_y=0):
        return self._rect.collidepoint((mouse_pos[0], mouse_pos[1] - offset_y))

    def set_above_text(self, text, color):
        self._above_text = self._font.render(text, True, color)
