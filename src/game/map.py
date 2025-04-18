import constants


class Map:
    def __init__(self, map_data, tile_size=constants.TILE_SIZE):
        self.data = map_data
        self.width = len(map_data[0])
        self.height = len(map_data)
        self.tile_size = tile_size

    def tile_in_bounds(self, x, y):
        cell_x, cell_y = self.grid_pos_to_cell((x, y))
        return self.cell_in_bounds(cell_x, cell_y)

    def cell_in_bounds(self, cell_x, cell_y):
        return 0 <= cell_x < self.width and 0 <= cell_y < self.height

    def screen_pos_to_grid(self, pos):
        x, y = pos
        ret_x = round(x // self.tile_size * self.tile_size)
        ret_y = round(y // self.tile_size * self.tile_size)

        return ret_x, ret_y

    def grid_pos_to_cell(self, pos):
        x, y = pos
        ret_x = x // self.tile_size
        ret_y = y // self.tile_size

        return ret_x, ret_y

    def cell_pos_to_grid(self, pos):
        x, y = pos
        ret_x = x * self.tile_size
        ret_y = y * self.tile_size

        return ret_x, ret_y

    def screen_pos_to_cell(self, pos):
        x, y = self.screen_pos_to_grid(pos)
        return self.grid_pos_to_cell((x, y))

    # expand to screen size (centered)
    def expand_map(self, screen_w=constants.SCREEN_WIDTH, screen_h=constants.SCREEN_HEIGHT):
        new_width = screen_w // self.tile_size
        new_height = screen_h // self.tile_size

        pad_x = (new_width - self.width) // 2
        pad_y = (new_height - self.height) // 2

        new_map_data = [[0 for _ in range(new_width)]
                        for _ in range(new_height)]

        for y in range(self.height):
            for x in range(self.width):
                new_map_data[y+pad_y][x+pad_x] = self.data[y][x]

        self.data = new_map_data
        self.width = new_width
        self.height = new_height

    # shrink map to smallest rectangle that contains all tiles
    def shrink_map(self):
        min_x, min_y = self.width, self.height
        max_x, max_y = 0, 0

        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] != 0:
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
                new_map_data[y - min_y][x - min_x] = self.data[y][x]

        self.data = new_map_data
        self.width = new_width
        self.height = new_height

    def insert_cell(self, cell_x, cell_y, tile_id):
        if self.cell_in_bounds(cell_x, cell_y):
            self.data[cell_y][cell_x] = tile_id
            return True
        return False

    def remove_cell(self, cell_x, cell_y):
        if self.cell_in_bounds(cell_x, cell_y):
            self.data[cell_y][cell_x] = 0
            return True
        return False

    def get_cell(self, cell_x, cell_y):
        if self.cell_in_bounds(cell_x, cell_y):
            return self.data[cell_y][cell_x]
        return None

    def has_spawn(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] == constants.TILE_SPAWN:
                    return True
        return False

    def has_end(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] == constants.TILE_END:
                    return True
        return False

    # top left corner = x, y. depth = (width, height)
    def has_empty_area(self, x, y, depth=(1, 1)):
        width, height = depth
        for i in range(height):
            for j in range(width):
                if not self.cell_in_bounds(x + j, y + i) or self.data[y + i][x + j] != 0:
                    return False
        return True

    # top left corner = x, y. depth = (width, height). tile_id @ corner. -tile_id @ rest.
    def add_tile(self, x, y, tile_id, depth=(1, 1)):
        width, height = depth
        if not self.has_empty_area(x, y, depth):
            return False

        for i in range(height):
            for j in range(width):
                if i == 0 and j == 0:
                    self.insert_cell(x + j, y + i, tile_id)
                else:
                    self.insert_cell(x + j, y + i, -tile_id)
        return True

    def area_in_bounds(self, x, y, depth=(1, 1)):
        width, height = depth
        for i in range(height):
            for j in range(width):
                if not self.cell_in_bounds(x + j, y + i):
                    return False
        return True

    # top left corner = x, y. depth = (width, height). (rename to remove_area?)
    def remove_tile(self, x, y, depth=(1, 1)):
        width, height = depth
        if not self.area_in_bounds(x, y, depth):
            return False

        for i in range(height):
            for j in range(width):
                self.remove_cell(x + j, y + i)
        return True

    # find the nearest topleft corner of a tile with the given tile_id.
    # starting from x, y. max depth = (width, height).
    def find_nearest_corner(self, x, y, tile_id, depth=(1, 1)):
        max_x, max_y = depth
        if tile_id > 0:
            return (x, y) if self.get_cell(x, y) == tile_id else None

        for distance in range(1, max_x + max_y + 1):
            for i in range(0, min(distance, max_x) + 1):
                j = distance - i
                if j > max_y:
                    continue

                check_x = x - i
                check_y = y - j
                if not self.cell_in_bounds(check_x, check_y):
                    continue

                if self.get_cell(check_x, check_y) == -tile_id:
                    return (check_x, check_y)

        return None

    def is_map_viable(self):
        if not self.has_spawn():
            return False

        if not self.has_end():
            return False

        return True
