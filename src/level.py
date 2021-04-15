"""
Level
"""
from tile import Tile, WallTile, FloorTile, CeilTile, EmptyTile


###############################################################################
# Exceptions
###############################################################################


class LevelError(Exception):
    pass


###############################################################################
# Classes
###############################################################################


class Level:

    DEFAULT_WALL_TILE_ID = -1
    DEFAULT_EMPTY_TILE_ID = -2
    DEFAULT_FLOOR_COLOR = 0x007004
    DEFAULT_CEIL_COLOR = 0x0463ca
    DEFAULT_WALL_COLOR = 0x473a01

    def __init__(self, width, height, tile_size, player):
        self.width, self.height = self._validate_size(width, height)
        self.tiles = []
        self.tile_size = tile_size

        self.default_floor_tile_id = None
        self.default_ceil_tile_id = None
        self.default_wall_tile_id = Level.DEFAULT_WALL_TILE_ID

        self.minimap = None
        self.set_player(player)

        # Maps
        self.cast_ceil_map = False
        self.cast_floor_map = False
        self.wall_map = None
        self.floor_map = None
        self.ceil_map = None

        self.floor_color = Level.DEFAULT_FLOOR_COLOR
        self.ceil_color = Level.DEFAULT_CEIL_COLOR

        self._register_default_entities()
        self.generate_maps()

    ###########################################################################
    # Public methods
    ###########################################################################

    def set_player(self, player):
        self.player = player
        self.player.level = self

    def set_minimap(self, minimap):
        self.minimap = minimap
        self.minimap.set_level(self)

    def generate_maps(self):
        self._generate_wall_map()
        if self.cast_floor:
            self._generate_floor_map()
        if self.cast_ceil:
            self._generate_ceil_map()

    def set_default_floor_tile_id(self, tile_id):
        self.default_floor_tile_id = tile_id

    def set_default_ceil_tile_id(self, tile_id):
        self.default_ceil_tile_id = tile_id

    def set_default_wall_tile_id(self, tile_id):
        self.default_wall_tile_id = tile_id

    def register_tile(self, entity):
        self.tiles.append(entity)

    def set_tile_on_wall_map(self, entity_id, x, y):
        self._validate_coords(x, y)
        self.wall_map[y][x] = entity_id

    def set_tile_on_floor_map(self, entity_id, x, y):
        self._validate_coords(x, y)
        self.floor_map[y][x] = entity_id

    def set_tile_on_ceil_map(self, entity_id, x, y):
        self._validate_coords(x, y)
        self.ceil_map[y][x] = entity_id

    def cast_ceil(self, cast):
        self.cast_ceil_map = cast

    def cast_floor(self, cast):
        self.cast_floor_map = cast

    def set_floor_color(self, color):
        self.floor_color = color

    def set_ceil_color(self, color):
        self.ceil_color = color

    def get_tile_by_id(self, id):
        for tile in self.tiles:
            if tile.id == id:
                return tile
        return None

    def get_wall_map_tile_by_coords(self, x, y):
        self._validate_coords(x, y)
        return self.wall_map[y][x]

    def get_floor_map_tile_by_coords(self, x, y):
        self._validate_coords(x, y)
        return self.floor_map[y][x]

    def get_ceil_map_tile_by_coords(self, x, y):
        self._validate_coords(x, y)
        return self.ceil_map[y][x]

    def set_default_wall_texture(self, texture):
        pass

    def set_default_floor_texture(self, texture):
        pass

    ###########################################################################
    # Private methods
    ###########################################################################

    def _validate_size(self, width, height):
        if width < 3 or height < 3:
            raise LevelError('The level must has at least 3x3 size')
        return width, height

    def _validate_coords(self, x, y):
        if x < 0 or x >= self.width:
            raise LevelError(f'The X coord is out of bounds {x, y}')
        if y < 0 or y >= self.height:
            raise LevelError(f'The Y coord is out of bounds {x, y}')

    def _register_default_entities(self):
        wall = WallTile(Level.DEFAULT_WALL_TILE_ID, 'wall', \
            Level.DEFAULT_WALL_COLOR)
        empty = EmptyTile(Level.DEFAULT_EMPTY_TILE_ID, 'empty')
        self.tiles.append(wall)
        self.tiles.append(empty)

    def _generate_wall_map(self):
        self.wall_map = [
            [Level.DEFAULT_EMPTY_TILE_ID for x in range(self.width)]
            for _ in range(self.height)
        ]
        for x in range(self.width):
            self.wall_map[0][x] = self.default_wall_tile_id
            self.wall_map[self.height - 1][x] = self.default_wall_tile_id
        for y in range(self.height):
            self.wall_map[y][0] = self.default_wall_tile_id
            self.wall_map[y][self.width - 1] = self.default_wall_tile_id

    def _generate_floor_map(self):
        self.floor_map = [
            [self.default_floor_tile_id for x in range(self.width)]
            for _ in range(self.height)
        ]

    def _generate_ceil_map(self):
        self.ceil_map = [
            [self.default_ceil_tile_id for x in range(self.width)]
            for _ in range(self.height)
        ]
