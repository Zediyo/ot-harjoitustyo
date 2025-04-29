import unittest
import pygame
from sprites.player import Player


class Block(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(256, 64)
        self.dt = 0.1
        self.blocks = pygame.sprite.Group()

    def test_constructor(self):
        self.assertEqual(self.player.rect.x, 256)
        self.assertEqual(self.player.rect.y, 64)

    def test_add_input(self):
        self.player.add_input(1, 0)
        self.assertEqual(self.player._body._input[0], 1)
        self.assertEqual(self.player._body._input[1], 0)

        self.player.add_input(0, 1)
        self.assertEqual(self.player._body._input[0], 1)
        self.assertEqual(self.player._body._input[1], 1)

        self.player.add_input(-1, -1)
        self.assertEqual(self.player._body._input[0], 0)
        self.assertEqual(self.player._body._input[1], 0)

    def test_horizontal_movement_right(self):
        self.player.add_input(1, 0)
        self.player.move(self.dt, self.blocks)
        self.assertGreater(self.player.rect.x, 256)

    def test_horizontal_movement_left(self):
        self.player.add_input(-1, 0)
        self.player.move(self.dt, self.blocks)
        self.assertLess(self.player.rect.x, 256)

    def test_gravity(self):
        self.player.move(self.dt, self.blocks)
        self.assertGreater(self.player.rect.y, 64)

    def test_jump(self):
        self.player._body.on_floor = True
        self.player.add_input(0, -1)
        self.player.move(self.dt, self.blocks)
        self.assertLess(self.player.rect.y, 64)
        self.assertFalse(self.player._body.on_floor)

    def test_vertical_collision(self):
        block_below = Block(256, 97)
        block_above = Block(256, -1)
        self.blocks.add(block_below)
        self.blocks.add(block_above)

        self.player.move(self.dt, self.blocks)
        self.assertTrue(self.player._body.on_floor)
        self.assertEqual(self.player.rect.y, 65)

        self.player.move(self.dt, self.blocks)
        self.assertEqual(self.player.rect.y, 65)
        self.assertGreater(self.player._body._gravity, 100.0)

        self.player.add_input(0, -1)
        self.player.move(self.dt, self.blocks)
        self.assertFalse(self.player._body.on_floor)
        self.assertEqual(self.player.rect.y, 63)
        self.assertEqual(self.player._body._gravity, 0.0)

    def test_horizontal_collision(self):
        block_left = Block(191, 64)
        block_right = Block(289, 64)
        self.blocks.add(block_left)
        self.blocks.add(block_right)

        self.player.move(self.dt, self.blocks)
        self.assertEqual(self.player.rect.x, 256)

        self.player.add_input(-1, 0)
        self.player.move(self.dt, self.blocks)
        self.assertEqual(self.player.rect.x, 255)

        self.player.add_input(1, 0)
        self.player.move(self.dt, self.blocks)
        self.assertEqual(self.player.rect.x, 257)
