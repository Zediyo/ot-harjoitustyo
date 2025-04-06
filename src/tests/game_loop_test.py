from map import Map
import unittest

import pygame
from scenes.scene import Scene
from game_loop import GameLoop

from collections import defaultdict


class StubUserInput:
    def __init__(self, events=[], keys=defaultdict(bool), mouse_pos=(0, 0)):
        self.keys = keys
        self.events = events
        self.mouse_pos = mouse_pos

    def get_events(self):
        return self.events

    def get_pressed(self):
        return self.keys

    def get_mouse_pos(self):
        return self.mouse_pos


class StubRenderer:
    def __init__(self, scene=None):
        self.scene = scene

    def render(self):
        self.scene.draw(None)

    def set_scene(self, scene):
        self.scene = scene


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
            self._end_scene = True
            self._next_scene = "text"

        self.one_loop = True

    def is_done(self):
        self.events.append(("is_done"))
        return self._end_scene

    def get_next_scene(self):
        self.events.append(("get_next_scene"))
        return self._next_scene

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
            ("input_key", "left"),
            ("input_key", "right"),
            ("input_key", "jump"),
            ("input_key", "down"),
            ("update", 0.1, (25, 25)),
            ("draw", None),
            ("is_done"),
            ("get_next_scene"),
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
            ("draw", None),
            ("is_done"),
            ("update", 0.1, (0, 0)),
            ("draw", None),
            ("is_done"),
            ("get_next_scene"),
            ("cleanup")
        ])
