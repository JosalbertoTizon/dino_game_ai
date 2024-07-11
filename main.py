import pygame
import sys
from constants import *

pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump and Fall")

# Clock for managing frame rate
clock = pygame.time.Clock()

# Player settings
player_pos = pygame.Vector2(100, FLOOR_HEIGHT)
player_velocity = pygame.Vector2(0, 0)
on_ground = True

# Load player textures
run_textures = [
    pygame.image.load('Images/DinoRun1.png').convert_alpha(),
    pygame.image.load('Images/DinoRun2.png').convert_alpha()
]
jump_texture = pygame.image.load('Images/DinoJump.png').convert_alpha()

# Scale textures to 60x60 pixels
run_textures = [pygame.transform.scale(tex, (60, 60)) for tex in run_textures]
jump_texture = pygame.transform.scale(jump_texture, (60, 60))

# Player sprite state
current_run_texture = 0
run_animation_timer = 0

# Player rect
player_rect = run_textures[current_run_texture].get_rect(topleft=player_pos)

# Load track texture and rect
track_texture = pygame.image.load('Images/Track.png').convert_alpha()
track_rect = track_texture.get_rect(topleft=(0, 500))  # Position the track at the bottom
track_x = 0  # Initial x position of the track

# Main game loop
while True:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and on_ground:
        player_velocity.y = -JUMP_STRENGTH
        on_ground = False

    # Apply gravity
    if not on_ground:
        player_velocity.y += GRAVITY * dt

    # Update player position
    player_pos.y += player_velocity.y * dt
    player_rect.topleft = player_pos

    # Check for landing on the ground (simple ground check at y=floor_height)
    if player_pos.y >= FLOOR_HEIGHT:
        player_pos.y = FLOOR_HEIGHT
        player_velocity.y = 0
        on_ground = True

    # Update run animation timer and switch textures
    if on_ground:
        run_animation_timer += dt
        if run_animation_timer >= RUN_ANIMATION_SPEED:
            current_run_texture = (current_run_texture + 1) % len(run_textures)
            run_animation_timer = 0

    # Move the track texture horizontally
    track_x -= MOVEMENT_SPEED * dt  # Adjust the speed as needed
    if track_x <= -track_rect.width:
        track_x = 0

    # Drawing
    screen.fill((247, 247, 247))  # Clear screen with light gray (Google Dino background color)

    # Draw the track with horizontal scrolling
    screen.blit(track_texture, (track_x, track_rect.y))
    screen.blit(track_texture, (track_x + track_rect.width, track_rect.y))

    # Draw player with appropriate texture
    if on_ground:
        screen.blit(run_textures[current_run_texture], player_rect.topleft)
    else:
        screen.blit(jump_texture, player_rect.topleft)

    pygame.display.flip()
