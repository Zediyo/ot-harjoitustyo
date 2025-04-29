""" Contains the EndScreen scene class, which is displayed when a level is completed."""

from constants import SceneName, InputAction, Settings
from tools.preview_generator import generate_level_preview
from tools.font_manager import FontManager

from scenes.scene import Scene
from game.endscreen_data import EndScreenData

from ui.button import Button
from ui.button_info import ButtonInfo

class EndScreen(Scene):
    """ Scene for the end screen, displayed when a level is completed.

    Displays the level preview, best time, completion time
    and buttons to retry or go back to the menu.
    """

    _BACKGROUND_COLOR = (128, 128, 128)
    _TEXT_COLOR_GOOD = (0, 255, 0)
    _TEXT_COLOR_BAD = (255, 0, 0)
    _TEXT_COLOR_NORMAL = (255, 255, 255)

    _PREVIEW_POS = (Settings.SCREEN_WIDTH // 2, 100)
    _PREVIEW_SIZE = (600, 300)

    _RETRY_RECT = (420, 500, 200, 50)
    _BACK_RECT = (660, 500, 200, 50)

    _MAIN_TEXT_POS = (Settings.SCREEN_WIDTH // 2, 420)
    _ALT_TEXT_POS = (Settings.SCREEN_WIDTH // 2, 460)

    def __init__(self, data: EndScreenData):
        """Initialize the EndScreen.

        Args:
            data (EndScreenData): The data for the end screen, including level and timer.
        """
        super().__init__()
        self._font = FontManager.get_font(24, "Arial")
        self._data = data

        self._preview = (None, None) #(pygame.Surface, pygame.Rect)
        self._buttons = [] #[ButtonInfo]
        self._texts = [] #[(pygame.Surface, pygame.Rect)]

        self._init_preview()
        self._init_buttons()
        self._init_texts()

    def _init_preview(self):
        """Setup the level preview image for the end screen."""
        preview = generate_level_preview(self._data.level.data, self._PREVIEW_SIZE)
        
        preview_rect = preview.get_rect()
        preview_rect.midtop = self._PREVIEW_POS

        self._preview = (preview, preview_rect)

    def _init_buttons(self):
        """Setup the menu buttons for the end screen."""
        retry_button = Button("Retry", self._font, self._RETRY_RECT)
        back_button = Button("Menu", self._font, self._BACK_RECT)

        self._buttons = [
            ButtonInfo(retry_button, SceneName.LEVEL, self._data.level),
            ButtonInfo(back_button, SceneName.LEVEL_LIST, False),
        ]

    def _init_texts(self):
        """Setup the result texts for level completion and best time."""
        time = self._data.timer.get_time()
        alt_text = f"Time: {time:.2f}"

        if self._data.timer.is_best_time():
            main_text = "New Best Time!"
            main_color = self._TEXT_COLOR_GOOD
            alt_color = self._TEXT_COLOR_GOOD
        else:
            best_time = self._data.timer.get_best_time()
            main_text = f"Best Time: {best_time:.2f}"
            main_color = self._TEXT_COLOR_NORMAL
            alt_color = self._TEXT_COLOR_BAD

        main_surface = self._font.render(main_text, True, main_color)
        alt_surface = self._font.render(alt_text, True, alt_color)

        main_rect = main_surface.get_rect(center=self._MAIN_TEXT_POS)
        alt_rect = alt_surface.get_rect(center=self._ALT_TEXT_POS)

        self._texts.append((main_surface, main_rect))
        self._texts.append((alt_surface, alt_rect))

    def draw(self, display):
        """Draw the end screen and its components.

        Args:
            display (pygame.Surface): The display surface to draw on.
        """
        display.fill(self._BACKGROUND_COLOR)

        for button_info in self._buttons:
            button_info.button.draw(display)

        display.blit(self._preview[0], self._preview[1])

        for text, pos in self._texts:
            display.blit(text, pos)

    def input_mouse(self, click, pos):
        """Handle mouse input for the end screen buttons.

        Args:
            click (InputAction): The type of mouse click.
            pos (tuple[int, int]): The position of the mouse click.
        """
        if click != InputAction.MOUSE_LEFT:
            return

        for button_info in self._buttons:
            if button_info.button.is_clicked(pos):
                self.set_next_scene(button_info.next_scene, button_info.next_scene_data)
                break

    def update(self, dt, mouse_pos):
        """ Update button hover states based on mouse position.
        
        Args:
            dt (float): The delta time since the last frame.
            mouse_pos (tuple[int, int]): The current mouse position.
        """
        for button_info in self._buttons:
            button_info.button.update(mouse_pos)
