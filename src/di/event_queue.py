import pygame

class EventQueue:
	def get(self):
		return pygame.event.get()