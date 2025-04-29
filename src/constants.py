from enum import Enum, IntEnum

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

TILE_SIZE = 16
ENEMY_SIZE = 32
PLAYER_SIZE = 32
CURSOR_TILE_RANGE = 3

MAX_LEVEL_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAX_LEVEL_HEIGHT = SCREEN_HEIGHT // TILE_SIZE - (TILE_SIZE * 2)


class TileType(IntEnum):
    EMPTY = 0
    BLOCK = 1
    PLACEABLE = 2
    ENEMY = 3
    SPAWN = 4
    END = 5


TILE_COLORS = {
    TileType.EMPTY: (0, 0, 0),
    TileType.BLOCK: (200, 100, 100),
    TileType.PLACEABLE: (0, 0, 255),
    TileType.ENEMY: (255, 255, 255),
    TileType.SPAWN: (0, 255, 0),
    TileType.END: (255, 0, 0),
}


class Input(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    DOWN = "down"
    JUMP = "jump"

    MOUSE_LEFT = "mouse_left"
    MOUSE_RIGHT = "mouse_right"
    MOUSE_SCROLL_UP = "mouse_scroll_up"
    MOUSE_SCROLL_DOWN = "mouse_scroll_down"


class SceneName(str, Enum):
    MAIN_MENU = "mainmenu"
    LEVEL_LIST = "level_list"
    LEVEL = "level"
    EDITOR = "editor"
    END_SCREEN = "endscreen"


TEST_LEVEL_DATA = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 4, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, -4, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 3, -3, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, -3, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

TEST_LEVEL_END_DATA = [[0, 0, 4, -4, 0, 0],
                       [0, 0, -4, -4, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 5, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1]]
