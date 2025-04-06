import constants

class Map:
    def __init__(self, map_data, tile_size=constants.TILE_SIZE):
        self.data = map_data
        self.width = len(map_data[0])
        self.height = len(map_data)
        self._tile_size = tile_size
