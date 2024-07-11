import random
import pygame
import sys
from constants import *
from agents import *

pygame.init()

# Screen settings
screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump and Fall")

# Clock for managing frame rate
clock = pygame.time.Clock()

# Player settings
player_pos = pygame.Vector2(100, FLOOR_HEIGHT)
player_velocity = pygame.Vector2(0, 0)
on_ground = True
is_ducking = False

# Load player textures
run_textures = [
    pygame.image.load('Images/DinoRun1.png').convert_alpha(),
    pygame.image.load('Images/DinoRun2.png').convert_alpha()
]
jump_texture = pygame.image.load('Images/DinoJump.png').convert_alpha()
duck_textures = [
    pygame.image.load('Images/DinoDuck1.png').convert_alpha(),
    pygame.image.load('Images/DinoDuck2.png').convert_alpha()
]
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

# Scale textures to 60x60 pixels (except duck textures)
run_textures = [pygame.transform.scale(tex, (60, 60)) for tex in run_textures]
jump_texture = pygame.transform.scale(jump_texture, (60, 60))

# Scale duck textures maintaining their aspect ratio
duck_textures = [pygame.transform.scale(duck_tex, (80, 40)) for duck_tex in duck_textures]

# Player sprite state
current_run_texture = 0
run_animation_timer = 0
current_duck_texture = 0
duck_animation_timer = 0

# Player rect
player_rect = run_textures[current_run_texture].get_rect(topleft=player_pos)
player_rect.width = 0.6 * player_rect.width
player_rect.height = 0.6 * player_rect.height

# Load track texture and rect
track_texture = pygame.image.load('Images/Track.png').convert_alpha()
track_rect = track_texture.get_rect(topleft=(0, 500))  # Position the track at the bottom
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
    if keys[pygame.K_w] and on_ground:
        player_velocity.y = -JUMP_STRENGTH
        on_ground = False
    if keys[pygame.K_s]:
        is_ducking = True
    else:
        is_ducking = False

    if len(obstacles) == 0:
        if random.randint(0, 2) == 0:
            obstacles.append(SmallCactus(SMALL_CACTUS, obstacles))
        elif random.randint(0, 2) == 1:
            obstacles.append(LargeCactus(LARGE_CACTUS, obstacles))
        elif random.randint(0, 2) == 2:
            obstacles.append(Bird(BIRD, obstacles))

    # Apply gravity
    if not on_ground:
        gravity = GRAVITY * 3.0 if is_ducking else GRAVITY
        player_velocity.y += gravity * dt

    # Update player position
    player_pos.y += player_velocity.y * dt
    player_rect.topleft = player_pos

    # Check for landing on the ground (simple ground check at y=floor_height)
    if player_pos.y >= FLOOR_HEIGHT:
        player_pos.y = FLOOR_HEIGHT
        player_velocity.y = 0
        on_ground = True

    # Update run animation timer and switch textures
    if on_ground and not is_ducking:
        run_animation_timer += dt
        if run_animation_timer >= RUN_ANIMATION_SPEED:
            current_run_texture = (current_run_texture + 1) % len(run_textures)
            run_animation_timer = 0

    # Update duck animation timer and switch textures
    if on_ground and is_ducking:
        duck_animation_timer += dt
        if duck_animation_timer >= RUN_ANIMATION_SPEED:
            current_duck_texture = (current_duck_texture + 1) % len(duck_textures)
            duck_animation_timer = 0

    # Move the track texture horizontally
    track_x -= movement_speed * dt  # Adjust the speed as needed
    if track_x <= -track_rect.width:
        track_x = 0

    # Updates score and increases movement speed
    if frame % 8 == 0:
        score += 1
        if score % 100 == 0 and movement_speed <= MAX_SPEED - SPEED_INCREMENT:
            movement_speed += SPEED_INCREMENT

    # Drawing
    screen.fill((247, 247, 247))  # Clear screen with light gray (Google Dino background color)

    # Draw objects
    for obstacle in obstacles:
        obstacle.draw(screen)
        obstacle.update(movement_speed, dt)
        if player_rect.colliderect(obstacle.rect):
            pygame.time.delay(2000)
            #death_count += 1

    # Draw the track with horizontal scrolling
    screen.blit(track_texture, (track_x, track_rect.y))
    screen.blit(track_texture, (track_x + track_rect.width, track_rect.y))

    # Draw player with appropriate texture
    if on_ground:
        if is_ducking:
            screen.blit(duck_textures[current_duck_texture], player_rect.topleft)
            player_pos = pygame.Vector2(100, FLOOR_HEIGHT + 20)  # Decrease height when ducked
        else:
            screen.blit(run_textures[current_run_texture], player_rect.topleft)
            player_pos = pygame.Vector2(100, FLOOR_HEIGHT)  # Correct height when stop ducking
    else:
        if is_ducking:
            screen.blit(duck_textures[current_duck_texture], player_rect.topleft)
        else:
            screen.blit(jump_texture, player_rect.topleft)

    # Draw the hitbox if enabled
    if show_hitbox:
        pygame.draw.rect(screen, (255, 0, 0), player_rect, 3)
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

