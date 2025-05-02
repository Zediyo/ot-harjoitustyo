"""Utility functions for loading assets and creating fallback textures."""

import os
import pygame
from constants import Settings

_ASSET_DIR = os.path.dirname(__file__)


def get_asset_path(asset_name):
    """Get the absolute path to an asset.

    Args:
        asset_name (str): Filename of the asset relative to the assets directory.

    Returns:
        str or None: Full path to the asset, or None if it doesn't exist.
    """
    asset_path = os.path.join(_ASSET_DIR, "../assets", asset_name)

    if not os.path.exists(asset_path):
        return None

    return asset_path


def load_image(image_path, scale=(0, 0)):
    """Load an image from the assets folder and optionally scale it.

    If the image is not found, a fallback checkerboard texture is returned.

    Args:
        image_path (str): The filename of the image to load (relative to assets).
        scale (tuple[int, int], optional):
            Desired image size. If (0, 0), no scaling is applied.
            If image is missing, this sets fallback size.
            Defaults to (0, 0).

    Returns:
        pygame.Surface: The loaded and scaled image surface.
    """
    path = get_asset_path(image_path)

    if path is None:
        error_size = (
            max(Settings.TILE_SIZE, scale[0]),
            max(Settings.TILE_SIZE, scale[1])
        )
        return generate_error_texture(error_size)

    image = pygame.image.load(path)

    if scale != (0, 0):
        image = pygame.transform.scale(image, scale)

    return image


def get_spritesheet_frames(sheet, frame_width, frame_height, count, scale=(0, 0)):
    """Extract individual frames from a sprite sheet.

    Args:
        sheet (pygame.Surface): The full sprite sheet surface.
        frame_width (int): Width of each frame.
        frame_height (int): Height of each frame.
        count (int): Number of frames to extract (left to right).
        scale (tuple[int, int], optional): If provided, scales each frame to this size.

    Returns:
        list[pygame.Surface]: A list of frame surfaces.
    """
    frames = []
    for i in range(count):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = sheet.subsurface(rect)

        if scale != (0, 0):
            frames.append(pygame.transform.scale(frame, scale))
        else:
            frames.append(frame)

    return frames


def generate_error_texture(size):
    """Generate a purple-and-green checkerboard pattern for invalid textures.

    Args:
        size (tuple[int, int]): Size of the surface to generate.

    Returns:
        pygame.Surface: The scaled error texture surface.
    """
    color1 = (128, 0, 128)
    color2 = (0, 255, 0)

    error_surface = pygame.Surface((4, 4))

    for x in range(4):
        for y in range(4):
            color = color1 if (x + y) % 2 == 0 else color2
            error_surface.set_at((x, y), color)

    return pygame.transform.scale(error_surface, size)
