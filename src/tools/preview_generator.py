import pygame

import constants


def generate_level_preview(level_data, size=(300, 150)):

    width = len(level_data[0])
    height = len(level_data)

    preview_surface = pygame.Surface((width, height))
    # preview_surface.fill((255, 255, 255))
    preview_surface = preview_surface.convert_alpha()

    for y in range(height):
        for x in range(width):
            tile = level_data[y][x]
            color = constants.TILE_COLORS.get(abs(tile), (0, 0, 0))
            preview_surface.set_at((x, y), color)

    scaler = min(size[0] / width, size[1] / height)

    preview_surface = pygame.transform.scale(
        preview_surface, (int(width * scaler), int(height * scaler)))

    return preview_surface
