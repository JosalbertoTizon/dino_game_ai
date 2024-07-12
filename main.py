import random
import sys
from constants import *
from agents import *

pygame.init()

# Screen settings
screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game")

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
movement_speed = INITIAL_MOVEMENT_SPEED

# Obstacles array
obstacles = []

player = Dinosaur(DUCK_TEXTURE, RUN_TEXTURE, JUMP_TEXTURE)

# Frame count
frame = 0

# Speed multiplier variable
speed_multiplier = 1

# Main game loop
while True:
    dt = clock.tick(60) * speed_multiplier / 1000  # Amount of seconds between each loop
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_hitbox = not show_hitbox
            elif event.key == pygame.K_x:
                speed_multiplier = min(10, speed_multiplier + 1)
            elif event.key == pygame.K_z:
                speed_multiplier = max(1, speed_multiplier - 1)

    # Draw the clear background screen
    screen.fill((247, 247, 247))

    # Update and draw player
    keys = pygame.key.get_pressed()
    player.update(keys, dt)
    player.draw(screen)

    # Obstacle generation logic
    if len(obstacles) == 0:
        if random.randint(0, 2) == 0:
            obstacles.append(SmallCactus(SMALL_CACTUS, obstacles))
        elif random.randint(0, 2) == 1:
            obstacles.append(LargeCactus(LARGE_CACTUS, obstacles))
        elif random.randint(0, 2) == 2:
            obstacles.append(Bird(BIRD, obstacles))
    elif len(obstacles) == 1 and obstacles[0].rect.x < SCREEN_WIDTH / 2:
        new_obstacle_prob = random.randint(0, 24)  # 5% probability per frame
        if(new_obstacle_prob == 0):
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
    if frame * speed_multiplier % 7 == 0:
        score += 1
        if score % 100 == 0 and movement_speed <= MAX_SPEED - SPEED_INCREMENT:
            movement_speed += SPEED_INCREMENT

    # Draw the track with horizontal scrolling
    screen.blit(TRACK_TEXTURE, (track_x, track_rect.y))
    screen.blit(TRACK_TEXTURE, (track_x + track_rect.width, track_rect.y))

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)
        obstacle.update(movement_speed, dt)
        if player.rect.colliderect(obstacle.rect):
            game_over = True
            final_score = score
            score = 0
            movement_speed = INITIAL_MOVEMENT_SPEED
            obstacles = []
            # Game Over Screen
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key:
                            game_over = False
                screen.fill((247, 247, 247))  # Clear screen
                # Fonts
                game_over_font = pygame.font.Font(None, 72)
                score_font = pygame.font.Font(None, 36)

                # Game Over Message
                game_over_text = game_over_font.render("G A M E   O V E R", True, (0, 0, 0))
                game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
                screen.blit(game_over_text, game_over_text_rect)

                # Final Score Message
                score_text = score_font.render(f"Score: {final_score}", True, (0, 0, 0))
                score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(score_text, score_text_rect)

                pygame.display.update()

    # Draw hitbox
    if show_hitbox:
        pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 255, 0), obstacle.rect, 3)

    # Display the message at the top of the window
    message = "Press H to turn ON/OFF hitbox"
    message_text = small_font.render(message, True, (255, 0, 0))  # Red color
    screen.blit(message_text, (10, 10))

    # Display the score on the screen
    score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_text, (10, 50))

    # Display the speed multiplier on the screen
    speed_text = font.render(f"Simulation Speed: {speed_multiplier}x", True, (0, 0, 0))
    screen.blit(speed_text, (10, 90))
    pygame.display.flip()
