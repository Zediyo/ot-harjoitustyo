""" Contains the Enemy sprite class, representing a standard enemy in the game."""

import pygame

from tools.asset_helpers import load_image
from constants import Settings
from game.body import Body
from game.sprite_animation import SpriteAnimation


class Enemy(pygame.sprite.Sprite):
    """ A basic enemy that moves left and right and jumps toward the player.

    The enemy moves left and right, changing direction when it touches a wall, and
    can jump towards the player under certain conditions. The enemy has a simple
    animation for its movement.

    Attributes:
        image (pygame.Surface): The image representing the enemy.
        rect (pygame.Rect): The rectangle representing the enemy's position and size.
    """
    _TOUCHES_TO_JUMP = 3
    _TIME_AFTER_TOUCH = 0.3
    _DISTANCE_TO_JUMP = 90

    _MOVE_ANIMATION = ("enemy_spritesheet.png", (72, 51), 5)
    _SIZE = (Settings.ENEMY_SIZE, Settings.ENEMY_SIZE)

    _DIR_LEFT = -1
    _DIR_RIGHT = 1

    def __init__(self, x=0, y=0, start_dir=1):
        """ Initialize the Enemy sprite.

        Args:
            x (int): The initial x world position of the enemy.
            y (int): The initial y world position of the enemy.
            start_dir (int): The initial direction of the enemy. 1 for right, -1 for left.
        """
        super().__init__()

        self._base = load_image("pl_enemy.png")
        self._base.set_alpha(100)

        self._animation = SpriteAnimation(fps=15, scale=self._SIZE)
        self._animation.add_image_set("move", *self._MOVE_ANIMATION)

        self.image = pygame.Surface(self._SIZE)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self._dir = start_dir

        self._body = Body(self.rect, x, y)

        self._touch_count = 0
        self._time_from_touch = 0.0

    def _animate(self, dt):
        """ Update the enemy's animation based on the time elapsed.

        Args:
            dt (float): The delta time since the last frame.
        """
        self._animation.update(dt)

        frame = self._animation.get_frame("move")

        # flip if moving right
        if self._dir == self._DIR_RIGHT:
            frame = pygame.transform.flip(frame, True, False)

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self._base, (0, 0))
        self.image.blit(frame, (0, 0))

    def update(self, dt, colliders, player_rect):
        """ Update the enemy's position and animation.

        Args:
            dt (float): The delta time since the last frame.
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
            player_rect (pygame.Rect): The rectangle representing the player's position.
        """
        self._animate(dt)

        if self._body.touching_wall:
            self._dir *= -1
            self._touch_count += 1

        # jump after 3 touches and 0.3 seconds
        if self._touch_count >= self._TOUCHES_TO_JUMP:
            self._time_from_touch += dt

        if self._time_from_touch >= self._TIME_AFTER_TOUCH:
            self._touch_count = 0
            self._time_from_touch = 0.0
            self._body.add_input(0, -1)

        # jump if moving towards player and player is above enemy and within range
        if self._should_jump(player_rect):
            self._body.add_input(0, -1)

        self._body.add_input(self._dir, 0)
        self._body.move(dt, colliders)

    def _should_jump(self, player_rect):
        """ Determine if the enemy should jump towards the player.

        Args:
            player_rect (pygame.Rect): The rectangle representing the player's position.

        Returns:
            bool: True if the enemy should jump, False otherwise.
        """
        if abs(player_rect.x - self.rect.x) > self._DISTANCE_TO_JUMP:
            return False

        if abs(player_rect.bottom - self.rect.top) > self._DISTANCE_TO_JUMP:
            return False

        if player_rect.bottom + 1 >= self.rect.bottom:
            return False

        if self._dir == self._DIR_RIGHT and player_rect.x <= self.rect.x:
            return False

        if self._dir == self._DIR_LEFT and player_rect.x >= self.rect.x:
            return False

        return True
