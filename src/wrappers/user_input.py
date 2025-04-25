import pygame


class UserInput:
    def get_events(self):
        return pygame.event.get()

    def get_pressed(self):
        return pygame.key.get_pressed()

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def get_mouse_pressed(self):
        return pygame.mouse.get_pressed()
