import random
import pygame
from constants import *


class Dinosaur:

    X_POS = 300
    Y_POS = FLOOR_HEIGHT
    Y_POS_DUCK = FLOOR_HEIGHT + 30
    JUMP_VEL = 8.5

    def __init__(self, duck_img, run_img, jump_img):
        self.duck_img = duck_img
        self.run_img = run_img
        self.jump_img = jump_img

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def get_rect(self):
        return self.dino_rect

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


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
            self.obstacles.pop()

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
    BIRD_HEIGHTS = [360, 410, 430]

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