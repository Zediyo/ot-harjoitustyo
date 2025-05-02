""" Contains the LevelList scene, a menu for selecting levels to play or edit. """

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
    """ Scene for the level list, displaying all levels available in the game.

    Depending on the mode, the list provides different interactions and information.
    In the play mode, it shows the best times for each level and gives the option to play them.
    In the editor mode it allows creating, deleting and moving to level editor.
    The scene is scrollable if there are more levels than can be displayed at once.
    """
    # Scroll settings
    _SCROLL_SPEED = 50
    _MAX_VISIBLE_ROWS = 4

    # Colors
    _BACKGROUND_COLOR = (128, 128, 128)
    _TEXT_COLOR_TIME = (50, 200, 50)
    _TEXT_COLOR_NO_TIME = (200, 50, 50)
    _TEXT_COLOR_DELETE = (255, 0, 0)
    _TEXT_COLOR_LEVEL_NAME = (50, 200, 50)
    _TEXT_COLOR_CLEAR = (200, 50, 50)

    # Static elements
    _BACK_BUTTON_RECT = (1000, 25, 200, 50)
    _CREATE_BUTTON_RECT = (775, 25, 200, 50)
    _CONFIRM_BOX_RECT = (775, 300, 425, 100)
    _TEXT_BOX_RECT = (775, 100, 425, 50)

    # Scrollable elements
    _PREVIEW_SCALE = (300, 150)
    _LIST_ENTRY_HEIGHT = 160
    _LIST_START_Y_OFFSET = 100

    _LEVEL_BUTTON_RECT = (200, 100, 150, 50)
    _DELETE_BUTTON_RECT = (200, 65, 150, 30)
    _CLEAR_BUTTON_RECT = (200, 155, 150, 30)

    # Level name limits
    _LEVEL_NAME_MIN = 3
    _LEVEL_NAME_MAX = 32

    def __init__(self, to_editor=True):
        """Initialize the LevelList scene.

        Args:
            to_editor (bool): If True, the scene is in editor mode.
        """
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
        """Set up the static elements for the scene."""
        back_button = Button(
            "Back", self._font, self._BACK_BUTTON_RECT,
            on_click=lambda: self.set_next_scene(SceneName.MAIN_MENU, None)
        )
        self._buttons.append((back_button, False))

        if self._to_editor:
            create_button = Button(
                "Create Level", self._font, self._CREATE_BUTTON_RECT,
                on_click=lambda: self._validate_and_create_level(
                    self._text_box.get_text())
            )
            self._buttons.append((create_button, False))

            self._confirm_box = ConfirmBox(self._font, *self._CONFIRM_BOX_RECT)
            self._text_box = TextBox(
                self._font, self._TEXT_BOX_RECT,
                on_submit=self._validate_and_create_level,
            )

    def _init_scrollable_buttons(self):
        """Set up the scrollable buttons for the level list."""
        levels = get_all_levels()
        times = get_all_best_times()
        scene = SceneName.EDITOR if self._to_editor else SceneName.LEVEL

        for i, level in enumerate(levels):
            button = Button(
                f"{level.name}", self._font,
                self._get_element_offset(i, self._LEVEL_BUTTON_RECT),
                preview=generate_level_preview(
                    level.data, self._PREVIEW_SCALE),
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
                        f"Best Time: {time:.2f}", self._TEXT_COLOR_TIME)
                else:
                    button.set_above_text(
                        "Best Time: --:--", self._TEXT_COLOR_NO_TIME)

            self._buttons.append((button, True))
            self._scrollable_count += 1

    def _add_delete_and_clear_button(self, index, level_id, level_name, time):
        """Add scrolling delete and clear buttons to a single level entry in the list.

        Args:
            index (int): The index of the level in the list.
            level_id (int): The ID of the level.
            level_name (str): The name of the level.
            time (float): The best time for the level, if available.
        """
        delete_button = Button(
            "Delete", self._font,
            self._get_element_offset(index, self._DELETE_BUTTON_RECT),
            text_color=self._TEXT_COLOR_DELETE,
            on_click=lambda level_id=level_id, level_name=level_name: self._confirm_delete_level(
                level_id, level_name)
        )
        delete_button.set_above_text(
            f"{level_name}", self._TEXT_COLOR_LEVEL_NAME)
        self._buttons.append((delete_button, True))

        if time is not None:
            clear_button = Button(
                "Clear Times", self._font,
                self._get_element_offset(index, self._CLEAR_BUTTON_RECT),
                text_color=self._TEXT_COLOR_CLEAR,
                on_click=lambda level_id=level_id, level_name=level_name: self._confirm_clear_times(
                    level_id, level_name)
            )

            self._buttons.append((clear_button, True))

    def _get_element_offset(self, index, base_rect):
        """Calculate the offset for a scrollable element based on its index.

        Args:
            index (int): The index of the element in the list.
            base_rect (tuple[int, int, int, int]): The base rectangle for the element.

        Returns:
            tuple[int, int, int, int]: The offset rectangle for the element.
        """
        (x, y, w, h) = base_rect
        return (x, y + (index * self._LIST_ENTRY_HEIGHT), w, h)

    def draw(self, display):
        """Draw the level list scene and its components.

        Args:
            display (pygame.Surface): The display surface to draw on.
        """
        display.fill(self._BACKGROUND_COLOR)

        if self._text_box:
            self._text_box.draw(display)

        if self._confirm_box:
            self._confirm_box.draw(display)

        for (button, scrollable) in self._buttons:
            offset = 0 if not scrollable else self._scroll
            button.draw(display, offset)

    def input_mouse(self, click, pos):
        """Handle mouse input for the level list scene.

        Uses the click position to determine which button was clicked.

        Args:
            click (InputAction): The mouse input action (e.g., InputAction.MOUSE_LEFT).
            pos (tuple[int, int]): The mouse position (x, y) on screen.
        """
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
        elif click == InputAction.MOUSE_SCROLL_DOWN \
                and self._scrollable_count > self._MAX_VISIBLE_ROWS:
            self._scroll -= self._SCROLL_SPEED
            self._scroll = max(self._scroll,
                               -self._scrollable_count * self._LIST_ENTRY_HEIGHT +
                               Settings.SCREEN_HEIGHT - self._LIST_START_Y_OFFSET
                               )

    def update(self, dt, mouse_pos):
        """Update button hover states and other dynamic elements in the scene.

        Args:
            dt (float): Time delta since the last frame.
            mouse_pos (tuple[int, int]): Current mouse position.
        """
        for (button, scrollable) in self._buttons:
            offset = 0 if not scrollable else self._scroll
            button.update(mouse_pos, offset)

    def input_raw(self, events):
        """Handle raw input events from Pygame.

        Updates elements that require raw input, such as text boxes and confirm boxes.

        Args:
            events (list[pygame.event.Event]): List of Pygame events to process.
        """
        if self._text_box:
            self._text_box.handle_events(events)

        if self._confirm_box:
            self._confirm_box.handle_events(events)

    def _validate_and_create_level(self, text):
        """Validate the level name and create a new level.

        Args:
            text (str): The level name entered by the user.
        """
        text = self._text_box.get_text().strip()
        self._text_box.set_error_text(None)

        if len(text) > self._LEVEL_NAME_MAX:
            self._text_box.set_error_text(
                f"Level name too long. (max {self._LEVEL_NAME_MAX})")
            return
        if len(text) < self._LEVEL_NAME_MIN:
            self._text_box.set_error_text(
                f"Level name too short. (min {self._LEVEL_NAME_MIN})")
            return

        # only alphanumeric, spaces, underscore and dashes allowed
        if not all(c.isalnum() or c in " _-" for c in text):
            self._text_box.set_error_text(
                "Use only letters, numbers, spaces, _ or -.")
            return

        if level_name_exists(text):
            self._text_box.set_error_text("Level name already exists.")
            return

        # go to level editor with new level name
        self.set_next_scene(
            SceneName.EDITOR,
            LevelData(id=-1, name=text, data=[[]])
        )

    def _clear_times(self, level_id):
        """Clear the best times for a level and reload the level list.

        Args:
            level_id (int): The ID of the level to clear times for.
        """
        self._confirm_box.set_active(False)
        delete_times(level_id)
        self.set_next_scene(SceneName.LEVEL_LIST, True)

    def _delete_level(self, level_id):
        """Delete a level and reload the level list.

        Args:
            level_id (int): The ID of the level to delete.
        """
        self._confirm_box.set_active(False)
        delete_level(level_id)
        self.set_next_scene(SceneName.LEVEL_LIST, True)

    def _confirm_clear_times(self, level_id, level_name):
        """ Prompt the user to confirm clearing times for a level. 

        Args:
            level_id (int): The ID of the level to clear times for.
            level_name (str): The name of the level to clear times for.
        """
        if self._confirm_box:
            self._confirm_box.set_text(
                f"Clear times for map {level_id}: {level_name}?")
            self._confirm_box.set_action(
                lambda level_id=level_id: self._clear_times(level_id)
            )
            self._confirm_box.set_active(True)

    def _confirm_delete_level(self, level_id, level_name):
        """Prompt the user to confirm deleting a level.

        Args:
            level_id (int): The ID of the level to delete.
            level_name (str): The name of the level to delete.
        """
        if self._confirm_box:
            self._confirm_box.set_text(f"Delete map {level_id}: {level_name}?")
            self._confirm_box.set_action(
                lambda level_id=level_id: self._delete_level(level_id)
            )
            self._confirm_box.set_active(True)
