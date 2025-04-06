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
