import unittest
from unittest.mock import patch, MagicMock

import pygame
from scenes.scene import Scene
from scenes.main_menu import MainMenu
from scenes.level_list import LevelList
from scenes.level import Level
from scenes.level_editor import LevelEditor
from scenes.end_screen import EndScreen
from game_loop import GameLoop

from collections import defaultdict

import constants


class StubUserInput:
    def __init__(self, events=None, keys=None, mouse_pos=(0, 0), break_after=0):
        self.events = events if events is not None else []
        self.keys = keys if keys is not None else defaultdict(bool)
        self.mouse_pos = mouse_pos
        self.break_after = break_after

    def get_events(self):
        if self.break_after > 0:
            self.break_after -= 1
            if self.break_after == 0:
                self.events.append(pygame.event.Event(pygame.QUIT))
        return self.events

    def get_pressed(self):
        return self.keys

    def get_mouse_pos(self):
        return self.mouse_pos
    
class StubDisplay:
    def fill(self, color):
        pass

    def blit(self, surface, rect):
        pass

    def get_width(self):
        return 800

    def get_height(self):
        return 600


class StubRenderer:
    def __init__(self, scene=None):
        self.scene = scene
        self.display = StubDisplay()

    def render(self):
        self.scene.draw(self.display)

    def set_scene(self, scene):
        self.scene = scene

    def fill(self, color):
        pass


class StubClock:
    def tick(self, fps):
        pass

    def get_dt(self):
        return 0.1


class SimpleScene(Scene):
    def __init__(self):
        super().__init__()
        self.events = []
        self.one_loop = True

    def input_key(self, key):
        self.events.append(("input_key", key))

    def input_mouse(self, click, pos):
        self.events.append(("input_mouse", click, pos))

    def update(self, dt, mouse_pos):
        self.events.append(("update", dt, mouse_pos))

    def draw(self, display):
        self.events.append(("draw", display))

        if self.one_loop:
            self.set_next_scene("test")

        self.one_loop = True

    def is_done(self):
        self.events.append(("is_done"))
        return super().is_done()

    def get_next_scene(self):
        self.events.append(("get_next_scene"))
        return super().get_next_scene()

    def get_next_scene_data(self):
        self.events.append(("get_next_scene_data"))
        return super().get_next_scene_data()

    def cleanup(self):
        self.events.append(("cleanup"))


class TestGameLoop(unittest.TestCase):
    def setUp(self):
        self.scene = SimpleScene()
        self.renderer = StubRenderer(self.scene)
        self.user_input = StubUserInput()
        self.clock = StubClock()

    def test_game_loop_and_order(self):
        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                               button=1, pos=(100, 200)),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                               button=3, pos=(300, 100)),
            pygame.event.Event(pygame.MOUSEBUTTONUP, button=2, pos=(300, 100)),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=4, pos=(52, 25)),
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=5, pos=(25, 52)),
        ]

        self.user_input.events = events

        keys = defaultdict(bool)
        keys[pygame.K_LEFT] = True
        keys[pygame.K_RIGHT] = True
        keys[pygame.K_UP] = True
        keys[pygame.K_DOWN] = True

        self.user_input.keys = keys

        self.user_input.mouse_pos = (25, 25)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            self.user_input,
            self.clock
        )

        game_loop.start()

        self.assertEqual(self.scene.events, [
            ("input_mouse", "left", (100, 200)),
            ("input_mouse", "right", (300, 100)),
            ("input_mouse", "scroll_up", (52, 25)),
            ("input_mouse", "scroll_down", (25, 52)),
            ("input_key", "left"),
            ("input_key", "right"),
            ("input_key", "jump"),
            ("input_key", "down"),
            ("update", 0.1, (25, 25)),
            ("draw", self.renderer.display),
            ("is_done"),
            ("get_next_scene"),
            ("get_next_scene_data"),
            ("cleanup")
        ])

    def test_event_quit(self):
        events = [
            pygame.event.Event(pygame.QUIT),
        ]

        self.user_input.events = events

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            self.user_input,
            self.clock
        )

        game_loop.start()

        self.assertEqual(self.scene.events, [])

    def test_game_loop_multiple_iterations(self):
        self.scene.one_loop = False

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            self.user_input,
            self.clock
        )

        game_loop.start()

        self.assertEqual(self.scene.events, [
            ("update", 0.1, (0, 0)),
            ("draw", self.renderer.display),
            ("is_done"),
            ("update", 0.1, (0, 0)),
            ("draw", self.renderer.display),
            ("is_done"),
            ("get_next_scene"),
            ("get_next_scene_data"),
            ("cleanup")
        ])

    def test_invalid_scene(self):
        self.scene.set_next_scene("invalid_scene")

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            self.user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

    @patch("scenes.main_menu.Button")
    @patch("pygame.font.SysFont")
    def test_scene_switch_to_main_menu(self, mock_sysfont, mock_button):
        #pygame.font.init()
        self.scene.set_next_scene("mainmenu")

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        #check if scene was mainmenu
        self.assertIsInstance(game_loop._scene, MainMenu)
        self.assertIsInstance(game_loop._renderer.scene, MainMenu)
        self.assertIsNone(game_loop._scene.get_next_scene())
        mock_sysfont.assert_called()
        mock_button.assert_called()

    @patch("scenes.level_list.generate_level_preview")
    @patch("scenes.level_list.Button")
    @patch("pygame.font.SysFont")
    def test_scene_switch_to_level_list(self, mock_sysfont, mock_button, mock_preview):
        #pygame.font.init()
        self.scene.set_next_scene("level_list", "level")

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        #check if scene was levellist
        self.assertIsInstance(game_loop._scene, LevelList)
        self.assertIsInstance(game_loop._renderer.scene, LevelList)
        self.assertIsNone(game_loop._scene.get_next_scene())

        mock_sysfont.assert_called()
        mock_button.assert_called()
        mock_preview.assert_called()

    @patch("scenes.level.LevelUI")
    @patch("scenes.level.Level.draw")
    def test_scene_switch_to_level(self, mock_ui, mock_draw):
        self.scene.set_next_scene("level", {"data": constants.TEST_LEVEL, "id": 1, "name": "Level 1"})

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        #check if scene was level
        self.assertIsInstance(game_loop._scene, Level)
        self.assertIsInstance(game_loop._renderer.scene, Level)
        self.assertIsNone(game_loop._scene.get_next_scene())

        mock_ui.assert_called()
        mock_draw.assert_called()

    def test_scene_switch_to_level_invalid(self):
        self.scene.set_next_scene("level", {"id": 1, "name": "Level 1"})

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        self.assertEqual(game_loop._user_input.break_after, 4)

        self.assertIsInstance(game_loop._scene, SimpleScene)
        self.assertIsInstance(game_loop._renderer.scene, SimpleScene)

    @patch("scenes.level_editor.generate_level_preview")
    @patch("scenes.level_editor.EditorUI")
    def test_scene_switch_to_editor(self, mock_ui, mock_preview):
        self.scene.set_next_scene("editor", {"data": constants.TEST_LEVEL, "id": 1, "name": "Level 1"})

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        #check if scene was level editor
        self.assertIsInstance(game_loop._scene, LevelEditor)
        self.assertIsInstance(game_loop._renderer.scene, LevelEditor)
        self.assertIsNone(game_loop._scene.get_next_scene())

        mock_ui.assert_called()
        mock_preview.assert_called()

    def test_scene_switch_to_editor_invalid(self):
        self.scene.set_next_scene("editor", {"id": 1, "name": "Level 1"})

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        self.assertEqual(game_loop._user_input.break_after, 4)

        self.assertIsInstance(game_loop._scene, SimpleScene)
        self.assertIsInstance(game_loop._renderer.scene, SimpleScene)


    @patch("scenes.end_screen.Button")
    @patch("scenes.end_screen.generate_level_preview")
    @patch("scenes.level.Level.draw")
    @patch("scenes.level.LevelUI")
    @patch("pygame.font.SysFont")
    def test_level_ends_and_changes_to_endscreen(self, mock_font, mock_ui, mock_draw, mock_preview, mock_button):
        self.scene.set_next_scene("level", {"data": constants.TEST_LEVEL_END, "id": 1, "name": "Level 1"})

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=10)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        result = game_loop.start()

        self.assertFalse(result)

        #check if scene was endscreen
        self.assertIsInstance(game_loop._scene, EndScreen)
        self.assertIsInstance(game_loop._renderer.scene, EndScreen)
        self.assertIsNone(game_loop._scene.get_next_scene())

        mock_font.assert_called()
        mock_ui.assert_called()
        mock_draw.assert_called()
        mock_preview.assert_called()
        mock_button.assert_called()

    def test_change_to_endscreen_invalid(self):
        self.scene.set_next_scene("endscreen", {"level:": "123", "timer": "123"})

        self.scene.one_loop = False
        user_input = StubUserInput(break_after=5)

        game_loop = GameLoop(
            self.scene,
            self.renderer,
            user_input,
            self.clock
        )

        game_loop.start()

        self.assertEqual(game_loop._user_input.break_after, 4)

        self.assertIsInstance(game_loop._scene, SimpleScene)
        self.assertIsInstance(game_loop._renderer.scene, SimpleScene)

