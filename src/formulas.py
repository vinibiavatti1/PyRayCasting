"""
Formulas (Math)

* This file contains the formulas used in the RayCasting rendering
* most of the time trigonometric formulas are used
"""

# Distance between camera and projection plane
# * It can be discovered by the tangent formula
# * tan(angle) = cat_op / cat_adj
# * cat_adj * tan(angle) = cat_op
# * cat_adj * tan(angle) / tan(angle) = cat_op / tan(angle) (add divisor)
# * cat_adj = cat_op / tan(angle) (Remove redundant)
"""
projection_distance = half_width / tan(fov / 2)
"""

# Fisheye fix
# * The cos formula can be used to discover the cat adj by angle and hipotenuse
# * cos(angle) = cat_adj / hyp
# * cos(angle) * hyp = cat_adj / hyp * hyp  (add multiply)
# * cos(angle) * hyp = cat_adj (Remove redundant)
# * cat_adj = cos(angle) * hyp
# * NOTE: Remove the player angle to use the correct angle to this formula
"""
distance = cos(ray_angle - player_angle) * distance
"""

# Wall distance (Pythagoras)
# * hyp ** 2 = cat_op ** 2 + cat_adj ** 2
"""
wall_distance = math.sqrt(cat_op ** 2 + cat_adj ** 2)
"""

# Get position of the first x,y intersection on grid
# * This formula will give the first intersection point to be used in the
#   raycasting
"""
x = math.floor(player_x / tile_size) * tile_size - 1
y = math.floor(player_y / tile_size) * tile_size + tile_size
"""
