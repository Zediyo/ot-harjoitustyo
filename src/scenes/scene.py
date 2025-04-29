""" Contains the base class for all game scenes."""

from constants import SceneName


class Scene():
    """ Base class for all game scenes.

    Defines the interface for all scenes in the game.
    Scenes should inherit from this class and override the necessary methods.
    """

    def __init__(self):
        self._next_scene = None

    def input_key(self, key):
        """Handle keyboard input.

        Args:
            key (Input): The input action (e.g., Input.LEFT, Input.RIGHT, Input.JUMP).
        """

    def input_mouse(self, click, pos):
        """Handle mouse button input.

        Args:
            click (Input): The mouse input action (e.g., Input.MOUSE_LEFT, Input.MOUSE_RIGHT).
            pos (tuple[int, int]): The mouse position (x, y) on screen.
        """

    def input_mouse_hold(self, click, pos):
        """Handle mouse button hold input.

        Args:
            click (Input): The mouse input action held down.
            pos (tuple[int, int]): The mouse position (x, y) on screen.
        """

    def input_raw(self, events):
        """Handle raw input events from Pygame.

        Args:
            events (list[pygame.event.Event]): List of Pygame events to process.
        """

    def update(self, dt, mouse_pos):
        """Update the scene state.

        Args:
            dt (float): Time delta since the last frame.
            mouse_pos (tuple[int, int]): Current mouse position.
        """

    def draw(self, display):
        """Draw all scene elements onto the given display surface.

        Args:
            display (pygame.Surface): The surface to draw on.
        """

    def cleanup(self):
        """Clean up the scene before transitioning."""

    def is_done(self):
        """Check if the scene has finished and wants to transition.

        Returns:
            bool: True if the scene is done, False otherwise.
        """
        return self._next_scene is not None

    def get_next_scene(self) -> SceneName | None:
        """Get the next scene to transition to.

        Returns:
            SceneName or None: The next scene to transition to.
        """
        return self._next_scene[0] if self._next_scene else None

    def get_next_scene_data(self):
        """Get the data associated with the next scene.

        Returns:
            Any: Data to pass to the next scene, or None if no data is set.
        """
        return self._next_scene[1] if self._next_scene else None

    def set_next_scene(self, scene: SceneName, data=None):
        """Set the next scene and optional data.

        Args:
            scene (SceneName): The name of the next scene.
            data (Any, optional): Additional data for the next scene.
        """
        self._next_scene = (scene, data)
