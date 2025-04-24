import pygame
from tools.asset_helpers import load_image

from game.body import Body
from game.sprite_animation import SpriteAnimation


class Player(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        super().__init__()

        self._base = load_image("pl_player.png")
        self._base.set_alpha(100)

        self._animation = SpriteAnimation(fps=15, scale=(32, 32))
        self._animation.add_image_set(
            "move", "player_move_spritesheet.png", (19, 16), 8)
        self._animation.add_image_set(
            "idle", "player_idle_spritesheet.png", (17, 16), 8)

        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.body = Body(self.rect, x, y)
        self.charges = 3

    def _animate(self, dt):
        self._animation.update(dt)

        # select frame based on movement type
        frame = self._get_animation_frame()

        # flip frame if moving left
        if self.body.last_direction == -1:
            frame = pygame.transform.flip(frame, True, False)

        # overlay the frame on the base image
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self._base, (0, 0))
        self.image.blit(frame, (0, 0))

    def move(self, dt, colliders):
        self.body.move(dt, colliders)
        self._animate(dt)

    def add_input(self, dx, dy):
        self.body.add_input(dx, dy)

    def _get_animation_frame(self):
        # first air frame
        if self._animation.get_previous_state() == 0 and not self.body.on_floor:
            self._animation.set_previous_state(1)
            self._animation.reset_animation()
            return self._animation.get_frame("move", 0)

        # first ground frame
        if self._animation.get_previous_state() == 1 and self.body.on_floor:
            self._animation.set_previous_state(0)
            self._animation.reset_animation()
            return self._animation.get_frame("move", 7)

        # jumping or falling
        if not self.body.on_floor:
            return self._get_air_frame()

        if self.body.is_moving():
            return self._animation.get_frame("move")

        return self._animation.get_frame("idle")

    def _get_air_frame(self):
        vel_y = self.body.get_velocity().y

        ascend_start_vel = -280
        descend_end_vel = 280

        # normalize to [0, 1]
        if vel_y < ascend_start_vel:
            normalized = 0.0
        elif vel_y > descend_end_vel:
            normalized = 1.0
        else:
            normalized = (vel_y - ascend_start_vel) / \
                (descend_end_vel - ascend_start_vel)

        # (frame 0 = ground, 1-2 = ascending, 3-4 = peak, 5-6 = descending, 7 = ground)
        cut_offs = [0.15, 0.30, 0.50, 0.70, 0.85, 1.10]

        target_index = 1
        for cut_off in cut_offs:
            if normalized < cut_off:
                break
            target_index += 1

        return self._animation.get_frame("move", target_index)
