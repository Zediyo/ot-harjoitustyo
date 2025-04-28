""" Contains the Map class, which represents a 2D grid of tiles for game levels. """

import constants


class Map:
    """ Map class represents a 2D grid of tiles for a game level.

    Handles tile data, dimensions, and provides methods for manipulating the map.
    Allows for operations such as tile placement, removal, bounds and area checking,
    iterating over cells and map resizing,
    as well as performing coordinate conversion between screen, world and cell space.

    Attributes:
        data (list[list[int]]): 2D list representing the map data, where each element is a tile ID.
        width (int): Width of the map in cells.
        height (int): Height of the map in cells.
        tile_size (int): Size of each tile in pixels.
    """

    def __init__(self, map_data, tile_size=constants.TILE_SIZE):
        """ Initializes the Map object.

        Args:
            map_data (list[list[int]]): 2D list of tile IDs.
            tile_size (int, optional): Size of each tile in pixels. Defaults to constants.TILE_SIZE.
        """
        self._data = map_data
        self._width = len(map_data[0])
        self._height = len(map_data)
        self._tile_size = tile_size

    @property
    def data(self):
        """ list[list[int]]: 2D list of tile IDs representing the map. Read-only property. """
        return self._data

    @property
    def width(self):
        """ int: Width of the map in cells. Read-only property. """
        return self._width

    @property
    def height(self):
        """ int: Height of the map in cells. Read-only property. """
        return self._height

    @property
    def tile_size(self):
        """ int: Size of each tile in pixels. Read-only property. """
        return self._tile_size

    def iterate_cells(self):
        """ Yield the indices and tile ID of each cell in the map.

        Yields:
            tuple[int, int, int]: Contains (cell_x, cell_y, tile_id) for each cell.
        """
        for y in range(self._height):
            for x in range(self._width):
                yield x, y, self._data[y][x]

    def snap_to_grid(self, pos):
        """ Snap screen position to the nearest grid-aligned position.

        Args:
            pos (tuple[float, float]): The screen position to snap.

        Returns:
            tuple[int, int]: The snapped position aligned to the grid.

        """
        x, y = pos
        ret_x = round(x // self._tile_size * self._tile_size)
        ret_y = round(y // self._tile_size * self._tile_size)

        return ret_x, ret_y

    def cell_index_to_world_pos(self, pos):
        """ Convert cell indices (cell_x, cell_y) to world position.

        Args:
            pos (tuple[int, int]): The indices of a single cell.

        Returns:
            tuple[int, int]: The world position of the cell's top-left corner.
        """
        x, y = pos
        ret_x = x * self._tile_size
        ret_y = y * self._tile_size

        return ret_x, ret_y

    def screen_to_cell_index(self, pos):
        """ Convert screen position to a single cell's indices.

        Args:
            pos (tuple[float, float]): The screen position to convert.

        Returns:
            tuple[int, int]: The cell indices (cell_x, cell_y) at the given screen position.
        """

        x, y = self.snap_to_grid(pos)
        ret_x = x // self._tile_size
        ret_y = y // self._tile_size
        return ret_x, ret_y

    def expand_map(self, screen_w=constants.SCREEN_WIDTH, screen_h=constants.SCREEN_HEIGHT):
        """ Expand the map to the given screen size, centering the current map data.

        Args:
            screen_w (int, optional): Width in pixels. Defaults to constants.SCREEN_WIDTH.
            screen_h (int, optional): Height in pixels. Defaults to constants.SCREEN_HEIGHT.
        """
        new_width = screen_w // self._tile_size
        new_height = screen_h // self._tile_size

        pad_x = (new_width - self._width) // 2
        pad_y = (new_height - self._height) // 2

        new_map_data = [[0 for _ in range(new_width)]
                        for _ in range(new_height)]

        for y in range(self._height):
            for x in range(self._width):
                new_map_data[y+pad_y][x+pad_x] = self._data[y][x]

        self._data = new_map_data
        self._width = new_width
        self._height = new_height

    def shrink_map(self):
        """ Shrink the map to the smallest rectangle that contains all non-zero tiles. """
        min_x, min_y = self._width, self._height
        max_x, max_y = 0, 0

        for y in range(self._height):
            for x in range(self._width):
                if self._data[y][x] != 0:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        new_width = max_x - min_x + 1
        new_height = max_y - min_y + 1

        new_map_data = [[0 for _ in range(new_width)]
                        for _ in range(new_height)]

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                new_map_data[y - min_y][x - min_x] = self._data[y][x]

        self._data = new_map_data
        self._width = new_width
        self._height = new_height

    def get_tile_at_cell(self, cell_x, cell_y):
        """ Get the tile ID at the specified cell.

        Args:
            cell_x (int): The x index of the cell.
            cell_y (int): The y index of the cell.

        Returns:
            int or None: The tile ID at the specified cell, or None if out of bounds.
        """
        if self.cell_in_bounds(cell_x, cell_y):
            return self._data[cell_y][cell_x]
        return None

    def set_tile_at_cell(self, cell_x, cell_y, tile_id):
        """ Set the tile ID at the specified cell.

        Args:
            cell_x (int): The x index of the cell.
            cell_y (int): The y index of the cell.
            tile_id (int): The tile ID to set.

        Returns:
            bool: True if the tile was set successfully, False if out of bounds.
        """
        if self.cell_in_bounds(cell_x, cell_y):
            self._data[cell_y][cell_x] = tile_id
            return True
        return False

    def cell_in_bounds(self, cell_x, cell_y):
        """ Check if the specified cell is within the map bounds.

        Args:
            cell_x (int): The x index of the cell.
            cell_y (int): The y index of the cell.

        Returns:
            bool: True if the cell is within bounds, False otherwise.
        """
        return 0 <= cell_x < self._width and 0 <= cell_y < self._height

    def contains_tile(self, tile_id):
        """ Check if the map contains a tile with the specified ID.

        Args:
            tile_id (int): The tile ID to check for.

        Returns:
            bool: True if the tile ID is found in the map, False otherwise.
        """
        for y in range(self._height):
            for x in range(self._width):
                if self._data[y][x] == tile_id:
                    return True
        return False

    def is_empty_area(self, x, y, depth=(1, 1)):
        """ Check if the rectangular area of cells is empty.

        All cells in the area must be empty (0) and within the map bounds.

        Args:
            x (int): The x index of the area's top-left cell.
            y (int): The y index of the area's top-left cell.
            depth (tuple[int, int], optional): The width and height of the area. Defaults to (1, 1).

        Returns:
            bool: True if the area is entirely empty and within bounds, False otherwise.
        """
        width, height = depth
        for i in range(height):
            for j in range(width):
                if not self.cell_in_bounds(x + j, y + i) or self._data[y + i][x + j] != 0:
                    return False
        return True

    def is_area_in_bounds(self, x, y, depth=(1, 1)):
        """ Check if the rectangular area of cells is within the map bounds.

        Args:
            x (int): The x index of the area's top-left cell.
            y (int): The y index of the area's top-left cell.
            depth (tuple[int, int], optional): The width and height of the area. Defaults to (1, 1).

        Returns:
            bool: True if the area is entirely within bounds, False otherwise.
        """
        width, height = depth
        for i in range(height):
            for j in range(width):
                if not self.cell_in_bounds(x + j, y + i):
                    return False
        return True

    def add_multi_tile(self, x, y, tile_id, depth=(1, 1)):
        """ Add a multi-tile area to the map.

        Places a tile with the given tile_id at the area's top-left cell (x, y),
        and fills the rest of the cells in the area with -tile_id.

        Args:
            x (int): The x index of the area's top-left cell.
            y (int): The y index of the area's top-left cell.
            tile_id (int): The tile ID to set at the top-left cell.
            depth (tuple[int, int], optional): The width and height of the area. Defaults to (1, 1).

        Returns:
            bool: True if the area was added successfully,
                False if the area is not empty or if any cell in the area is out of bounds.
        """
        width, height = depth
        if not self.is_empty_area(x, y, depth):
            return False

        for i in range(height):
            for j in range(width):
                if i == 0 and j == 0:
                    self.set_tile_at_cell(x + j, y + i, tile_id)
                else:
                    self.set_tile_at_cell(x + j, y + i, -tile_id)
        return True

    def remove_multi_tile(self, x, y, depth=(1, 1)):
        """ Remove all tiles from the rectangular area of cells.

        Args:
            x (int): The x index of the area's top-left cell.
            y (int): The y index of the area's top-left cell.
            depth (tuple[int, int], optional): The width and height of the area. Defaults to (1, 1).

        Returns:
            bool: True if the area was removed successfully, False if any cell is out of bounds.
        """
        width, height = depth
        if not self.is_area_in_bounds(x, y, depth):
            return False

        for i in range(height):
            for j in range(width):
                self.set_tile_at_cell(x + j, y + i, 0)
        return True

    def find_nearest_tile_corner(self, x, y, tile_id, depth=(1, 1)):
        """ Find the nearest top-left cell of a tile in area with the given tile_id.

        If given tile_id is positive, only the starting cell (x, y) is checked.
        If given tile_id is negative, searches for the nearest cell with the same absolute tile id.

        Searches in a diamond pattern from the starting cell (x, y) and expanding outwards.
        The search area is limited to the given depth in both x and y directions from the center.

        Args:
            x (int): The x index of the starting cell (center of the area).
            y (int): The y index of the starting cell (center of the area).
            tile_id (int): The tile ID to search for.
            depth (tuple[int, int], optional): The x and y distance from center. Defaults to (1, 1).

        Returns:
            tuple[int, int] or None: The cell indices of the corner if found, None otherwise.
        """
        max_x, max_y = depth
        if tile_id > 0:
            return (x, y) if self.get_tile_at_cell(x, y) == tile_id else None

        for distance in range(1, max_x + max_y + 1):
            for i in range(0, min(distance, max_x) + 1):
                j = distance - i
                if j > max_y:
                    continue

                check_x = x - i
                check_y = y - j
                if not self.cell_in_bounds(check_x, check_y):
                    continue

                if self.get_tile_at_cell(check_x, check_y) == -tile_id:
                    return (check_x, check_y)

        return None

    def is_map_viable(self):
        """ Check if the map has a valid start and end point.

        Returns:
            bool: True if the map has a valid start and end point, False otherwise.
        """
        return self.contains_tile(constants.TILE_SPAWN) and self.contains_tile(constants.TILE_END)
