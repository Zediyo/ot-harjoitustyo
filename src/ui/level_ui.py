import pygame

from ui.button import Button


class LevelUI:
    def __init__(self, name):
        self.name = name
        self._font = pygame.font.Font(None, 24)

        self.back_button = Button("Back", self._font, 1180, 20, 60, 30)

    def draw(self, display, item):
        text = f"Level: {self.name}     Inventory: {item}"
        text_surface = self._font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(display.get_width() // 2, 20))
        display.blit(text_surface, text_rect)

        self.back_button.draw(display)

    def is_back_clicked(self, mouse_pos):
        if self.back_button.is_clicked(mouse_pos):
            return True
        return False

    def update(self, dt, mouse_pos):
        self.back_button.update(mouse_pos)
