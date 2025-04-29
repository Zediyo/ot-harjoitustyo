from scenes.scene import Scene
from ui.button import Button
from ui.text_box import TextBox
from ui.confirm_box import ConfirmBox

from tools.db import get_all_levels, get_all_best_times, \
    level_name_exists, delete_level, delete_times
from tools.preview_generator import generate_level_preview
from tools.font_manager import FontManager

from constants import SceneName, InputAction, Settings
from game.level_data import LevelData


class LevelList(Scene):
    _SCROLL_SPEED = 50

    def __init__(self, to_editor=True):
        super().__init__()
        self._font = FontManager.get_font()
        self._buttons = []  # [(Button, scrollable)]

        self._to_editor = to_editor

        self._scroll = 0
        self._scrollable_count = 0

        self._text_box = None
        self._confirm_box = None

        self._init_static_elements()
        self._init_scrollable_buttons()

    def _init_static_elements(self):
        """Setup the static elements for the scene."""
        back_button = Button(
            "Back", self._font, (1000, 25, 200, 50),
            on_click=lambda: self.set_next_scene(SceneName.MAIN_MENU, None)
        )
        self._buttons.append((back_button, False))

        if self._to_editor:
            create_button = Button(
                "Create Level", self._font, (775, 25, 200, 50),
                on_click=lambda: self._validate_and_create_level(
                    self._text_box.get_text())
            )
            self._buttons.append((create_button, False))

            self._confirm_box = ConfirmBox(self._font, 775, 300, 425, 100)
            self._text_box = TextBox(
                self._font, (775, 100, 425, 50),
                on_submit=self._validate_and_create_level,
            )

    def _init_scrollable_buttons(self):
        """Setup the scrollable buttons for the level list."""
        levels = get_all_levels()
        times = get_all_best_times()
        scene = SceneName.EDITOR if self._to_editor else SceneName.LEVEL

        for i, level in enumerate(levels):
            button = Button(
                f"{level.name}", self._font,
                (200, 100 + (i * 160), 150, 50),
                preview=generate_level_preview(level.data, (300, 150)),
                on_click=lambda level=level: self.set_next_scene(scene, level)
            )

            time = times.get(level.id, None)

            if self._to_editor:
                button.set_text("Edit")
                self._add_delete_and_clear_button(
                    i, level.id, level.name, time)
            else:
                if time is not None:
                    button.set_above_text(
                        f"Best Time: {time:.2f}", (50, 200, 50))
                else:
                    button.set_above_text("Best Time: --:--", (200, 50, 50))

            self._buttons.append((button, True))
            self._scrollable_count += 1

    def _add_delete_and_clear_button(self, index, level_id, level_name, time):
        """Add scrollable delete and clear buttons to a single level entry in the list."""
        delete_button = Button(
            "Delete", self._font,
            (200, 65 + (index * 160), 150, 30),
            text_color=(255, 0, 0),
            on_click=lambda level_id=level_id, level_name=level_name: self._confirm_delete_level(
                level_id, level_name)
        )
        delete_button.set_above_text(f"{level_name}", (50, 200, 50))
        self._buttons.append((delete_button, True))

        if time is not None:
            clear_button = Button(
                "Clear Times", self._font,
                (200, 155 + (index * 160), 150, 30),
                text_color=(200, 50, 50),
                on_click=lambda level_id=level_id, level_name=level_name: self._confirm_clear_times(
                    level_id, level_name)
            )

            self._buttons.append((clear_button, True))

    def draw(self, display):
        display.fill((128, 128, 128))

        if self._text_box:
            self._text_box.draw(display)

        if self._confirm_box:
            self._confirm_box.draw(display)

        for (button, scrollable) in self._buttons:
            offset = 0 if not scrollable else self._scroll
            button.draw(display, offset)

    def input_mouse(self, click, pos):
        if click == InputAction.MOUSE_LEFT:
            for (button, scrollable) in self._buttons:
                offset = 0 if not scrollable else self._scroll
                if button.is_clicked(pos, offset):
                    button.click()
                    break
        # update scroll offsets
        elif click == InputAction.MOUSE_SCROLL_UP:
            self._scroll += self._SCROLL_SPEED
            self._scroll = min(self._scroll, 0)
        elif click == InputAction.MOUSE_SCROLL_DOWN and self._scrollable_count > 4:
            self._scroll -= self._SCROLL_SPEED
            self._scroll = max(self._scroll, -self._scrollable_count
                               * 160 + Settings.SCREEN_HEIGHT - 100)

    def update(self, dt, mouse_pos):
        for (button, scrollable) in self._buttons:
            offset = 0 if not scrollable else self._scroll
            button.update(mouse_pos, offset)

    def input_raw(self, events):
        if self._text_box:
            self._text_box.handle_events(events)

        if self._confirm_box:
            self._confirm_box.handle_events(events)

    def _validate_and_create_level(self, text):
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
        self.set_next_scene(
            SceneName.EDITOR,
            LevelData(id=-1, name=text, data=[[]])
        )

    def _clear_times(self, level_id):
        self._confirm_box.set_active(False)
        delete_times(level_id)
        self.set_next_scene(SceneName.LEVEL_LIST, True)

    def _delete_level(self, level_id):
        self._confirm_box.set_active(False)
        delete_level(level_id)
        self.set_next_scene(SceneName.LEVEL_LIST, True)

    def _confirm_clear_times(self, level_id, level_name):
        if self._confirm_box:
            self._confirm_box.set_text(
                f"Clear times for map {level_id}: {level_name}?")
            self._confirm_box.set_action(
                lambda level_id=level_id: self._clear_times(level_id)
            )
            self._confirm_box.set_active(True)

    def _confirm_delete_level(self, level_id, level_name):
        if self._confirm_box:
            self._confirm_box.set_text(f"Delete map {level_id}: {level_name}?")
            self._confirm_box.set_action(
                lambda level_id=level_id: self._delete_level(level_id)
            )
            self._confirm_box.set_active(True)
