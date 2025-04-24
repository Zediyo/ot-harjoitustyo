import pygame
from tools.asset_path import get_asset_path
from tools.spritesheet_frames import get_spritesheet_frames


class SpriteAnimation():
    def __init__(self, fps=15, scale=(0, 0)):
        super().__init__()

        self._fps = fps
        self._scale = scale
        self._current_frame = 0
        self._animation_time = 0.0
        self._previous_state = 0
        self._images = {}

    def update(self, dt):
        self._animation_time += dt

        if 1 / self._fps <= self._animation_time:
            self._animation_time = 0.0
            self._current_frame += 1

    def add_image_set(self, name, image_path, frame_size, count):
        (frame_width, frame_height) = frame_size
        sheet = pygame.image.load(get_asset_path(image_path))
        self._images[name] = get_spritesheet_frames(
            sheet, frame_width, frame_height, count=count, scale=self._scale)

    def get_frame(self, name, index=-1):
        if name in self._images:
            if index != -1:
                return self._images[name][index % len(self._images[name])]

            current_frame = self._current_frame % len(self._images[name])
            return self._images[name][current_frame]

        return pygame.Surface((32, 32))

    def reset_animation(self):
        self._current_frame = 0

    def set_previous_state(self, state):
        self._previous_state = state

    def get_previous_state(self):
        return self._previous_state
