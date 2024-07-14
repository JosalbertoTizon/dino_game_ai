import os
import numpy as np
import matplotlib.pyplot as plt
from dqn_agent import DQNAgent
from game import Game

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress informational messages and warnings

# Hyperparameters
EPISODE_TIME = 10  # Episode duration in seconds
NUM_EPISODES = 10  # Number of episodes used for training
batch_size = 32  # Batch size used for experience replay


# Comment this line to enable training using your GPU
#  os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Initialize the game environment
speed_multiplier = 1

# Create the DQN agent
state_size = 10  # Your game state size
action_size = 3  # Number of actions: 0 (No action), 1 (Jump), 2 (Duck)
agent = DQNAgent(state_size, action_size)

return_history = []

# Training loop
for episode in range(1, NUM_EPISODES + 1):
    # Reset the environment
    game = Game(speed_multiplier, True)
    state = game.get_state()
    state = np.reshape(state, [1, state_size])
    cumulative_reward = 0.0
    elapsed_time = 0

    while elapsed_time < EPISODE_TIME:

        # Select action
        action = agent.act(state)
        # Take action, observe reward and new state
        next_state, reward, speed_multiplier, game_over, dt = game.step(action)
        elapsed_time += dt
        done = game_over

        # Reshape to keep compatibility with Keras
        next_state = np.reshape(next_state, [1, state_size])

        # Simple reward shaping: positive reward for surviving, negative for game over
        if done:
            reward -= 200

        # Append experience to replay buffer
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        # Accumulate reward
        cumulative_reward += reward

    # Update policy if enough experience
    if len(agent.memory) > 4 * batch_size:
        loss = agent.replay(batch_size)
        agent.clear_memory()

    return_history.append(cumulative_reward)
    agent.update_epsilon()

    print(f"Episode: {episode}/{NUM_EPISODES}, Score: {cumulative_reward}, Epsilon: {agent.epsilon}")

    # Plot and save model every 20 episodes
    # if episode % 20 == 0:
    #     plt.plot(return_history, 'b')
    #     plt.xlabel('Episode')
    #     plt.ylabel('Return')
    #     plt.show(block=False)
    #     plt.pause(0.1)
    #     plt.savefig('dqn_training.png')

plt.pause(1.0)

# Start playing indefinitely after trained
while True:
    game = Game(speed_multiplier, False)
    state = game.get_state()
    state = np.reshape(state, [1, state_size])
    game_over = False

    while not game_over:
        action = agent.act(state)
        next_state, _, speed_multiplier, game_over, _ = game.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        state = next_state

    print("Game over! Restarting...")

