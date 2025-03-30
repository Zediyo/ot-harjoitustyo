import pygame

class Clock:
	def __init__(self):
		self._clock = pygame.time.Clock()

	def tick(self, fps):
		self._clock.tick(fps)

	def get_dt(self):
		return self._clock.get_time() / 1000.0