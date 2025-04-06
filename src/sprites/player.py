import math
import pygame
from tools.asset_path import get_asset_path


class Player(pygame.sprite.Sprite):
    # physics constants
    _GRAVITY_CONSTANT = 800
    _TERMINAL_VELOCITY = 1000
    _BASE_MOVEMENT_SPEED = 150.0
    _BASE_JUMP_FORCE = -285.0
    _FLOOR_GRAVITY = 100.0
    _STEP_SIZE = 10.0

    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(get_asset_path("pl_player.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # movement variables
        self._input = [0, 0]
        self._gravity = 0.0
        self._velocity = pygame.Vector2(0, 0)
        self._position = pygame.Vector2(x, y)
        self._on_floor = False

    def move(self, dt, colliders):
        # update velocity + gravity
        self._velocity.x = self._input[0] * self._BASE_MOVEMENT_SPEED
        # self._velocity.y = self._input[1] * self._movement_speed

        # jumping and walk off gravity
        if self._on_floor:
            if self._input[1] < 0:
                self._gravity = self._BASE_JUMP_FORCE
            else:
                self._gravity = self._FLOOR_GRAVITY

        # gravity
        self._velocity.y = self._gravity + dt * self._GRAVITY_CONSTANT / 2
        self._gravity += self._GRAVITY_CONSTANT * dt

        self._gravity = min(self._gravity, self._TERMINAL_VELOCITY)

        # update position
        move = self._velocity * dt

        # reset input
        self._input[0] = 0
        self._input[1] = 0

        self._move_and_collide(colliders, move)

    def add_input(self, dx, dy):
        self._input[0] += dx
        self._input[1] += dy

    def _move_and_collide(self, colliders, move):
        self._on_floor = False

        # move in steps to avoid going through walls

        # horizontal movement steps
        while abs(move.x) > 0.01:
            if abs(move.x) > self._STEP_SIZE:
                self._position.x += self._STEP_SIZE * math.copysign(1, move.x)
                move.x -= self._STEP_SIZE * math.copysign(1, move.x)
            else:
                self._position.x += move.x
                move.x = 0.0

            if self._horizontal_move(colliders):
                break

        # vertical movement steps
        while abs(move.y) > 0.01:
            if abs(move.y) > self._STEP_SIZE:
                self._position.y += self._STEP_SIZE * math.copysign(1, move.y)
                move.y -= self._STEP_SIZE * math.copysign(1, move.y)
            else:
                self._position.y += move.y
                move.y = 0.0

            if self._vertical_move(colliders):
                break

    def _horizontal_move(self, colliders):
        self.rect.x = self._position.x
        colliding = pygame.sprite.spritecollide(self, colliders, False)

        if colliding:
            for other in colliding:
                if self._velocity[0] > 0:
                    self.rect.right = other.rect.left
                elif self._velocity[0] < 0:
                    self.rect.left = other.rect.right

            self._velocity[0] = 0
            self._position.x = self.rect.x

            return True

        return False

    def _vertical_move(self, colliders):
        self.rect.y = self._position.y
        colliding = pygame.sprite.spritecollide(self, colliders, False)

        if colliding:
            for other in colliding:
                if self._velocity[1] > 0:
                    self.rect.bottom = other.rect.top
                    self._on_floor = True
                elif self._velocity[1] < 0:
                    self.rect.top = other.rect.bottom
                    self._gravity = 0

            self._velocity[1] = 0
            self._position.y = self.rect.y

            return True

        return False
