""" Contains the SpriteAnimation class for handling sprite animations."""

import pygame
from tools.asset_helpers import load_image, get_spritesheet_frames


class SpriteAnimation:
    """ Stores and handles sprite animations.

    Provides methods to update the animation frames, add new image sets,
    retrieve frames, reset animations and change animation modes.
    """

    def __init__(self, fps=15, scale=(0, 0)):
        """ Initialize the SpriteAnimation class.
        Args:
            fps (int, optional): Frames per second for the animation. Defaults to 15.
            scale (tuple[int, int], optional): Size (width, height) to scale the frames to.
                Defaults to (0, 0), which disables scaling and uses the original frame sizes.
        """
        self._fps = fps
        self._scale = scale
        self._current_frame = 0
        self._animation_time = 0.0
        self._mode = 0
        self._images = {}

    def update(self, dt):
        """ Update the animation state based on the time elapsed.

        Args:
            dt (float): The delta time since the last frame.
        """

        self._animation_time += dt

        if 1 / self._fps <= self._animation_time:
            self._animation_time = 0.0
            self._current_frame += 1

    def add_image_set(self, name, asset, frame_size, count):
        """ Load a tile sheet and add its frames to the animation sets.

        Args:
            name (str): The name of the animation set.
            asset (str): Asset filename or path relative to the assets folder.
            frame_size (tuple[int, int]): The size (width, height) of each frame in the sheet.
            count (int): The number of frames to read from the sprite sheet.
        """
        frame_width, frame_height = frame_size

        sheet = load_image(asset)

        self._images[name] = get_spritesheet_frames(
            sheet, frame_width, frame_height, count=count, scale=self._scale)

    def get_frame(self, name, index=-1):
        """ Get a frame from the specified animation set.

        Args:
            name (str): The name of the animation set.
            index (int, optional): The index of the frame to retrieve.
                Defaults to -1, which return the current frame based on the internal timer.

        Returns:
            pygame.Surface: The requested frame, or a blank surface if not found.
        """
        if name in self._images:
            if index != -1:
                return self._images[name][index % len(self._images[name])]

            current_frame = self._current_frame % len(self._images[name])
            return self._images[name][current_frame]

        return pygame.Surface((1, 1))

    def reset_animation(self):
        """ Reset the animation frame to the first frame and reset the animation time. """
        self._current_frame = 0
        self._animation_time = 0.0

    def change_mode(self, mode, start_frame=0):
        """ Change the animation mode and reset the animation if mode changes.

        Args:
            mode (int): The new animation mode.
            start_frame (int, optional): The frame to start at after mode change.
                Defaults to 0, which starts from the first frame.
        """

        if mode != self._mode:
            self._mode = mode
            self.reset_animation()

            if start_frame != 0:
                self._current_frame = start_frame

    def get_mode(self):
        """ Get the current animation mode.

        Returns:
            int: The current animation mode.
        """
        return self._mode
