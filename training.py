from game import Game

speed_multiplier = 1

# Choose game mode
training = False
# training = False
while True:
    game = Game(speed_multiplier, training)
    game_over = False
    while not game_over:
        if training:
            [next_state, reward, speed_multiplier, game_over] = game.step()
        else:
            game.step()
