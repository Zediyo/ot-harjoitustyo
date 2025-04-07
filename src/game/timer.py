from tools.db import get_best_time, save_level_time


class Timer:
    def __init__(self, level_id):
        self._time = 0.0
        self._level_id = level_id
        self._best_time = get_best_time(level_id)

        self._active = False

    def reset(self):
        self._time = 0.0

    def update(self, delta_time):
        if self._active:
            self._time += delta_time

    def get_time(self):
        return self._time

    def is_best_time(self):
        return self._best_time == -1 or self._time < self._best_time

    def get_best_time(self):
        return self._best_time if self._best_time != -1 else None

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def finish(self):
        self._active = False
        if self.is_best_time():
            save_level_time(self._level_id, self._time)
