import pygame

from scenes.scene import Scene
from ui.button import Button
from ui.text_box import TextBox
from ui.confirm_box import ConfirmBox

from tools.db import get_all_levels, get_all_best_times, \
    level_name_exists, delete_level, delete_times
from tools.preview_generator import generate_level_preview

from constants import SceneName, InputAction, Settings
from game.level_data import LevelData


class LevelList(Scene):
    _SCROLL_SPEED = 50

    def __init__(self, to_editor=True):
        super().__init__()
        self._font = pygame.font.SysFont("Arial", 24)
        self._buttons = []

        self._to_editor = to_editor

        self._scroll = 0
        self._scrollable_count = 0

        self._text_box = None
        self._confirm_box = None

        self._init_buttons()
        self._init_scrollable_buttons()

    def _init_buttons(self):
        back_button = Button("Back", self._font, 1000, 25, 200, 50)
        self._buttons.append((back_button, "mainmenu", None, False))

        if self._to_editor:
            new_button = Button("Create Level", self._font, 775, 25, 200, 50)
            self._buttons.append((new_button, "create", None, False))

            self._text_box = TextBox(self._font, 775, 100, 425, 50)
            self._confirm_box = ConfirmBox(self._font, 775, 300, 425, 100)

    def _init_scrollable_buttons(self):
        levels = get_all_levels()
        best_times = get_all_best_times()
        scene = SceneName.EDITOR if self._to_editor else SceneName.LEVEL

        for i, level in enumerate(levels):
            preview = generate_level_preview(level.data, (300, 150))

            button = Button(f"{level.name}", self._font,
                            200, 100 + (i * 160), 150, 50, preview=preview)

            best_time = best_times.get(level.id, None)

            if self._to_editor:
                button.set_text("Edit")

                self._add_delete_and_clear_button(
                    i, level.id, level.name, best_time)
            else:
                if best_time is not None:
                    button.set_above_text(
                        f"Best Time: {best_time:.2f}", (50, 200, 50))
                else:
                    button.set_above_text("Best Time: --:--", (200, 50, 50))

            self._buttons.append((button, scene, level, True))

            self._scrollable_count += 1

    def _add_delete_and_clear_button(self, index, level_id, level_name, best_time):
        delete_button = Button(
            "Delete", self._font, 200, 65 + (index * 160), 150, 30, text_color=(255, 0, 0))
        delete_button.set_above_text(f"{level_name}", (50, 200, 50))

        self._buttons.append((
            delete_button,
            "confirm",
            {"action": "delete", "id": level_id,  "name": level_name,
                "text": f"Delete map {level_id}: {level_name}?"},
            True,
        ))

        if best_time is not None:
            clear_button = Button(
                "Clear Times", self._font,
                200, 155 + (index * 160), 150, 30,
                text_color=(200, 50, 50))

            self._buttons.append((
                clear_button,
                "confirm",
                {"action": "clear", "id": level_id,  "name": level_name,
                    "text": f"Clear times for map {level_id}: {level_name}?"},
                True,
            ))

    def draw(self, display):
        display.fill((128, 128, 128))

        if self._text_box:
            self._text_box.draw(display)

        if self._confirm_box:
            self._confirm_box.draw(display)

        for (button, _, _, scrollable) in self._buttons:
            offset = 0 if not scrollable else self._scroll
            button.draw(display, offset)

    def input_mouse(self, click, pos):
        if click == InputAction.MOUSE_LEFT:
            for (button, next_scene, next_scene_data, scrollable) in self._buttons:
                offset = 0 if not scrollable else self._scroll
                if button.is_clicked(pos, offset):
                    self._handle_button_click(next_scene, next_scene_data)
                    break
        # update scroll offsets
        elif click == InputAction.MOUSE_SCROLL_UP:
            self._scroll += self._SCROLL_SPEED
            self._scroll = min(self._scroll, 0)
        elif click == InputAction.MOUSE_SCROLL_DOWN and self._scrollable_count > 4:
            self._scroll -= self._SCROLL_SPEED
            self._scroll = max(self._scroll, -self._scrollable_count
                               * 160 + Settings.SCREEN_HEIGHT - 100)

    def _handle_button_click(self, next_scene, next_scene_data):
        if next_scene == "create":
            self._handle_new_level_text_input()
        elif next_scene == "confirm":
            self._activate_confirm_box(next_scene_data)
        else:
            self.set_next_scene(next_scene, next_scene_data)

    def update(self, dt, mouse_pos):
        for (button, _, _, scrollable) in self._buttons:
            offset = 0 if not scrollable else self._scroll
            button.update(mouse_pos, offset)

    def input_raw(self, events):
        if self._text_box:
            res = self._text_box.handle_events(events)
            if res is not None:
                self._handle_new_level_text_input()

        if self._confirm_box:
            res = self._confirm_box.handle_events(events)
            if res is not None:
                self._handle_confirm_box_action()

    def _handle_new_level_text_input(self):
        text = self._text_box.get_text().strip()
        self._text_box.set_error_text(None)

        # return if invalid text
        if len(text) > 32:
            self._text_box.set_error_text("Level name too long. (max 32)")
            return
        if len(text) < 3:
            self._text_box.set_error_text("Level name too short. (min 3)")
            return

        # only alphanumeric, spaces, underscore and dashes allowed
        if not all(c.isalnum() or c in " _-" for c in text):
            self._text_box.set_error_text(
                "Use only letters, numbers, spaces, _ or -.")
            return

        # check if level name already exists
        if level_name_exists(text):
            self._text_box.set_error_text("Level name already exists.")
            return

        # go to level editor with new level name
        self.set_next_scene(SceneName.EDITOR, LevelData(
            id=-1, name=text, data=[[]]))

    def _handle_confirm_box_action(self):
        self._confirm_box.set_active(False)

        action = self._confirm_box.get_data()
        if action is None:
            return

        if action["action"] == "delete":
            delete_level(action["id"])

        elif action["action"] == "clear":
            delete_times(action["id"])

        self.set_next_scene(SceneName.LEVEL_LIST, True)

    def _activate_confirm_box(self, data):
        if self._confirm_box:
            self._confirm_box.set_data(data)
            self._confirm_box.set_text(data["text"])
            self._confirm_box.set_active(True)
