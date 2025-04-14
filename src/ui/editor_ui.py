import pygame

from ui.button import Button
import constants


class EditorUI:
    def __init__(self, name):
        self.name = name
        self._font = pygame.font.Font(None, 24)

        self._back_button = Button("Back", self._font, 1180, 20, 60, 30)
        self._save_button = Button("Save", self._font, 1110, 20, 60, 30)

    def draw(self, display, item, required):
        text1 = (
            f"Level: {self.name:<33}"
            f"Current: {self._get_item_name(item):<10}"
        )
        text2 = (
            f"1: {self._get_item_name(1):<15}"
            f"2: {self._get_item_name(2):<15}"
            f"3: {self._get_item_name(3):<15}"
            f"4: {self._get_item_name(4):<15}"
            f"5: {self._get_item_name(5):<15}"
        )

        self._save_button.set_active(True)

        if required["spawn"]:
            spawn_text = "Spawn"
            spawn_color = (0, 255, 0)
        else:
            spawn_text = "No Spawn"
            spawn_color = (255, 0, 0)
            self._save_button.set_active(False)
        if required["end"]:
            end_color = (0, 255, 0)
            end_text = "End"
        else:
            end_color = (255, 0, 0)
            end_text = "No End"
            self._save_button.set_active(False)

        spawn_surface = self._font.render(spawn_text, True, spawn_color)
        spawn_rect = spawn_surface.get_rect(topleft=(500, 50))
        end_surface = self._font.render(end_text, True, end_color)
        end_rect = end_surface.get_rect(topleft=(500, 70))

        text_surface1 = self._font.render(text1, True, (255, 255, 255))
        text_rect1 = text_surface1.get_rect(topleft=(500, 10))
        text_surface2 = self._font.render(text2, True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(topleft=(500, 30))

        display.blit(text_surface1, text_rect1)
        display.blit(text_surface2, text_rect2)
        display.blit(spawn_surface, spawn_rect)
        display.blit(end_surface, end_rect)

        self._back_button.draw(display)
        self._save_button.draw(display)

    def is_back_clicked(self, mouse_pos):
        return self._back_button.is_clicked(mouse_pos)

    def is_save_clicked(self, mouse_pos):
        return self._save_button.is_clicked(mouse_pos)

    def update(self, mouse_pos):
        self._back_button.update(mouse_pos)
        self._save_button.update(mouse_pos)

    def _get_item_name(self, item):
        if item == constants.TILE_BLOCK:
            return "Block"
        elif item == constants.TILE_PLACEABLE:
            return "Placeable"
        elif item == constants.TILE_ENEMY:
            return "Enemy"
        elif item == constants.TILE_SPAWN:
            return "Spawn"
        elif item == constants.TILE_END:
            return "End"
