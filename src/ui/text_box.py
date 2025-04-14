import pygame


class TextBox:

    def __init__(self, font, x, y, width, height, hover_color=(200, 200, 200), bg_color=(64, 64, 64), text_color=(255, 150, 25), border_color=(0, 0, 0), max_length=32):
        self._rect = pygame.Rect(x, y, width, height)
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

    def draw(self, display):
        text = "Enter text..."if not self._text and not self._active else self._text
        color = self._text_color if self._active else (100, 100, 100)

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
        return self._rect.collidepoint(mouse_pos)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self._active:
                    if event.key == pygame.K_BACKSPACE:
                        self._text = self._text[:-1]
                    elif event.key == pygame.K_RETURN:
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
        return self._text

    def set_error_text(self, error_text):
        self._error_text = error_text

    def clear_error_text(self):
        self._error_text = None
