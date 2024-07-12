import random
import pygame
from constants import *


class Dinosaur:

    X_POS = 300
    Y_POS = FLOOR_HEIGHT
    Y_POS_DUCK = FLOOR_HEIGHT + 30

    def __init__(self, duck_img, run_img, jump_img):
        self.duck_img = duck_img
        self.run_img = run_img
        self.jump_img = jump_img

        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False
        self.is_air_ducking = False

        self.step_index = 0
        self.jump_vel = JUMP_STRENGTH
        self.image = self.run_img[0]
        self.rect = self.image.get_rect()
        self.rect.width = 0.7 * self.rect.width
        self.rect.height = 0.7 * self.rect.height
        self.rect.x = self.X_POS + 100
        self.rect.y = self.Y_POS

    def update(self, userInput, dt):
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump(dt)
        if self.is_air_ducking:
            self.air_duck(dt)

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.is_air_ducking and not self.is_ducking:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
            self.is_air_ducking = False
        elif userInput[pygame.K_DOWN] and not self.is_jumping and not self.is_air_ducking:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
            self.is_air_ducking = False
        elif not (self.is_jumping or self.is_air_ducking or userInput[pygame.K_DOWN]):
            self.is_ducking = False
            self.is_running = True
            self.is_jumping = False
            self.is_air_ducking = False
        elif userInput[pygame.K_DOWN] and self.is_jumping:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = False
            self.is_air_ducking = True

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.rect.width = 0.7 * self.rect.width
        self.rect.height = 0.7 * self.rect.height
        self.step_index += 1

    def jump(self, dt):
        self.image = self.jump_img
        self.rect.y -= self.jump_vel * dt
        self.jump_vel -= GRAVITY * dt
        if self.rect.y >= FLOOR_HEIGHT:
            self.is_jumping = False
            self.jump_vel = JUMP_STRENGTH
            self.rect.y = FLOOR_HEIGHT

    def air_duck(self, dt):
        self.image = self.duck_img[self.step_index // 5]
        self.rect.y -= self.jump_vel * dt
        self.jump_vel -= 3.0 * GRAVITY * dt
        if self.rect.y > FLOOR_HEIGHT:
            self.is_air_ducking = False
            self.jump_vel = JUMP_STRENGTH
            self.rect.y = FLOOR_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


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

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


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
    BIRD_HEIGHTS = [360, 395, 430]

    def __init__(self, image, obstacles):
        self.type = 0
        super().__init__(image, self.type, obstacles)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def update(self, game_speed, dt):
        self.rect.x -= (game_speed + BIRD_RELATIVE_SPEED) * dt
        if self.rect.x < -self.rect.width:
            self.obstacles.pop(0)

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1