import pygame


class Renderer:
	def __init__(self, display, level):
		self._display = display
		self._level = level

	def render(self):
		self._display.fill((0, 0, 0))
		
		self._level.all_sprites.draw(self._display)

		pygame.display.flip()