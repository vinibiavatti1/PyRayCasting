"""
Player
"""
import math
import calc


class Player:

    DEFAULT_FOV = 60

    def __init__(self, x, y, angle=0, fov=60):
        self.x = x
        self.y = y
        self.angle = angle
        self.fov = fov
        self.level = None
        self.move_speed = 0.2
        self.turn_speed = 6

    def set_level(self, level):
        self.level = level

    def move_forward(self):
        cos = math.cos(calc.dg_to_rad(self.angle))
        sin = math.sin(calc.dg_to_rad(self.angle))
        newx = self.x + (cos * self.move_speed)
        newy = self.y + (sin * self.move_speed)
        half_dist = self.level.tile_size / 2
        colx = self.x + (cos * (half_dist / self.level.tile_size))
        coly = self.y + (sin * (half_dist / self.level.tile_size))
        if not self.will_collide(colx, self.y):
            self.x = newx
        if not self.will_collide(self.x, coly):
            self.y = newy

    def move_back(self):
        cos = math.cos(calc.dg_to_rad(self.angle))
        sin = math.sin(calc.dg_to_rad(self.angle))
        newx = self.x - (cos * self.move_speed)
        newy = self.y - (sin * self.move_speed)
        half_dist = self.level.tile_size / 2
        colx = self.x - (cos * (half_dist / self.level.tile_size))
        coly = self.y - (sin * (half_dist / self.level.tile_size))
        if not self.will_collide(colx, coly):
            self.x = newx
            self.y = newy

    def turn_left(self):
        self.angle -= self.turn_speed
        self.angle %= 360

    def turn_right(self):
        self.angle += self.turn_speed
        self.angle %= 360

    def check_colision(self):
        return self.will_collide(self.x, self.y)

    def will_collide(self, x, y):
        x = math.floor(x)
        y = math.floor(y)
        tile_id = self.level.get_wall_map_tile_by_coords(x, y)
        tile = self.level.get_tile_by_id(tile_id)
        if tile and tile.solid:
            return True
        return False
