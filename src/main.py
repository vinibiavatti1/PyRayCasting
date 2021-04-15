"""
Main
"""
from player import Player
from level import Level
from game import Game
from tile import Tile, WallTile, FloorTile, CeilTile
from assets import Assets
from minimap import Minimap
import os
import sys

# Constants
CURRENT_PATH = sys.path[0]
ASSETS_DIR = os.path.join(CURRENT_PATH, '../assets')

# Game Data
game = Game(160, 120, 4)
game.init()

# Assets
Assets.load('wall', os.path.join(ASSETS_DIR, 'wall.png'))
Assets.load('floor', os.path.join(ASSETS_DIR, 'floor.png'))
Assets.load('ceil', os.path.join(ASSETS_DIR, 'ceil.png'))

# Minimap
minimap = Minimap(4, 5, 5)
minimap.show(ray_cast=True)

# Player
player = Player(5, 5, fov=60)

# Level
level = Level(10, 10, 32, player)
wall = WallTile(1, 'wall', texture=Assets.get('wall'))
floor = FloorTile(2, 'floor', texture=Assets.get('floor'))
ceil = CeilTile(3, 'ceil', texture=Assets.get('ceil'))
level.register_tile(wall)
level.register_tile(floor)
level.register_tile(ceil)
level.set_default_wall_tile_id(1)
level.set_default_floor_tile_id(2)
level.set_default_ceil_tile_id(3)
level.cast_floor(True)
level.cast_ceil(False)
level.generate_maps()
level.set_tile_on_wall_map(1, 3, 3)
level.set_minimap(minimap)

# Start
game.set_level(level)
game.start()
