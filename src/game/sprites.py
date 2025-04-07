import pygame


class Sprites:

    def __init__(self):
        self.player = None
        self.cursor = None
        self.end = None

        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.all = pygame.sprite.Group()
