"""
Entity
"""
import pygame


class Tile:
    def __init__(self, id, name, solid, is_wall, color=None, texture=None):
        self.id = id
        self.name = name
        self.solid = solid
        self.is_wall = is_wall
        self.color = color
        self.texture = texture


class WallTile(Tile):
    def __init__(self, id, name, color=None, texture=None):
        super().__init__(id, name, True, True, color, texture)


class FloorTile(Tile):
    def __init__(self, id, name, color=None, texture=None):
        super().__init__(id, name, False, False, color, texture)


class CeilTile(FloorTile):
    def __init__(self, id, name, color=None, texture=None):
        super().__init__(id, name, color, texture)


class EmptyTile(FloorTile):
    def __init__(self, id, name):
        super().__init__(id, name)
