import math

height = 600


print(math.floor(-1.607))
exit()
for y in range(301, 600):
    dist = height / (2 * y - height)
    dist2 = y - height / 2
    print(dist, dist2)
