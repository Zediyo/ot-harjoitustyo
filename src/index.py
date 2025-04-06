import pygame
import constants

from scenes.main_menu import MainMenu
from di.user_input import UserInput
from di.renderer import Renderer
from di.clock import Clock
from game_loop import GameLoop


def main():
    pygame.init()

    display = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Game")

    scene = MainMenu()
    user_input = UserInput()
    renderer = Renderer(display, scene)
    clock = Clock()

    game_loop = GameLoop(scene, renderer, user_input, clock)

    game_loop.start()


if __name__ == "__main__":
    main()
