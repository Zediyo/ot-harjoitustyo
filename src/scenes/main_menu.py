from constants import SceneName, InputAction
from scenes.scene import Scene
from ui.button import Button
from game.sprite_animation import SpriteAnimation
from tools.font_manager import FontManager


class MainMenu(Scene):
    _BACKGROUND_COLOR = (128, 128, 128)
    _SPRITE_POSITION = (620, 100)
    _SPRITE_ANIMATION = ("player_idle_spritesheet.png", (17, 16), 9)

    _PLAY_BUTTON_RECT = (540, 200, 200, 50)
    _EDITOR_BUTTON_RECT = (540, 300, 200, 50)
    _EXIT_BUTTON_RECT = (540, 400, 200, 50)

    def __init__(self):
        super().__init__()
        self._font = FontManager.get_font()
        self._buttons = []

        self._player_sprite = SpriteAnimation(fps=15, scale=(32, 32))
        self._player_sprite.add_image_set("idle", *self._SPRITE_ANIMATION)

        self._init_buttons()

    def _init_buttons(self):
        play_button = Button(
            "Play", self._font, self._PLAY_BUTTON_RECT,
            on_click=lambda: self.set_next_scene(SceneName.LEVEL_LIST, False)
        )
        editor_button = Button(
            "Editor", self._font, self._EDITOR_BUTTON_RECT,
            on_click=lambda: self.set_next_scene(SceneName.LEVEL_LIST, True)
        )
        exit_button = Button(
            "Exit", self._font, self._EXIT_BUTTON_RECT,
            on_click=lambda: self.set_next_scene(None, None)
        )

        self._buttons = [play_button, editor_button, exit_button]

    def draw(self, display):
        display.fill(self._BACKGROUND_COLOR)

        for button in self._buttons:
            button.draw(display)

        display.blit(self._player_sprite.get_frame(
            "idle"), self._SPRITE_POSITION)

    def input_mouse(self, click, pos):
        if click != InputAction.MOUSE_LEFT:
            return

        next((bt.click() for bt in self._buttons if bt.is_clicked(pos)), None)

    def update(self, dt, mouse_pos):
        self._player_sprite.update(dt)
        for button in self._buttons:
            button.update(mouse_pos)
