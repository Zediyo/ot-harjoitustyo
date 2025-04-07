import pygame

from scenes.scene import Scene
from ui.button import Button


class MainMenu(Scene):

    def __init__(self):
        super().__init__()
        self._font = pygame.font.SysFont("Arial", 24)
        self._buttons = {}

        self._init_buttons()

    def _init_buttons(self):
        play_button = Button("Play", self._font, 540, 200, 200, 50)
        editor_button = Button("Editor", self._font, 540, 300, 200, 50)
        exit_button = Button("Exit", self._font, 540, 400, 200, 50)

        self._buttons = {
            "play": (play_button, "level_list", "level"),
            "editor": (editor_button, "level_list", "editor"),
            "exit": (exit_button, None, None)
        }

    def draw(self, display):
        display.fill((128, 128, 128))

        for (button, _, _) in self._buttons.values():
            button.draw(display)

    def input_mouse(self, click, pos):
        if click != "left":
            return

        for (button, next_scene, next_scene_data) in self._buttons.values():
            if button.is_clicked(pos):
                self._next_scene = next_scene
                self._end_scene = True
                self._next_scene_data = next_scene_data
                break

    def update(self, dt, mouse_pos):
        for (button, _, _) in self._buttons.values():
            button.update(mouse_pos)
