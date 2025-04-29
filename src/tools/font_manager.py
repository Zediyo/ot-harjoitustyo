import pygame

class DummyFont:
    """Dummy font class used when pygame.font is not initialized."""
    def render(self, _text, _antialias, _color):
        return pygame.Surface((1, 1))

class FontManager:
    _fonts = {}
    _dummy_font = DummyFont()

    @classmethod
    def get_font(cls, size=24, name="Arial"):

        key = (name, size)

        if not pygame.font.get_init():
            return cls._dummy_font

        if key not in cls._fonts:
            cls._fonts[key] = pygame.font.SysFont(name, size)

        return cls._fonts[key]

    @classmethod
    def clear(cls):
        cls._fonts.clear()