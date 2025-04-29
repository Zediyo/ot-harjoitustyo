"""Contains the Player sprite class, representing the player character in the game."""

import pygame

from constants import Settings
from tools.asset_helpers import load_image

from game.body import Body
from game.sprite_animation import SpriteAnimation


class Player(pygame.sprite.Sprite):
    """ The main player character controlled by the user.

    The player can move left and right, jump, and interact with the game world.
    The player has animations for moving, jumping, falling, and idling.
    Collides with the game world and is affected by gravity.

    Attributes:
        image (pygame.Surface): The image representing the player.
        rect (pygame.Rect): The rectangle representing the player's position and size.
        charges (int): The number of placeable blocks player has available.
    """

    _MOVE_ANIMATION = ("player_move_spritesheet.png", (19, 16), 8)
    _IDLE_ANIMATION = ("player_idle_spritesheet.png", (17, 16), 8)
    _SIZE = (Settings.PLAYER_SIZE, Settings.PLAYER_SIZE)

    _DIR_LEFT = -1

    # Manually calculated values for the air frames
    _ASCEND_START_VEL = -280
    _DESCEND_END_VEL = 280

    # (frame 0 = ground, 1-2 = ascending, 3-4 = peak, 5-6 = descending, 7 = ground)
    _AIR_FRAME_CUT_OFFS = [0.15, 0.30, 0.50, 0.70, 0.85, 1.10]

    def __init__(self, x=0, y=0):
        """ Initialize the Player sprite.

        Args:
            x (int, optional): The initial x world position of the player. Defaults to 0.
            y (int, optional): The initial y world position of the player. Defaults to 0.
        """

        super().__init__()

        self._base = load_image("pl_player.png")
        self._base.set_alpha(100)

        self._animation = SpriteAnimation(fps=15, scale=self._SIZE)
        self._animation.add_image_set("move", *self._MOVE_ANIMATION)
        self._animation.add_image_set("idle", *self._IDLE_ANIMATION)

        self.image = pygame.Surface(self._SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._body = Body(self.rect, x, y)
        self.charges = 3

    def _animate(self, dt):
        """ Update the player's animation based on the current state.

        Args:
            dt (float): The delta time since the last frame.
        """
        self._animation.update(dt)

        # select frame based on movement type
        frame = self._get_animation_frame()

        # flip frame if moving left
        if self._body.last_direction == self._DIR_LEFT:
            frame = pygame.transform.flip(frame, True, False)

        # overlay the frame on the base image
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self._base, (0, 0))
        self.image.blit(frame, (0, 0))

    def move(self, dt, colliders):
        """ Move the player and update animation.

        Applies movement input and physics to update the player's position, 
        then updates the animation based on the new state.

        Args:
            dt (float): The delta time since the last frame.
            colliders (pygame.sprite.Group): The group of colliders to check for collisions with.
        """
        self._body.move(dt, colliders)
        self._animate(dt)

    def add_input(self, dx, dy):
        """ Add movement input to be processed on the next move call.

        Args:
            dx (int): The x-axis input (-1 for left, 1 for right, 0 for no movement).
            dy (int): The y-axis input (-1 for jump, 1 for down, 0 for no movement).
        """
        self._body.add_input(dx, dy)

    def _get_animation_frame(self):
        """ Get the current animation frame based on the player's state.

        Returns:
            pygame.Surface: The correct animation frame for the player.
        """
        # first air frame
        if self._animation.get_mode() == 0 and not self._body.on_floor:
            self._animation.change_mode(1, 0)
            return self._animation.get_frame("move")

        # first ground frame
        if self._animation.get_mode() == 1 and self._body.on_floor:
            self._animation.change_mode(0, 7)
            return self._animation.get_frame("move")

        # jumping or falling
        if not self._body.on_floor:
            return self._get_air_frame()

        if self._body.is_moving():
            return self._animation.get_frame("move")

        return self._animation.get_frame("idle")

    def _get_air_frame(self):
        """ Select the correct frame based on the player's vertical velocity.

        Returns:
            pygame.Surface: The correct air frame for the player.
        """
        vel_y = self._body.get_velocity().y

        ascend_start_vel = self._ASCEND_START_VEL
        descend_end_vel = self._DESCEND_END_VEL

        # normalize to [0, 1]
        if vel_y < ascend_start_vel:
            normalized = 0.0
        elif vel_y > descend_end_vel:
            normalized = 1.0
        else:
            normalized = (vel_y - ascend_start_vel) / \
                (descend_end_vel - ascend_start_vel)

        cut_offs = self._AIR_FRAME_CUT_OFFS

        target_index = 1
        for cut_off in cut_offs:
            if normalized < cut_off:
                break
            target_index += 1

        return self._animation.get_frame("move", target_index)
