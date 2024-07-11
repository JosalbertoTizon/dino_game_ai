import random
import pygame
import sys
from constants import *
from agents import *

pygame.init()

# Screen settings
screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo do Zé Betão")

# Clock for managing frame rate
clock = pygame.time.Clock()


RUN_TEXTURE = [
    pygame.image.load('Images/DinoRun1.png').convert_alpha(),
    pygame.image.load('Images/DinoRun2.png').convert_alpha()
]
RUN_TEXTURE = [pygame.transform.scale(tex, (60, 60)) for tex in RUN_TEXTURE]

JUMP_TEXTURE = pygame.image.load('Images/DinoJump.png').convert_alpha()
JUMP_TEXTURE = pygame.transform.scale(JUMP_TEXTURE, (60, 60))

DUCK_TEXTURE = [
    pygame.image.load('Images/DinoDuck1.png').convert_alpha(),
    pygame.image.load('Images/DinoDuck2.png').convert_alpha()
]
DUCK_TEXTURE = [pygame.transform.scale(duck_tex, (80, 40)) for duck_tex in DUCK_TEXTURE]

SMALL_CACTUS = [
    pygame.image.load("Images/SmallCactus1.png").convert_alpha(),
    pygame.image.load("Images/SmallCactus2.png").convert_alpha(),
    pygame.image.load("Images/SmallCactus3.png").convert_alpha(),
]
LARGE_CACTUS = [
    pygame.image.load("Images/LargeCactus1.png").convert_alpha(),
    pygame.image.load("Images/LargeCactus2.png").convert_alpha(),
    pygame.image.load("Images/LargeCactus3.png").convert_alpha(),
]

BIRD = [
    pygame.image.load("Images/Bird1.png").convert_alpha(),
    pygame.image.load("Images/Bird2.png").convert_alpha(),
]

# Load track texture and rect
TRACK_TEXTURE = pygame.image.load('Images/Track.png').convert_alpha()
track_rect = TRACK_TEXTURE.get_rect(topleft=(0, 500))  # Position the track at the bottom
track_x = 0  # Initial x position of the track

# Score variable
score = 0
font = pygame.font.Font(None, 36)  # Font for displaying the score
small_font = pygame.font.Font(None, 24)  # Font for displaying the small message

# Hitbox display flag
show_hitbox = True

# Game movement speed variable
movement_speed = 500

# Obstacles array
obstacles = []

player = Dinosaur(DUCK_TEXTURE, RUN_TEXTURE, JUMP_TEXTURE)

# Frame count
frame = 0

# Main game loop
while True:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_hitbox = not show_hitbox

    keys = pygame.key.get_pressed()
    player.update(keys)

    if len(obstacles) == 0:
        if random.randint(0, 2) == 0:
            obstacles.append(SmallCactus(SMALL_CACTUS, obstacles))
        elif random.randint(0, 2) == 1:
            obstacles.append(LargeCactus(LARGE_CACTUS, obstacles))
        elif random.randint(0, 2) == 2:
            obstacles.append(Bird(BIRD, obstacles))

    # Move the track texture horizontally
    track_x -= movement_speed * dt  # Adjust the speed as needed
    if track_x <= -track_rect.width:
        track_x = 0

    # Updates score and increases movement speed
    if frame % 8 == 0:
        score += 1
        if score % 100 == 0 and movement_speed <= MAX_SPEED - SPEED_INCREMENT:
            movement_speed += SPEED_INCREMENT

    # Draw the clear background screen
    screen.fill((247, 247, 247))

    # Draw the track with horizontal scrolling
    screen.blit(TRACK_TEXTURE, (track_x, track_rect.y))
    screen.blit(TRACK_TEXTURE, (track_x + track_rect.width, track_rect.y))

    # Draw player
    player.draw(screen)

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)
        obstacle.update(movement_speed, dt)
        if player.get_rect().colliderect(obstacle.rect):
            pygame.time.delay(2000)
            score = 0

    # Draw hitbox
    if show_hitbox:
        pygame.draw.rect(screen, (255, 0, 0), player.get_rect(), 2)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 255, 0), obstacle.rect, 3)

    # Display the message at the top of the window
    message = "Press H to turn ON/OFF hitbox"
    message_text = small_font.render(message, True, (255, 0, 0))  # Red color
    screen.blit(message_text, (10, 10))

    # Display the score on the screen
    score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()

