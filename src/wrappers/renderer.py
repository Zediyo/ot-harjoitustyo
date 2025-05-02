""" Renderer class for rendering the game scene. """
import pygame


class Renderer:
    """ Renderer class for rendering the game scene. """

    def __init__(self, display, scene):
        """ Initialize the Renderer.

        Args:
            display (pygame.Surface): The display surface to render on.
            scene (Scene): The scene to be rendered.
        """
        self._display = display
        self._scene = scene

    def render(self):
        """ Render the current scene to the display. """
        self._display.fill((0, 0, 0))

        self._scene.draw(self._display)

        pygame.display.flip()

    def set_scene(self, scene):
        """ Set the current scene to be rendered.

        Args:
            scene (Scene): The new scene to be rendered.
        """
        self._scene = scene
