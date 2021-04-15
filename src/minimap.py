"""
Minimap
"""
import math


class Minimap:

    DEFAULT_WALL_COLOR = 0x000000
    DEFAULT_EMPTY_COLOR = 0xFFFFFF
    DEFAULT_RAY_CAST_COLOR = 0xFF0000
    DEFAULT_FLOOR_CAST_COLOR = 0x00FF00
    DEFAULT_PLAYER_COLOR = 0xFF0000

    def __init__(self, scale, x=0, y=0):
        self.level = None
        self.scale = scale
        self.x = x
        self.y = y
        self.minimap = None
        self.wall_color = Minimap.DEFAULT_WALL_COLOR
        self.empty_color = Minimap.DEFAULT_EMPTY_COLOR
        self.ray_cast_color = Minimap.DEFAULT_RAY_CAST_COLOR
        self.floor_cast_color = Minimap.DEFAULT_FLOOR_CAST_COLOR
        self.player_color = Minimap.DEFAULT_PLAYER_COLOR
        self.show_ray_cast = False
        self.show_player = True
        self.show_floor_cast = False
        self.show_ceil_cast = False

    def set_level(self, level):
        self.level = level
        self.reset_minimap()

    def show(self, *, player=True, ray_cast=False, floor_cast=False):
        self.show_player = player
        self.show_ray_cast = ray_cast
        self.show_floor_cast = floor_cast

    def reset_minimap(self):
        scale = self.scale
        self.minimap = [
            [self.empty_color for x in range(self.level.width * scale)]
            for _ in range(self.level.height * scale)
        ]
        for y in range(self.level.height):
            for x in range(self.level.width):
                tile_id = self.level.get_wall_map_tile_by_coords(x, y)
                tile = self.level.get_tile_by_id(tile_id)
                if tile and not tile.is_wall:
                    continue
                minimap_x = x * scale
                minimap_y = y * scale
                for my in range(minimap_y, minimap_y + scale):
                    for mx in range(minimap_x, minimap_x + scale):
                        self.minimap[my][mx] = self.wall_color

    def set_pixel(self, x, y, pixel):
        scale = self.scale
        x *= scale
        y *= scale
        x = math.floor(x)
        y = math.floor(y)
        self.minimap[y][x] = pixel
