from game import Game

game = Game(training=False)
while True:
    reward = game.loop()
