"""
Game
"""
import pygame
from raycasting import RayCasting
from keyboard import Keyboard


###############################################################################
# Exceptions
###############################################################################


class GameError(Exception):
    pass


###############################################################################
# Classes
###############################################################################


class Game:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        self.level = None
        self.raycasting = None
        self.running = False
        self.surface = None
        self.projection = None
        self.keyboard = Keyboard()

    def set_level(self, level):
        if not level.player:
            msg = 'You must define the player on the level to start the game'
            raise GameError(msg)
        self.level = level

    def init(self):
        pygame.init()
        pygame.display.set_caption('RayCasting')
        dimension = (self.width * self.scale, self.height * self.scale)
        self.surface = pygame.display.set_mode(dimension)
        self.projection = pygame.surface.Surface((self.width, self.height))

    def start(self):
        self.raycasting = RayCasting(
            self.width,
            self.height,
            self.level.tile_size,
            self.level,
            self.level.player,
            pygame.PixelArray(self.projection)
        )
        self.running = True
        self._game_loop()

    def _game_loop(self):
        while self.running:
            self._process_keyboard_events()
            self._process_events()
            self.raycasting.process()
            projection_scaled = pygame.transform.scale(
                self.projection,
                (self.width * self.scale, self.height * self.scale)
            )
            self.surface.blit(projection_scaled, (0, 0))
            pygame.display.flip()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.keyboard.w = True
                elif event.key == pygame.K_s:
                    self.keyboard.s = True
                elif event.key == pygame.K_a:
                    self.keyboard.a = True
                elif event.key == pygame.K_d:
                    self.keyboard.d = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.keyboard.w = False
                elif event.key == pygame.K_s:
                    self.keyboard.s = False
                elif event.key == pygame.K_a:
                    self.keyboard.a = False
                elif event.key == pygame.K_d:
                    self.keyboard.d = False

    def _process_keyboard_events(self):
        if self.keyboard.w:
            self.level.player.move_forward()
        if self.keyboard.s:
            self.level.player.move_back()
        if self.keyboard.a:
            self.level.player.turn_left()
        if self.keyboard.d:
            self.level.player.turn_right()
