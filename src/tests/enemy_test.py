import unittest
import pygame
from sprites.enemy import Enemy


class Block(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.enemy = Enemy(256, 64, start_dir=1)
        self.dt = 0.1
        self.blocks = pygame.sprite.Group()

    def test_constructor(self):
        self.assertEqual(self.enemy.rect.x, 256)
        self.assertEqual(self.enemy.rect.y, 64)

    def test_enemy_wall_collision(self):
        self.blocks.add(Block(289, 64))

        self.assertEqual(self.enemy._body.touching_wall, False)
        self.assertEqual(self.enemy._dir, 1)

        self.enemy.update(self.dt, self.blocks, pygame.Rect(0, 0, 0, 0))

        self.assertEqual(self.enemy._body.touching_wall, True)

        self.enemy.update(self.dt, self.blocks, pygame.Rect(0, 0, 0, 0))

        self.assertEqual(self.enemy._body.touching_wall, False)
        self.assertEqual(self.enemy._dir, -1)

    def test_enemy_jumps_after_touch_and_time(self):
        self.blocks.add(Block(256, 96))
        self.assertEqual(self.enemy._body.on_floor, False)

        self.enemy.update(self.dt, self.blocks, pygame.Rect(0, 0, 0, 0))
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy._touch_count = self.enemy._TOUCHES_TO_JUMP
        self.enemy._time_from_touch = self.enemy._TIME_AFTER_TOUCH

        self.enemy.update(self.dt, self.blocks, pygame.Rect(0, 0, 0, 0))
        self.assertEqual(self.enemy._touch_count, 0)
        self.assertEqual(self.enemy._time_from_touch, 0.0)
        self.assertEqual(self.enemy._body.on_floor, False)

    def test_enemy_jumps_towards_player(self):
        (x, y, w, h) = self.enemy.rect.copy()
        range = self.enemy._DISTANCE_TO_JUMP + 5

        player_rect_too_far_above = pygame.Rect(x + 1, y - range * 2, w, h)
        player_rect_too_far_left = pygame.Rect(x - range, y - 5, w, h)
        player_rect_too_far_right = pygame.Rect(x + range, y - 5, w, h)
        player_rect_too_low = pygame.Rect(x + 1, y, w, h)
        player_rect_behind_enemy_left = pygame.Rect(x - 5, y - 5, w, h)
        player_rect_behind_enemy_right = pygame.Rect(x + 5, y - 5, w, h)
        player_rect_correct = pygame.Rect(x + 1, y - range / 2, w, h)

        self.blocks.add(Block(256, 96))
        self.assertEqual(self.enemy._body.on_floor, False)

        dt = 0.0001

        self.enemy.update(dt, self.blocks, pygame.Rect(0, 0, 0, 0))
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy.update(dt, self.blocks, player_rect_too_far_above)
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy.update(dt, self.blocks, player_rect_too_far_left)
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy.update(dt, self.blocks, player_rect_too_far_right)
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy.update(dt, self.blocks, player_rect_too_low)
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy.update(dt, self.blocks, player_rect_behind_enemy_left)
        self.assertEqual(self.enemy._body.on_floor, True)

        self.enemy._dir = self.enemy._DIR_LEFT
        self.enemy.update(dt, self.blocks, player_rect_behind_enemy_right)
        self.assertEqual(self.enemy._body.on_floor, True)
        self.enemy._dir = self.enemy._DIR_RIGHT

        self.enemy.update(dt, self.blocks, player_rect_correct)
        self.assertEqual(self.enemy._body.on_floor, False)
