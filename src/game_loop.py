import pygame

from constants import SceneName, InputAction
from scenes.main_menu import MainMenu
from scenes.level import Level
from scenes.level_editor import LevelEditor
from scenes.level_list import LevelList
from scenes.end_screen import EndScreen

from game.level_data import LevelData
from game.endscreen_data import EndScreenData


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
                    self._scene.input_mouse(InputAction.MOUSE_LEFT, event.pos)
                if event.button == 3:
                    self._scene.input_mouse(InputAction.MOUSE_RIGHT, event.pos)
                if event.button == 4:
                    self._scene.input_mouse(
                        InputAction.MOUSE_SCROLL_UP, event.pos)
                if event.button == 5:
                    self._scene.input_mouse(
                        InputAction.MOUSE_SCROLL_DOWN, event.pos)
            elif event.type == pygame.QUIT:
                return False

        # for text fields
        self._scene.input_raw(events)

        return True

    def _handle_input(self):
        keys = self._user_input.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._scene.input_key(InputAction.LEFT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._scene.input_key(InputAction.RIGHT)
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self._scene.input_key(InputAction.JUMP)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self._scene.input_key(InputAction.DOWN)

        mouse = self._user_input.get_mouse_pressed()
        if mouse[0]:
            self._scene.input_mouse_hold(
                InputAction.MOUSE_LEFT, self._user_input.get_mouse_pos())
        if mouse[2]:
            self._scene.input_mouse_hold(
                InputAction.MOUSE_RIGHT, self._user_input.get_mouse_pos())

    def _render(self):
        self._renderer.render()

    def _change_scene(self, new_scene, new_scene_data):
        self._scene.cleanup()

        scene = self._get_new_scene(new_scene, new_scene_data)

        if scene is None:
            return False

        self._renderer.set_scene(scene)
        self._scene = scene

        return True

    def _get_new_scene(self, new_scene, new_scene_data):
        if new_scene is None:
            return None

        scene_map = {
            SceneName.MAIN_MENU: (MainMenu, None),
            SceneName.LEVEL_LIST: (LevelList, lambda data: isinstance(data, bool) or data is None),
            SceneName.LEVEL: (Level, LevelData.is_valid),
            SceneName.EDITOR: (LevelEditor, LevelData.is_valid),
            SceneName.END_SCREEN: (EndScreen, EndScreenData.is_valid),
        }

        result = scene_map.get(new_scene)

        if result is None:
            return None

        scene_class, validator = result

        if validator and not validator(new_scene_data):
            return None

        return scene_class(new_scene_data) if new_scene_data is not None else scene_class()
