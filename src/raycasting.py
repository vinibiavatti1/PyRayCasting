"""
RayCasting
"""
import math
import calc
from player import Player


###############################################################################
# Exceptions
###############################################################################


class RayCastingError(Exception):
    pass


###############################################################################
# Classes
###############################################################################


class RayCasting:
    def __init__(self, width, height, tile_size, level, player, pixels):
        self.level = level
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.half_width = width // 2
        self.half_height = height // 2
        self.precision = self.tile_size
        self.player = self._validate_player_coords(player)
        self.pixels = pixels
        self.projection_plane_distance = \
            self._calculate_distance_projection_plane(
                self.half_width
            )
        self.minimap = level.minimap

    ###########################################################################
    # Public Methods
    ###########################################################################

    def process(self):
        if self.minimap:
            self.minimap.reset_minimap()
            if self.minimap.show_player:
                self.minimap.set_pixel(
                    self.player.x,
                    self.player.y,
                    self.minimap.player_color
                )
        self.raycasting()
        if self.minimap:
            self._draw_minimap()

    def raycasting(self):
        current_angle = self.player.angle - (self.player.fov / 2)
        current_angle %= 360
        inc_angle = self.player.fov / self.width
        player_rad = calc.dg_to_rad(self.player.angle)
        for x in range(self.width):
            rad = calc.dg_to_rad(current_angle)

            cos = math.cos(rad) / self.precision
            sin = math.sin(rad) / self.precision

            level_x = self.player.x
            level_y = self.player.y
            tile = None
            while tile is None or not tile.solid:
                identifier = self.level.wall_map[
                    math.floor(level_y)
                ][
                    math.floor(level_x)
                ]
                tile = self.level.get_tile_by_id(identifier)

                level_x += cos
                level_y += sin
                if self.minimap and self.minimap.show_ray_cast:
                    self.minimap.set_pixel(
                        level_x,
                        level_y,
                        self.minimap.ray_cast_color
                    )

            # Calculate distance (Pythagoras)
            distance = calc.pythagoras(
                level_x,
                level_y,
                self.player.x,
                self.player.y
            ) * self.tile_size

            # Fisheye fix
            distance = abs(math.cos(rad - player_rad) * distance)

            # Calculate wall height
            wall_height = self._calculate_wall_height(distance)

            # Render wall
            if tile.texture is not None:
                self._draw_textured_wall(
                    x, wall_height, tile, level_x, level_y
                )
            else:
                self._draw_wall(x, wall_height, tile)

            # Render ceil
            if self.level.cast_ceil_map:
                self._draw_textured_ceil(x, wall_height)
            else:
                self._draw_ceil(x, wall_height)

            # Render floor
            if self.level.cast_floor_map or self.level.cast_ceil_map:
                self._draw_textured_floor_ceil(x, wall_height, rad)
            else:
                self._draw_floor(x, wall_height)

            current_angle += inc_angle
            current_angle %= 360
        # exit()

    def set_precision(self, precision):
        self.precision = precision

    def get_pixels(self):
        return self.pixels

    def set_minimap(self, minimap):
        self.minimap = minimap

    ###########################################################################
    # Private Methods
    ###########################################################################

    def _calculate_distance_projection_plane(self, half_width):
        return half_width / math.tan(calc.dg_to_rad(Player.DEFAULT_FOV) / 2)

    def _calculate_wall_height(self, distance):
        wall_height = \
            self.tile_size / distance * self.projection_plane_distance

        wall_height = math.floor(wall_height)
        return wall_height

    def _validate_player_coords(self, player):
        if player.x < 1 or player.x >= self.width - 1:
            raise RayCastingError(f'Invalid player X position: {player.x}')
        if player.y < 1 or player.y >= self.height - 1:
            raise RayCastingError(f'Invalid player Y position: {player.y}')
        return player

    def _set_pixel(self, x, y, pixel):
        self.pixels[x, y] = pixel

    def _draw_ceil(self, x, wall_height):
        end = self.half_height - wall_height // 2
        for y in range(end):
            self._set_pixel(x, y, self.level.ceil_color)

    def _draw_wall(self, x, wall_height, tile):
        start = self.half_height - wall_height // 2
        end = self.half_height + wall_height // 2
        for y in range(start, end):
            self._set_pixel(x, y, tile.color)

    def _draw_textured_wall(self, x, wall_height, tile, level_x, level_y):
        tex_width, tex_height = tile.texture.width, tile.texture.height
        tex_x = (self.tile_size * (level_x + level_y)) % tex_width
        inc_y = tex_height / wall_height

        start = self.half_height
        end = self.half_height - wall_height // 2
        if end < 0:
            end = -1
        tex_y = tex_height / 2

        for y in range(start, end, -1):
            pixel = tile.texture.pixels[
                math.floor(tex_x), math.floor(tex_y)
            ]
            self._set_pixel(x, y, pixel)
            tex_y -= inc_y
            tex_y %= tex_height

        start = self.half_height
        end = self.half_height + wall_height // 2
        if end >= self.height:
            end = self.height
        tex_y = tex_height / 2

        for y in range(start, end):
            pixel = tile.texture.pixels[
                math.floor(tex_x), math.floor(tex_y)
            ]
            self._set_pixel(x, y, pixel)
            tex_y += inc_y
            tex_y %= tex_height

    def _draw_floor(self, x, wall_height):
        start = self.half_height + wall_height // 2
        end = self.height
        for y in range(start, end):
            self._set_pixel(x, y, self.level.floor_color)

    def _draw_textured_ceil(self, x, wall_height):
        pass

    def _draw_textured_floor_ceil(self, x, wall_height, ray_rad):
        pr = calc.dg_to_rad(self.player.angle)
        cos = math.cos(ray_rad)
        sin = math.sin(ray_rad)
        start = math.floor(self.half_height + wall_height / 2)
        end = self.height

        for y in range(start, end):
            dist = (self.height / (2 * y - self.height))
            dist = dist / math.cos(pr - ray_rad)
            pos_x = dist * cos
            pos_y = dist * sin
            pos_x += self.player.x
            pos_y += self.player.y

            if self.minimap and self.minimap.show_floor_cast:
                self.minimap.set_pixel(
                    pos_x,
                    pos_y,
                    self.minimap.floor_cast_color
                )

            if self.level.cast_floor_map:
                floor_tile_id = self.level.get_floor_map_tile_by_coords(
                    math.floor(pos_x),
                    math.floor(pos_y)
                )
                floor_tile = self.level.get_tile_by_id(floor_tile_id)
                tx = math.floor(pos_x * floor_tile.texture.width)
                ty = math.floor(pos_y * floor_tile.texture.height)
                tex_width = floor_tile.texture.width
                tex_height = floor_tile.texture.height
                pixels = floor_tile.texture.pixels
                pixel = pixels[tx % tex_width, ty % tex_height]
                self._set_pixel(x, y, pixel)

            if self.level.cast_ceil_map:
                ceil_tile_id = self.level.get_ceil_map_tile_by_coords(
                    math.floor(pos_x),
                    math.floor(pos_y)
                )
                ceil_tile = self.level.get_tile_by_id(ceil_tile_id)
                tx = math.floor(pos_x * ceil_tile.texture.width)
                ty = math.floor(pos_y * ceil_tile.texture.height)
                tex_width = ceil_tile.texture.width
                tex_height = ceil_tile.texture.height
                pixels = ceil_tile.texture.pixels
                pixel = pixels[tx % tex_width, ty % tex_height]
                mirrored = self.height - y - 1
                self._set_pixel(x, mirrored, pixel)

    def _draw_minimap(self):
        minimap = self.minimap.minimap
        offeset_x = self.minimap.x
        offeset_y = self.minimap.y
        for y in range(len(minimap)):
            for x in range(len(minimap[y])):
                pixel = minimap[y][x]
                self._set_pixel(x + offeset_x, y + offeset_y, pixel)
