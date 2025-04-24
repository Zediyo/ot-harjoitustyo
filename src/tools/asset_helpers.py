import os
import pygame

dirname = os.path.dirname(__file__)


def get_asset_path(asset_name):
    asset_path = os.path.join(dirname, "../assets", asset_name)

    if not os.path.exists(asset_path):
        return None

    return asset_path


def load_image(image_path, scale=(0, 0)):
    path = get_asset_path(image_path)

    if path is None:
        return pygame.Surface(scale)

    image = pygame.image.load(path)

    if scale != (0, 0):
        image = pygame.transform.scale(image, scale)

    return image


def get_spritesheet_frames(sheet, frame_width, frame_height, count, scale=(0, 0)):
    frames = []
    for i in range(count):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = sheet.subsurface(rect)

        if scale != (0, 0):
            scaled = pygame.transform.scale(frame, scale)
            frames.append(scaled)
        else:
            frames.append(frame)

    return frames
