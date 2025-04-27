""" Contains the Body class, which is used for sprites that require physics simulation."""

import math
import pygame


class Body():
    """ Body class for sprites that require physics simulation.

    Handles movement, gravity, and collision detection with colliders.

    Attributes:
        rect (pygame.Rect): The rect of the sprite.
        on_floor (bool): True when the sprite is on the floor, False otherwise.
        touching_wall (bool): True when the sprite is touching a wall, False otherwise.
        last_direction (int): The last direction the sprite was moving in. 1 for right, -1 for left.
    """
    # physics constants
    _GRAVITY_CONSTANT = 800
    _TERMINAL_VELOCITY = 1000
    _BASE_MOVEMENT_SPEED = 150.0
    _BASE_JUMP_FORCE = -285.0
    _FLOOR_GRAVITY = 100.0
    _STEP_SIZE = 10.0
    _MOVE_EPSILON = 0.001

    _DIR_VERTICAL = 1
    _DIR_HORIZONTAL = 0

    def __init__(self, rect, x, y):
        """ Initialize the Body class.

        Args:
            rect (pygame.Rect): The rect of the sprite.
            x (int): The initial x position of the sprite.
            y (int): The initial y position of the sprite.
        """
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
        """ Consume stored input and move the sprite.

        Handles gravity and collision detection with colliders.
        The sprite will move in the direction of the input, and will jump if the input is up.

        Args:
            dt (float): The delta time since the last frame.
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
        """
        # take input and apply movement speed
        self._velocity.x = self._input[0] * self._BASE_MOVEMENT_SPEED

        # jump + gravity
        self._apply_jump_input()
        self._apply_gravity(dt)

        move = self._velocity * dt

        # remember last direction
        if self.is_moving_horizontal():
            self.last_direction = 1 if self._velocity.x > 0 else -1

        # reset input
        self._input[0] = 0
        self._input[1] = 0

        self._move_and_collide(colliders, move)

    def add_input(self, dx, dy):
        """ Add movement input to be processed on the next move call.

        The input is added to the current input.
        Input will be consumed when the move() method is called.

        Args:
            dx (int): The input in the x direction.
            dy (int): The input in the y direction.
        """
        self._input[0] += dx
        self._input[1] += dy

    def _apply_jump_input(self):
        """ Set gravity to jump force or floor gravity based on input and on_floor status."""
        if self.on_floor:
            if self._input[1] < 0:
                self._gravity = self._BASE_JUMP_FORCE
            else:
                self._gravity = self._FLOOR_GRAVITY

    def _apply_gravity(self, dt):
        """ Apply gravity to vertical velocity and update accumulated gravity.

        Args:
            dt (float): The delta time since the last frame. 
        """
        self._velocity.y = self._gravity + dt * self._GRAVITY_CONSTANT / 2
        self._gravity += self._GRAVITY_CONSTANT * dt

        self._gravity = min(self._gravity, self._TERMINAL_VELOCITY)

    def _move_and_collide(self, colliders, move):
        """ Move the sprite and check for collisions with colliders.

        Args:
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
            move (pygame.Vector2): Delta time scaled movement vector to be applied to the sprite.
        """
        self.on_floor = False
        self.touching_wall = False

        # move in steps to avoid going through walls
        self._step_move(colliders, move, self._DIR_HORIZONTAL)
        self._step_move(colliders, move, self._DIR_VERTICAL)

        self._check_for_ground(colliders)

    def _step_move(self, colliders, move, direction):
        """ Move the sprite in steps to avoid going through walls.

        Args:
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
            move (pygame.Vector2): Delta time scaled movement vector to be applied to the sprite.
            direction (int): The direction to move in. 0 for horizontal, 1 for vertical.
        """
        if direction not in [self._DIR_HORIZONTAL, self._DIR_VERTICAL]:
            return

        while abs(move[direction]) > self._MOVE_EPSILON:
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
        """ Move one step horizontally and resolve collisions.

        Checks for collisions with colliders and adjusts the position of the sprite accordingly.

        Args:
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
        """
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
        """ Move one step vertically and resolve collisions.

        Checks for collisions with colliders and adjusts the position of the sprite accordingly.

        Args:
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
        """
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
        """ Update the on_floor status if the sprite is standing on the ground.

        Args:
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
        """

        # check if not going up
        if self._velocity[1] < 0:
            return

        self.rect.y += 1
        if pygame.sprite.spritecollide(self, colliders, False):
            self.on_floor = True
        self.rect.y -= 1

    def is_moving(self):
        """ Check if the sprite is moving in any direction.

        Returns:
            bool: True if the sprite is moving, False otherwise.
        """
        return self.is_moving_horizontal() or self.is_moving_vertical()

    def is_moving_horizontal(self):
        """ Check if the sprite is moving in the horizontal direction.

        Returns:
            bool: True if the sprite is moving horizontally, False otherwise.
        """
        return abs(self._velocity[0]) > self._MOVE_EPSILON

    def is_moving_vertical(self):
        """ Check if the sprite is moving in the vertical direction.

        Returns:
            bool: True if the sprite is moving vertically, False otherwise.
        """
        return abs(self._velocity[1]) > self._MOVE_EPSILON and not self.on_floor

    def get_velocity(self):
        """ Get the current velocity. 

        Returns:
            pygame.Vector2: The current velocity of the sprite.
        """
        return self._velocity
