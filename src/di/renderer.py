import pygame


class Renderer:
	def __init__(self, display, scene):
		self._display = display
		self._scene = scene

	def render(self):
		self._display.fill((0, 0, 0))
		
		self._scene.draw(self._display)

		pygame.display.flip()

	def set_scene(self, scene):
		self._scene = scene