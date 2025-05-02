"""Function for generating a level preview surface from raw tile data."""

import pygame
import constants


def generate_level_preview(level_data, size=(300, 150)):
    """Generate a scaled preview image from level tile data.

    Args:
        level_data (list[list[int]]): 2D grid of tile values representing the level layout.
        size (tuple[int, int]): Maximum size (width, height) of the output preview image.

    Returns:
        pygame.Surface: The scaled surface visualizing the level layout.
    """

    width = len(level_data[0])
    height = len(level_data)

    preview_surface = pygame.Surface((width, height)).convert_alpha()

    for y in range(height):
        for x in range(width):
            tile = level_data[y][x]
            color = constants.TILE_COLORS.get(abs(tile), (0, 0, 0))
            preview_surface.set_at((x, y), color)

    scaler = min(size[0] / width, size[1] / height)

    preview_surface = pygame.transform.scale(
        preview_surface, (int(width * scaler), int(height * scaler)))

    return preview_surface
