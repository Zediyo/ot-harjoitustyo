import pygame
import pygame.freetype
import constants

from scenes.scene import Scene
from scenes.level import Level
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
            "play": (play_button, "level"),
            "editor": (editor_button, "level"),
            "exit": (exit_button, None)
        }


    def draw(self, display):
        for (button, _) in self._buttons.values():
            button.draw(display)

    def input_mouse(self, click, pos):
        for (button, next_scene) in self._buttons.values():
            if button.is_clicked(pos):
                if next_scene == "level":
                    self._next_scene = Level(constants.TEST_LEVEL)
                else:
                    self._next_scene = None

                self._end_scene = True
                break

    def update(self, dt, mouse_pos):
        for (button, _) in self._buttons.values():
            button.update(mouse_pos)



