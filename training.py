from game import Game

speed_multiplier = 1

# Choose game mode
training = True
# training = False
while True:
    game = Game(speed_multiplier, training)
    [reward, speed_multiplier] = game.loop()
