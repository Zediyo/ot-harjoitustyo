""" Editor UI for the game for the level editor scene."""

from ui.button import Button
from constants import TileType
from tools.font_manager import FontManager


class EditorUI:
    """ User interface for the level editor.

    Displays the current level name, selected item, and spawn/end point status.
    Provides buttons for saving and going back to the previous screen.
    """

    _BACK_BUTTON_RECT = (1180, 20, 60, 30)
    _SAVE_BUTTON_RECT = (1110, 20, 60, 30)
    _SPAWN_POS = (500, 50)
    _END_POS = (500, 70)
    _TEXT1_POS = (500, 10)
    _TEXT2_POS = (500, 30)

    _COLOR_TEXT = (255, 255, 255)
    _COLOR_VALID = (0, 255, 0)
    _COLOR_INVALID = (255, 0, 0)

    def __init__(self, name):
        """Initialize the EditorUI.

        Args:
            name (str): The name of the level being edited.
        """
        self._name = name
        self._font = FontManager.get_font()

        self._back_button = Button("Back", self._font, self._BACK_BUTTON_RECT)
        self._save_button = Button("Save", self._font, self._SAVE_BUTTON_RECT)

    def draw(self, display, item, required):
        """Draw the editor UI on the display.

        Args:
            display (pygame.Surface): The surface to draw on.
            item (TileType): The currently selected item type.
            required (dict): Dictionary indicating spawn and end point status.
        """
        text1 = (
            f"Level: {self._name:<33}"
            f"Current: {self._get_item_name(item):<10}"
        )
        text2 = (
            f"1: {self._get_item_name(1):<15}"
            f"2: {self._get_item_name(2):<15}"
            f"3: {self._get_item_name(3):<15}"
            f"4: {self._get_item_name(4):<15}"
            f"5: {self._get_item_name(5):<15}"
        )

        self._save_button.set_active(True)

        if required["spawn"]:
            spawn_text = "Spawn"
            spawn_color = self._COLOR_VALID
        else:
            spawn_text = "No Spawn"
            spawn_color = self._COLOR_INVALID
            self._save_button.set_active(False)

        if required["end"]:
            end_color = self._COLOR_VALID
            end_text = "End"
        else:
            end_color = self._COLOR_INVALID
            end_text = "No End"
            self._save_button.set_active(False)

        spawn_surface = self._font.render(spawn_text, True, spawn_color)
        spawn_rect = spawn_surface.get_rect(topleft=self._SPAWN_POS)
        end_surface = self._font.render(end_text, True, end_color)
        end_rect = end_surface.get_rect(topleft=self._END_POS)

        text_surface1 = self._font.render(text1, True, self._COLOR_TEXT)
        text_rect1 = text_surface1.get_rect(topleft=self._TEXT1_POS)
        text_surface2 = self._font.render(text2, True, self._COLOR_TEXT)
        text_rect2 = text_surface2.get_rect(topleft=self._TEXT2_POS)

        display.blit(text_surface1, text_rect1)
        display.blit(text_surface2, text_rect2)
        display.blit(spawn_surface, spawn_rect)
        display.blit(end_surface, end_rect)

        self._back_button.draw(display)
        self._save_button.draw(display)

    def is_back_clicked(self, mouse_pos):
        """Check if the back button was clicked.

        Args:
            mouse_pos (tuple[int, int]): The mouse position (x, y) on screen.

        Returns:
            bool: True if the back button was clicked, False otherwise.
        """
        return self._back_button.is_clicked(mouse_pos)

    def is_save_clicked(self, mouse_pos):
        """Check if the save button was clicked.

        Args:
            mouse_pos (tuple[int, int]): The mouse position (x, y) on screen.

        Returns:
            bool: True if the save button was clicked, False otherwise.
        """
        return self._save_button.is_clicked(mouse_pos)

    def update(self, mouse_pos):
        """Update the UI elements hover states based on mouse position.

        Args:
            mouse_pos (tuple[int, int]): The mouse position (x, y) on screen.
        """
        self._back_button.update(mouse_pos)
        self._save_button.update(mouse_pos)

    def _get_item_name(self, item):
        """Get the name of the selected tile.

        Args:
            item (TileType): The tile type to get the name for.

        Returns:
            str: The name of the tile type.
        """
        if item == TileType.BLOCK:
            return "Block"
        elif item == TileType.PLACEABLE:
            return "Placeable"
        elif item == TileType.ENEMY:
            return "Enemy"
        elif item == TileType.SPAWN:
            return "Spawn"
        elif item == TileType.END:
            return "End"
        return "None"
