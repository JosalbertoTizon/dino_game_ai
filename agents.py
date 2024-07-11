import random
import pygame
from constants import *


class Obstacle:
    def __init__(self, image, type, game_speed, obstacles):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.game_speed = game_speed
        self.obstacles = obstacles

    def update(self, dt):
        self.rect.x -= self.game_speed * dt
        if self.rect.x < -self.rect.width:
            self.obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, game_speed, obstacles):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, game_speed, obstacles)
        self.rect.y = FLOOR_HEIGHT - 10


class LargeCactus(Obstacle):
    def __init__(self, image, game_speed, obstacles):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, game_speed, obstacles)
        self.rect.y = FLOOR_HEIGHT - 30


class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image, game_speed, obstacles):
        self.type = 0
        super().__init__(image, self.type, game_speed, obstacles)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1