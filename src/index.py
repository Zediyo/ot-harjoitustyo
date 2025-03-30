import pygame
import constants

from level import Level
from di.event_queue import EventQueue
from di.renderer import Renderer
from di.clock import Clock
from di.input import Input
from game_loop import GameLoop

def main():

	display = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
	pygame.display.set_caption("Game")

	level = Level(constants.TEST_LEVEL)
	event_queue = EventQueue()
	renderer = Renderer(display, level)
	clock = Clock()
	input = Input()
	game_loop = GameLoop(level, renderer, event_queue, clock, input)

	pygame.init()
	game_loop.start()

if __name__ == "__main__":
	main()