import pygame

from tools.asset_path import get_asset_path

from game.body import Body
from game.sprite_animation import SpriteAnimation


class Enemy(pygame.sprite.Sprite):
    _TOUCHES_TO_JUMP = 3
    _TIME_AFTER_TOUCH = 0.3
    _DISTANCE_TO_JUMP = 90

    def __init__(self, x=0, y=0, start_dir=1):
        super().__init__()

        self._base = pygame.image.load(get_asset_path("pl_enemy.png"))
        self._base.set_alpha(100)

        self._animation = SpriteAnimation(fps=15, scale=(32, 32))
        self._animation.add_image_set("move", "enemy_spritesheet.png", (72, 51), 5)

        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self._dir = start_dir

        self.body = Body(self.rect, x, y)

        self._touch_count = 0
        self._time_from_touch = 0.0

    def _animate(self, dt):
        self._animation.update(dt)

        frame = self._animation.get_frame("move")

        # flip if moving right
        if self._dir == 1:
            frame = pygame.transform.flip(frame, True, False)

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self._base, (0, 0))
        self.image.blit(frame, (0, 0))


    def update(self, dt, colliders, player_rect):
        self._animate(dt)

        if self.body.touching_wall:
            self._dir *= -1
            self._touch_count += 1

        # jump after 3 touches and 0.3 seconds
        if self._touch_count >= self._TOUCHES_TO_JUMP:
            self._time_from_touch += dt

        if self._time_from_touch >= self._TIME_AFTER_TOUCH:
            self._touch_count = 0
            self._time_from_touch = 0.0
            self.body.add_input(0, -1)

        # jump if moving towards player and player is above enemy and withing range
        if self._should_jump(player_rect):
            self.body.add_input(0, -1)

        self.body.add_input(self._dir, 0)
        self.body.move(dt, colliders)

    def _should_jump(self, player_rect):
        if abs(player_rect.x - self.rect.x) > self._DISTANCE_TO_JUMP:
            return False

        if abs(player_rect.bottom - self.rect.top) > self._DISTANCE_TO_JUMP:
            return False

        if player_rect.bottom+1 >= self.rect.bottom:
            return False

        if self._dir == 1 and player_rect.x <= self.rect.x:
            return False

        if self._dir == -1 and player_rect.x >= self.rect.x:
            return False

        return True
