import pygame
import constants

from scenes.main_menu import MainMenu
from wrappers.user_input import UserInput
from wrappers.renderer import Renderer
from wrappers.clock import Clock
from game_loop import GameLoop
from tools.db import init_db


def main():
    init_db()

    pygame.init()
    pygame.key.set_repeat(500, 50)

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
