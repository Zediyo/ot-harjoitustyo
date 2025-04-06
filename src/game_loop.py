import pygame

from scenes.main_menu import MainMenu
from scenes.level import Level
from scenes.level_editor import LevelEditor

import constants


class GameLoop:
    def __init__(self, scene, renderer, user_input, clock):
        self._scene = scene
        self._renderer = renderer
        self._user_input = user_input
        self._clock = clock

    def start(self):
        while True:
            if not self._handle_events():
                break

            self._handle_input()

            self._scene.update(self._clock.get_dt(),
                               self._user_input.get_mouse_pos())

            self._render()

            self._clock.tick(240)

            if self._scene.is_done():
                if not self._change_scene(self._scene.get_next_scene()):
                    break

    def _handle_events(self):
        for event in self._user_input.get_events():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._scene.input_mouse("left", event.pos)
                if event.button == 3:
                    self._scene.input_mouse("right", event.pos)
            elif event.type == pygame.QUIT:
                return False

        return True

    def _handle_input(self):
        keys = self._user_input.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._scene.input_key("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._scene.input_key("right")
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self._scene.input_key("jump")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self._scene.input_key("down")

    def _render(self):
        self._renderer.render()

    def _change_scene(self, new_scene):
        if new_scene is None:
            return False

        self._scene.cleanup()

        if new_scene == "mainmenu":
            new_scene = MainMenu()
        elif new_scene == "level":
            new_scene = Level(constants.TEST_LEVEL)
        elif new_scene == "editor":
            new_scene = LevelEditor()
        else:
            return False

        self._renderer.set_scene(new_scene)
        self._scene = new_scene

        return True
