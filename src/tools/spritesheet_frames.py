import pygame


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
