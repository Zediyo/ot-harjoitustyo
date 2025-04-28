import pygame

from scenes.main_menu import MainMenu
from scenes.level import Level
from scenes.level_editor import LevelEditor
from scenes.level_list import LevelList
from scenes.end_screen import EndScreen


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
                if not self._change_scene(
                    self._scene.get_next_scene(),
                    self._scene.get_next_scene_data()
                ):
                    break

    def _handle_events(self):
        events = self._user_input.get_events()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._scene.input_mouse("left", event.pos)
                if event.button == 3:
                    self._scene.input_mouse("right", event.pos)
                if event.button == 4:
                    self._scene.input_mouse("scroll_up", event.pos)
                if event.button == 5:
                    self._scene.input_mouse("scroll_down", event.pos)
            elif event.type == pygame.QUIT:
                return False

        # for text fields
        self._scene.input_raw(events)

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

        mouse = self._user_input.get_mouse_pressed()
        if mouse[0]:
            self._scene.input_mouse_hold(
                "left", self._user_input.get_mouse_pos())
        if mouse[2]:
            self._scene.input_mouse_hold(
                "right", self._user_input.get_mouse_pos())

    def _render(self):
        self._renderer.render()

    def _change_scene(self, new_scene, new_scene_data):
        if new_scene is None:
            return False

        self._scene.cleanup()

        if new_scene == "mainmenu":
            new_scene = MainMenu()
        elif new_scene == "level_list":
            new_scene = LevelList(new_scene_data)
        elif new_scene == "level":
            if not self._level_data_exists(new_scene_data):
                return False
            new_scene = Level(new_scene_data)
        elif new_scene == "editor":
            if not self._level_data_exists(new_scene_data):
                return False
            new_scene = LevelEditor(new_scene_data)
        elif new_scene == "endscreen":
            if not self._end_data_exists(new_scene_data):
                return False
            new_scene = EndScreen(new_scene_data)
        else:
            return False

        self._renderer.set_scene(new_scene)
        self._scene = new_scene

        return True

    def _level_data_exists(self, data):
        if ("data" not in data or "id" not in data or "name" not in data):
            return False
        return True

    def _end_data_exists(self, data):
        if ("level" not in data or "timer" not in data):
            return False

        if not self._level_data_exists(data["level"]):
            return False

        return True
