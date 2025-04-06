import pygame


class Sprites:

    def __init__(self):
        self.player = pygame.sprite.GroupSingle()
        self.cursor = pygame.sprite.GroupSingle()
        self.end = pygame.sprite.GroupSingle()

        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.all = pygame.sprite.Group()
