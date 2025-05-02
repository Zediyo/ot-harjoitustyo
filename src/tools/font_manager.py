"""FontManager module that provides cached font loading and a fallback font for testing purposes."""

import pygame


class DummyFont:
    """Fallback font class used when pygame.font is not initialized.

    Always returns a blank surface when rendering text.
    """

    def render(self, _text, _antialias, _color):
        """Return a blank 1x1 surface as a placeholder."""
        return pygame.Surface((1, 1))


class FontManager:
    """A utility class for loading and caching fonts in Pygame.

    Provides a dummy font if Pygame's font system is not initialized.
    """
    _font_cache = {}
    _dummy_font = DummyFont()

    @classmethod
    def get_font(cls, size=24, name=None):
        """Get a cached Pygame font or load a new one.

        If the Pygame font system is not initialized, returns a dummy font
        that avoids crashes but does not render visible text.

        Args:
            size (int, optional): The font size. Defaults to 24.
            name (str or None, optional): Font name (None for default system font). Default is None.

        Returns:
            pygame.font.Font: The requested or fallback font object.
        """

        key = (name, size)

        if not pygame.font.get_init():
            return cls._dummy_font

        if key not in cls._font_cache:
            cls._font_cache[key] = pygame.font.SysFont(name, size)

        return cls._font_cache[key]

    @classmethod
    def clear(cls):
        """Clear all cached fonts."""
        cls._font_cache.clear()
