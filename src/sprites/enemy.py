import pygame

from tools.asset_path import get_asset_path

from game.body import Body


class Enemy(pygame.sprite.Sprite):
    _TOUCHES_TO_JUMP = 3
    _TIME_AFTER_TOUCH = 0.3
    _DISTANCE_TO_JUMP = 90

    def __init__(self, x=0, y=0, start_dir=1):
        super().__init__()

        self.image = pygame.image.load(get_asset_path("pl_enemy.png"))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self._dir = start_dir

        self.body = Body(self.rect, x, y)

        self._touch_count = 0
        self._time_from_touch = 0.0

    def update(self, dt, colliders, player_rect):
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

        if player_rect.bottom >= self.rect.top:
            return False

        if self._dir == 1 and player_rect.x <= self.rect.x:
            return False

        if self._dir == -1 and player_rect.x >= self.rect.x:
            return False

        return True
