import pygame

from scenes.scene import Scene
from ui.button import Button

from tools.db import get_all_levels, get_all_best_times
from tools.preview_generator import generate_level_preview
import constants


class LevelList(Scene):
    _SCROLL_SPEED = 50

    def __init__(self, button_action=None):
        super().__init__()
        self._font = pygame.font.SysFont("Arial", 24)
        self._buttons = {}

        self._button_action = "editor" if button_action is not None and \
            button_action == "editor" else "level"

        self._back_button = Button("Back", self._font, 1000, 25, 200, 50)
        self._init_scrollable_buttons()

        self._scroll = 0

    def _init_scrollable_buttons(self):
        levels = get_all_levels()
        best_times = get_all_best_times()

        for i, (level_id, level_name, level_data) in enumerate(levels):
            preview = generate_level_preview(level_data, (300, 150))

            button = Button(f"{level_id}: {level_name}", self._font,
                            200, 100 + (i * 160), 150, 50, preview=preview)

            best_time = best_times.get(level_id, None)
            if best_time is not None:
                button.set_above_text(
                    f"Best Time: {best_time:.2f}", (50, 200, 50))
            else:
                button.set_above_text("Best Time: --:--", (200, 50, 50))

            self._buttons[level_name] = (
                button, self._button_action, {
                    "id": level_id,
                    "name": level_name,
                    "data": level_data
                }
            )

    def draw(self, display):
        display.fill((128, 128, 128))

        self._back_button.draw(display)

        for (button, _, _) in self._buttons.values():
            button.draw(display, self._scroll)

    def input_mouse(self, click, pos):
        if click == "left":
            if self._back_button.is_clicked(pos):
                self.set_next_scene("mainmenu")
                return

            for (button, next_scene, next_scene_data) in self._buttons.values():
                if button.is_clicked(pos, self._scroll):
                    self.set_next_scene(next_scene, next_scene_data)
                    break
        elif click == "scroll_up":
            self._scroll += self._SCROLL_SPEED
            self._scroll = min(self._scroll, 0)
        elif click == "scroll_down" and len(self._buttons) > 4:
            self._scroll -= self._SCROLL_SPEED
            self._scroll = max(self._scroll, -len(self._buttons)
                               * 160 + constants.SCREEN_HEIGHT - 100)

    def update(self, dt, mouse_pos):
        self._back_button.update(mouse_pos)
        for (button, _, _) in self._buttons.values():
            button.update(mouse_pos, self._scroll)
