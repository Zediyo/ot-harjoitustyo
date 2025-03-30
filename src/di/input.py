import pygame

class Input:
	def get_pressed(self):
		return pygame.key.get_pressed()
    
	def get_mouse_pos(self):
		return pygame.mouse.get_pos()