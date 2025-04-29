import pygame

from constants import SceneName, InputAction
from scenes.scene import Scene
from ui.button import Button
from game.sprite_animation import SpriteAnimation


class MainMenu(Scene):

    def __init__(self):
        super().__init__()
        self._font = pygame.font.SysFont("Arial", 24)
        self._buttons = {}

        self._player_sprite = SpriteAnimation(fps=15, scale=(32, 32))
        self._player_sprite.add_image_set(
            "idle", "player_idle_spritesheet.png", (17, 16), 9)

        self._init_buttons()

    def _init_buttons(self):
        play_button = Button("Play", self._font, 540, 200, 200, 50)
        editor_button = Button("Editor", self._font, 540, 300, 200, 50)
        exit_button = Button("Exit", self._font, 540, 400, 200, 50)

        self._buttons = {
            "play": (play_button, SceneName.LEVEL_LIST, False),
            "editor": (editor_button, SceneName.LEVEL_LIST, True),
            "exit": (exit_button, None, None)
        }

    def draw(self, display):
        display.fill((128, 128, 128))

        for (button, _, _) in self._buttons.values():
            button.draw(display)

        display.blit(self._player_sprite.get_frame("idle"), (620, 100))

    def input_mouse(self, click, pos):
        if click != InputAction.MOUSE_LEFT:
            return

        for (button, next_scene, next_scene_data) in self._buttons.values():
            if button.is_clicked(pos):
                self.set_next_scene(next_scene, next_scene_data)
                break

    def update(self, dt, mouse_pos):
        self._player_sprite.update(dt)
        for (button, _, _) in self._buttons.values():
            button.update(mouse_pos)
