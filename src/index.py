import pygame
import constants

from scenes.main_menu import MainMenu
from di.event_queue import EventQueue
from di.renderer import Renderer
from di.clock import Clock
from di.input import Input
from game_loop import GameLoop

def main():

	display = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
	pygame.display.set_caption("Game")

	scene = MainMenu()
	event_queue = EventQueue()
	renderer = Renderer(display, scene)
	clock = Clock()
	input = Input()
	game_loop = GameLoop(scene, renderer, event_queue, clock, input)

	pygame.init()
	game_loop.start()

if __name__ == "__main__":
	main()