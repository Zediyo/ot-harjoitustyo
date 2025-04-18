import pygame
from ui.button import Button


class ConfirmBox:

    def __init__(self, font, x, y, width, height):
        self._font = font
        self._rect = pygame.Rect(x, y, width, height)
        self._static_text = font.render("Are you sure?", True, (255, 150, 25))
        self._static_text_rect = self._static_text.get_rect(
            center=(self._rect.centerx, self._rect.centery - 46))
        self._text = "Delete map test_test_level12?"
        self._yes_button = Button("Yes", font, x, y + height //
                                  2, width // 2 - 10, height // 2, text_color=(0, 255, 0))
        self._no_button = Button("No", font, x + width // 2 + 10, y +
                                 height // 2, width // 2 - 10, height // 2, text_color=(255, 0, 0))
        self._active = False
        self._data = None

    def draw(self, display):
        if not self._active:
            return

        if self._text:
            text_surface = self._font.render(self._text, True, (200, 50, 50))
            text_rect = text_surface.get_rect(
                center=(self._rect.centerx, self._rect.centery - 20))
            display.blit(text_surface, text_rect)

        display.blit(self._static_text, self._static_text_rect)
        self._yes_button.draw(display)
        self._no_button.draw(display)

    def handle_events(self, events):
        if not self._active:
            return None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self._yes_button.is_clicked(event.pos):
                        self._yes_button.update((-1, -1))
                        self._active = False
                        return self._data
                    elif self._no_button.is_clicked(event.pos):
                        self._no_button.update((-1, -1))
                        self._active = False
            elif event.type == pygame.MOUSEMOTION:
                self._yes_button.update(event.pos)
                self._no_button.update(event.pos)
        return None

    def set_text(self, text):
        self._text = text

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_active(self, active):
        self._active = active

    def is_active(self):
        return self._active
