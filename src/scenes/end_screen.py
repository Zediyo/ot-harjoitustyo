import pygame

from scenes.scene import Scene
from ui.button import Button

from tools.preview_generator import generate_level_preview

from constants import SceneName, InputAction
from game.endscreen_data import EndScreenData


class EndScreen(Scene):

    def __init__(self, data: EndScreenData):
        super().__init__()
        self._font = pygame.font.SysFont("Arial", 24)
        self._buttons = {}
        self._texts = []

        self._data = data

        self._preview = generate_level_preview(
            data.level.data, size=(600, 300))

        self._init_buttons()
        self._init_texts()

    def _init_buttons(self):
        retry_button = Button("Retry", self._font, 420, 500, 200, 50)
        back_button = Button("Menu", self._font, 660, 500, 200, 50)

        self._buttons = {
            "retry": (retry_button, SceneName.LEVEL, self._data.level),
            "back": (back_button, SceneName.LEVEL_LIST, False),
        }

    def _init_texts(self):
        time = self._data.timer.get_time()
        time_text = f"Time: {time:.2f}"

        time_surface = None
        best_time_surface = None

        if self._data.timer.is_best_time():
            best_time_surface = self._font.render(time_text, True, (0, 255, 0))
            time_surface = self._font.render(
                "New Best Time!", True, (0, 255, 0))
        else:
            best_time = self._data.timer.get_best_time()
            best_time_text = f"Best Time: {best_time:.2f}"

            best_time_surface = self._font.render(
                best_time_text, True, (255, 255, 255))
            time_surface = self._font.render(time_text, True, (255, 0, 0))

        best_time_rect = best_time_surface.get_rect(center=(640, 420))
        time_rect = time_surface.get_rect(center=(640, 460))

        self._texts.append((best_time_surface, best_time_rect))
        self._texts.append((time_surface, time_rect))

    def draw(self, display):
        display.fill((128, 128, 128))

        for (button, _, _) in self._buttons.values():
            button.draw(display)

        preview_rect = self._preview.get_rect()
        preview_rect.midtop = (display.get_width() // 2, 100)
        display.blit(self._preview, preview_rect)

        for text, pos in self._texts:
            display.blit(text, pos)

    def input_mouse(self, click, pos):
        if click != InputAction.MOUSE_LEFT:
            return

        for button, next_scene, next_scene_data in self._buttons.values():
            if button.is_clicked(pos):
                self.set_next_scene(next_scene, next_scene_data)
                break

    def update(self, dt, mouse_pos):
        for button, *_ in self._buttons.values():
            button.update(mouse_pos)
