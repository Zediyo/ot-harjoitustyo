""" Contains the main game loop and handles scene transitions. """

import pygame

from constants import SceneName, InputAction, Settings
from scenes.scene import Scene
from scenes.main_menu import MainMenu
from scenes.level import Level
from scenes.level_editor import LevelEditor
from scenes.level_list import LevelList
from scenes.end_screen import EndScreen

from game.level_data import LevelData
from game.endscreen_data import EndScreenData


class GameLoop:
    """ Main game loop class that handles the game execution and scene transitions.

    This class is responsible for managing the game loop, handling user input,
    updating the game state, rendering the scene, and transitioning between different scenes.
    """

    def __init__(self, scene, renderer, user_input, clock):
        """Initialize the game loop.

        Args:
            scene (Scene): The initial scene to be displayed.
            renderer (Renderer): The renderer responsible for drawing the scene.
            user_input (UserInput): The user input handler for capturing events.
            clock (Clock): The clock for managing frame rate and timing.
        """
        self._scene = scene
        self._renderer = renderer
        self._user_input = user_input
        self._clock = clock

    def start(self):
        """Start the game loop.

        Runs the main game loop, handling events, updating the scene, and rendering it.
        The loop continues until the game is exited or a scene transition requests a termination.
        """
        while True:
            if not self._handle_events():
                break

            self._handle_input()

            self._scene.update(self._clock.get_dt(),
                               self._user_input.get_mouse_pos())

            self._render()

            self._clock.tick(Settings.FPS)

            if self._scene.is_done():
                if not self._change_scene(
                    self._scene.get_next_scene(),
                    self._scene.get_next_scene_data()
                ):
                    break

    def _handle_events(self):
        """Process Pygame events and forward them to the active scene.

        Also forwards the events to the scene for raw input handling.
        Returns:
            bool: True if the game should continue running, False if it should exit.
        """
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
        """ Handle continuous input from the user and forward it to the active scene."""
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
        """Render the current scene using the renderer."""
        self._renderer.render()

    def _change_scene(self, new_scene, new_scene_data):
        """Change the current scene to a new one.

        Args:
            new_scene (SceneName): The name of the new scene to be displayed.
            new_scene_data (Any): Data passed to the new scene for initialization.

        Returns:
            bool: True if the scene was changed successfully, False otherwise.
        """
        self._scene.cleanup()

        scene = self._get_new_scene(new_scene, new_scene_data)

        if scene is None:
            return False

        self._renderer.set_scene(scene)
        self._scene = scene

        return True

    def _get_new_scene(self, new_scene: SceneName, new_scene_data) -> Scene | None:
        """Return a new scene instance based on the given scene name and its required data.

        Args:
            new_scene (SceneName): The name of the new scene to be created.
            new_scene_data (Any): Data passed to the new scene for initialization.

        Returns:
            Scene or None: A new scene instance or None if the scene is invalid.
        """
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
