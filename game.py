import sys
from agents import *


class Game:
    def __init__(self, speed_multiplier=1, training=False):
        pygame.init()

        # Game mode
        self.training_mode = training

        # Choose if game can be played manually
        self.manual_playing = False
        # self.manual_playing = True

        # Screen settings
        self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dino Game")

        # Load textures
        [self.RUN_TEXTURE, self.JUMP_TEXTURE, self.DUCK_TEXTURE,
         self.SMALL_CACTUS, self.LARGE_CACTUS, self.BIRD, self.TRACK_TEXTURE] = self.load_textures()

        # Clock for managing frame rate
        self.clock = pygame.time.Clock()

        # Create track rect
        self.track_rect = self.TRACK_TEXTURE.get_rect(topleft=(0, 500))  # Position the track at the bottom
        self.track_x = 0  # Initial x position of the track

        # Score variable
        self.score = 0
        self.font = pygame.font.Font(None, 36)  # Font for displaying the score
        self.small_font = pygame.font.Font(None, 24)  # Font for displaying the small message

        # Hitbox display flag
        self.show_hitbox = True

        # Game movement speed variable
        self.movement_speed = INITIAL_MOVEMENT_SPEED

        # Game obstacle probability variable
        self.obstacle_prob = INITIAL_OBSTACLE_PROB

        # Obstacles array
        self.obstacles = []

        self.player = Dinosaur(self.DUCK_TEXTURE, self.RUN_TEXTURE, self.JUMP_TEXTURE)

        # Frame count
        self.frame = 0

        # Speed multiplier variable
        self.speed_multiplier = speed_multiplier

        # Game State
        self.state = self.get_state()

    def step(self, action=0):
        # Main game loop
        dt = self.clock.tick(240) * self.speed_multiplier / 1000  # Amount of seconds between each loop
        self.frame += 1
        game_over = False
        show_game_over_screen = False
        reward = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.show_hitbox = not self.show_hitbox
                elif event.key == pygame.K_x:
                    self.speed_multiplier = min(10, self.speed_multiplier + 1)  # The game's physics don't work properly
                elif event.key == pygame.K_z:  # with speeds greater than 10
                    self.speed_multiplier = max(1, self.speed_multiplier - 1)

        # Draw the clear background screen
        self.screen.fill((247, 247, 247))

        # Convert pressed keys to actions
        if self.manual_playing:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                action = 1  # Jump
            elif keys[pygame.K_DOWN]:
                action = 2  # Duck
            else:
                action = 0  # No action

        # Update and draw player
        self.player.update(action, dt, self.speed_multiplier)
        self.player.draw(self.screen)

        # Obstacle generation logic
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(SmallCactus(self.SMALL_CACTUS, self.obstacles))
            elif random.randint(0, 2) == 1:
                self.obstacles.append(LargeCactus(self.LARGE_CACTUS, self.obstacles))
            elif random.randint(0, 2) == 2:
                self.obstacles.append(Bird(self.BIRD, self.obstacles))
        elif len(self.obstacles) == 1 and self.obstacles[0].rect.x < SCREEN_WIDTH * (
                1 - 1 / MINIMUM_OBSTACLE_DISTANCE_RATIO):
            new_obstacle_prob = random.randint(0, int(100 / MAX_OBSTACLE_PROB) - 1)
            if new_obstacle_prob == 0:
                if random.randint(0, 2) == 0:
                    self.obstacles.append(SmallCactus(self.SMALL_CACTUS, self.obstacles))
                elif random.randint(0, 2) == 1:
                    self.obstacles.append(LargeCactus(self.LARGE_CACTUS, self.obstacles))
                elif random.randint(0, 2) == 2:
                    self.obstacles.append(Bird(self.BIRD, self.obstacles))

        # Move the track texture horizontally
        self.track_x -= self.movement_speed * dt  # Adjust the speed as needed
        if self.track_x <= -self.track_rect.width:
            self.track_x = 0

        scored_this_frame = False
        # Updates score, number of obstacles and increases movement speed
        if self.frame % 7 == 0:
            self.score += self.speed_multiplier
            scored_this_frame = True
            if self.score % D_SCORE_TO_INCREASE_SPEED == 0:
                if self.movement_speed <= MAX_SPEED - SPEED_INCREMENT:
                    self.movement_speed += SPEED_INCREMENT
            if self.score % D_SCORE_TO_INCREASE_PROB == 0:
                if self.obstacle_prob <= MAX_OBSTACLE_PROB:
                    self.obstacle_prob += OBSTACLE_PROB_INCREMENT

        # Draw the track with horizontal scrolling
        self.screen.blit(self.TRACK_TEXTURE, (self.track_x, self.track_rect.y))
        self.screen.blit(self.TRACK_TEXTURE, (self.track_x + self.track_rect.width, self.track_rect.y))

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.update(self.movement_speed, dt)
            obstacle.draw(self.screen)
            if self.player.rect.colliderect(obstacle.rect):
                if self.training_mode:
                    reward -= 1
                    # Ends Game
                    self.score = 0
                    self.movement_speed = INITIAL_MOVEMENT_SPEED
                    self.obstacles = []
                    return [self.get_state(), reward, self.speed_multiplier, game_over, dt]
                else:
                    game_over = True
                    final_score = self.score
                    self.score = 0
                    self.movement_speed = INITIAL_MOVEMENT_SPEED
                    self.obstacles = []
                    # Game Over Screen
                    while show_game_over_screen and game_over:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key:
                                    game_over = False
                        self.screen.fill((247, 247, 247))  # Clear screen

                    # Fonts
                    game_over_font = pygame.font.Font(None, 72)
                    score_font = pygame.font.Font(None, 36)

                    # Game Over Message
                    game_over_text = game_over_font.render("G A M E   O V E R", True, (0, 0, 0))
                    game_over_text_rect = game_over_text.get_rect(
                        center=(self.screen_width // 2, self.screen_height // 2 - 50))
                    self.screen.blit(game_over_text, game_over_text_rect)

                    # Final Score Message
                    score_text = score_font.render(f"Score: {final_score}", True, (0, 0, 0))
                    score_text_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                    self.screen.blit(score_text, score_text_rect)

                    pygame.display.update()
                    return [self.get_state(), reward, self.speed_multiplier, game_over, dt]

        # Draw hitbox
        if self.show_hitbox:
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 2)
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, (0, 255, 0), obstacle.rect, 3)

        # Display the message at the top of the window
        message = "Press H to turn ON/OFF hitbox"
        message_text = self.small_font.render(message, True, (255, 0, 0))  # Red color
        self.screen.blit(message_text, (10, 10))

        # Display the score on the screen
        score_text = self.font.render(f"Score: {int(self.score)}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 50))

        # Display the speed multiplier on the screen
        speed_text = self.font.render(f"Simulation Speed (Press Z/X): {self.speed_multiplier}x", True, (0, 0, 0))
        self.screen.blit(speed_text, (10, 90))
        pygame.display.flip()

        return [self.get_state(), reward, self.speed_multiplier, game_over, dt]

    def get_state(self):

        # Player state
        player_speed = self.movement_speed
        player_y = self.player.rect.y

        # Identify next obstacle
        if self.obstacles:
            next_obstacle = self.obstacles[0]
            # If dino gets past first obstacle, then move to the next one
            if len(self.obstacles) > 1 and self.obstacles[0].rect.x < 300:
                next_obstacle = self.obstacles[1]
            # Get obstacle position
            obstacle_y = next_obstacle.rect.y
            distance_to_next = next_obstacle.rect.x - self.player.rect.x
            obstacle_height = next_obstacle.rect.height
            obstacle_width = next_obstacle.rect.width
        else:
            obstacle_y, distance_to_next, obstacle_height, obstacle_width = 0, 1200, 0, 0

        # Return current state
        return [
            player_speed,
            player_y,
            distance_to_next,
            obstacle_height,
            obstacle_width,
            obstacle_y,
            int(self.player.is_jumping),
            int(self.player.is_running),
            int(self.player.is_ducking),
            int(self.player.is_air_ducking),
        ]

    def load_textures(self):
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

        TRACK_TEXTURE = pygame.image.load('Images/Track.png').convert_alpha()

        return [RUN_TEXTURE, JUMP_TEXTURE, DUCK_TEXTURE, SMALL_CACTUS, LARGE_CACTUS, BIRD, TRACK_TEXTURE]
