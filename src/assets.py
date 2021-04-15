"""
Texture
"""
import pygame


###############################################################################
# Exceptions
###############################################################################


class AssetsError(Exception):
    pass


###############################################################################
# Classes
###############################################################################


class Assets:

    assets = {}

    @classmethod
    def load(cls, name, path, alpha=True):
        image = pygame.image.load(path)
        size = image.get_size()
        if alpha:
            image = image.convert_alpha()
        pixels = pygame.PixelArray(image)
        cls.assets[name] = Asset(size[0], size[1], pixels)

    @classmethod
    def get(cls, name):
        if name not in cls.assets:
            raise AssetsError(f'Asset "{name}" not found')
        return cls.assets[name]


class Asset:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels
