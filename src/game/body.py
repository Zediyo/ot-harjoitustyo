import math
import pygame


class Body():
    # physics constants
    _GRAVITY_CONSTANT = 800
    _TERMINAL_VELOCITY = 1000
    _BASE_MOVEMENT_SPEED = 150.0
    _BASE_JUMP_FORCE = -285.0
    _FLOOR_GRAVITY = 100.0
    _STEP_SIZE = 10.0

    _DIR_VERTICAL = 1
    _DIR_HORIZONTAL = 0

    def __init__(self, rect, x, y):
        self.rect = rect

        # movement variables
        self._input = [0, 0]
        self._gravity = 0.0
        self._velocity = pygame.Vector2(0, 0)
        self._position = pygame.Vector2(x, y)
        self.on_floor = False
        self.touching_wall = False
        self.last_direction = 1

    def move(self, dt, colliders):
        # update velocity + gravity
        self._velocity.x = self._input[0] * self._BASE_MOVEMENT_SPEED

        self._handle_jump()
        self._update_gravity(dt)

        move = self._velocity * dt

        # remember last direction
        if self.is_moving_horizontal():
            self.last_direction = 1 if self._velocity.x > 0 else -1

        # reset input
        self._input[0] = 0
        self._input[1] = 0

        self._move_and_collide(colliders, move)

    def add_input(self, dx, dy):
        self._input[0] += dx
        self._input[1] += dy

    def _handle_jump(self):
        if self.on_floor:
            if self._input[1] < 0:
                self._gravity = self._BASE_JUMP_FORCE
            else:
                self._gravity = self._FLOOR_GRAVITY

    def _update_gravity(self, dt):
        self._velocity.y = self._gravity + dt * self._GRAVITY_CONSTANT / 2
        self._gravity += self._GRAVITY_CONSTANT * dt

        self._gravity = min(self._gravity, self._TERMINAL_VELOCITY)

    def _move_and_collide(self, colliders, move):
        self.on_floor = False
        self.touching_wall = False

        # move in steps to avoid going through walls
        self._step_move(colliders, move, self._DIR_HORIZONTAL)
        self._step_move(colliders, move, self._DIR_VERTICAL)

        self._check_for_ground(colliders)

    def _step_move(self, colliders, move, direction):
        if direction not in [self._DIR_HORIZONTAL, self._DIR_VERTICAL]:
            return

        while abs(move[direction]) > 0.01:
            if abs(move[direction]) > self._STEP_SIZE:
                self._position[direction] += self._STEP_SIZE * \
                    math.copysign(1, move[direction])
                move[direction] -= self._STEP_SIZE * \
                    math.copysign(1, move[direction])
            else:
                self._position[direction] += move[direction]
                move[direction] = 0.0

            if direction == self._DIR_VERTICAL:
                if self._vertical_move(colliders):
                    break
            elif direction == self._DIR_HORIZONTAL:
                if self._horizontal_move(colliders):
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
            self.touching_wall = True

            return True

        return False

    def _vertical_move(self, colliders):
        self.rect.y = self._position.y
        colliding = pygame.sprite.spritecollide(self, colliders, False)

        if colliding:
            for other in colliding:
                if self._velocity[1] > 0:
                    self.rect.bottom = other.rect.top
                    self.on_floor = True
                elif self._velocity[1] < 0:
                    self.rect.top = other.rect.bottom
                    self._gravity = 0

            self._velocity[1] = 0
            self._position.y = self.rect.y

            return True

        return False

    def _check_for_ground(self, colliders):
        # check if not going up
        if self._velocity[1] < 0:
            return

        self.rect.y += 1
        if pygame.sprite.spritecollide(self, colliders, False):
            self.on_floor = True
        self.rect.y -= 1

    def is_moving(self):
        return self.is_moving_horizontal() or self.is_moving_vertical()

    def is_moving_horizontal(self):
        return abs(self._velocity[0]) > 0.001

    def is_moving_vertical(self):
        return abs(self._velocity[1]) > 0.001 and not self.on_floor

    def get_velocity(self):
        return self._velocity
