import random
import pygame
from constants import *


class Obstacle:
    def __init__(self, image, type, obstacles):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.obstacles = obstacles

    def update(self, game_speed, dt):
        self.rect.x -= game_speed * dt
        if self.rect.x < -self.rect.width:
            self.obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, obstacles):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, obstacles)
        self.rect.y = FLOOR_HEIGHT - 10


class LargeCactus(Obstacle):
    def __init__(self, image, obstacles):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, obstacles)
        self.rect.y = FLOOR_HEIGHT - 30


class Bird(Obstacle):
    BIRD_HEIGHTS = [360, 405, 430]

    def __init__(self, image, obstacles):
        self.type = 0
        super().__init__(image, self.type, obstacles)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1