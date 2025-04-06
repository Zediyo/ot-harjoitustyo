import pygame

from scenes.scene import Scene
from ui.button import Button


class LevelEditor(Scene):

    def __init__(self):
        super().__init__()
        self._font = pygame.font.SysFont("Arial", 24)
        self._buttons = {}

        self._init_buttons()

    def _init_buttons(self):
        back_button = Button("Back", self._font, 540, 300, 200, 50)

        self._buttons = {
            "back": (back_button, "mainmenu"),
        }

    def draw(self, display):
        res = self._font.render(
            "Nothing here yet. (click to go back)", True, (255, 128, 64))
        display.blit(res, (540, 200))

    def input_mouse(self, click, pos):
        self._next_scene = "mainmenu"
        self._end_scene = True

    def update(self, dt, mouse_pos):
        pass
