""" Level UI for the level scene."""

from ui.button import Button
from tools.font_manager import FontManager


class LevelUI:
    """ User interface for the level scene.

    Displays the current level name, inventory, best time, and current time.
    Provides a button to go back to the previous screen.
    """

    _BACK_BUTTON_RECT = (1180, 20, 60, 30)
    _TEXT_POS = (500, 20)
    _TEXT_COLOR = (255, 255, 255)

    def __init__(self, name):
        """Initialize the LevelUI.

        Args:
            name (str): The name of the level being played.
        """
        self._name = name
        self._font = FontManager.get_font()

        self.back_button = Button("Back", self._font, self._BACK_BUTTON_RECT)

    def draw(self, display, item, timer):
        """Draw the level UI on the display.

        Args:
            display (pygame.Surface): The surface to draw on.
            item (int): The current item count in the inventory.
            timer (Timer): The timer object for the level.
        """
        best_time = timer.get_best_time()
        time = timer.get_time()

        record = f"{best_time:<10.2f}" if best_time != None else "--:--"
        text = (
            f"Level: {self._name:<33}"
            f"Inventory: {item:<10}"
            f"Best Time: {record:<10}"
            f"Time: {time:<10.2f}"
        )
        text_surface = self._font.render(text, True, self._TEXT_COLOR)
        text_rect = text_surface.get_rect(topleft=self._TEXT_POS)
        display.blit(text_surface, text_rect)

        self.back_button.draw(display)

    def is_back_clicked(self, mouse_pos):
        """Check if the back button is clicked.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.

        Returns:
            bool: True if the back button is clicked, False otherwise.
        """
        if self.back_button.is_clicked(mouse_pos):
            return True
        return False

    def update(self, mouse_pos):
        """Update the button hover states based on mouse position.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse cursor.
        """
        self.back_button.update(mouse_pos)
