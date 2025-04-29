import pygame

from ui.button import Button
from tools.font_manager import FontManager


class LevelUI:
    def __init__(self, name):
        self.name = name
        self._font = FontManager.get_font()

        self.back_button = Button("Back", self._font, (1180, 20, 60, 30))

    def draw(self, display, item, timer):
        best_time = timer.get_best_time()
        time = timer.get_time()

        record = f"{best_time:<10.2f}" if best_time != None else "--:--"
        text = (
            f"Level: {self.name:<33}"
            f"Inventory: {item:<10}"
            f"Best Time: {record:<10}"
            f"Time: {time:<10.2f}"
        )
        text_surface = self._font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            topleft=(500, 20))
        display.blit(text_surface, text_rect)

        self.back_button.draw(display)

    def is_back_clicked(self, mouse_pos):
        if self.back_button.is_clicked(mouse_pos):
            return True
        return False

    def update(self, mouse_pos):
        self.back_button.update(mouse_pos)
