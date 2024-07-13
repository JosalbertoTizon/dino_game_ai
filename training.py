import os
import numpy as np
import matplotlib.pyplot as plt
from dqn_agent import DQNAgent
from game import Game

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress informational messages and warnings

# Hyperparameters
NUM_EPISODES = 300  # Number of episodes used for training
batch_size = 32  # Batch size used for experience replay

# Comment this line to enable training using your GPU
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Initialize the game environment
speed_multiplier = 1
training = True

# Create the DQN agent
state_size = 10  # Your game state size
action_size = 3  # Number of actions: 0 (No action), 1 (Jump), 2 (Duck)
agent = DQNAgent(state_size, action_size)

return_history = []

for episode in range(1, NUM_EPISODES + 1):
    # Reset the environment
    game = Game(speed_multiplier, training)
    state = game.get_state()
    state = np.reshape(state, [1, state_size])
    cumulative_reward = 0.0
    done = False

    while not done:
        # Select action
        action = agent.act(state)
        # Take action, observe reward and new state
        next_state, speed_multiplier, game_over = game.step(action)
        done = game_over

        # Reshape to keep compatibility with Keras
        next_state = np.reshape(next_state, [1, state_size])

        # Simple reward shaping: positive reward for surviving, negative for game over
        reward = 1 if not done else -10

        # Append experience to replay buffer
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        # Accumulate reward
        cumulative_reward += reward

        # Update policy if enough experience
        if len(agent.memory) > 2 * batch_size:
            loss = agent.replay(batch_size)

    return_history.append(cumulative_reward)
    agent.update_epsilon()

    print(f"Episode: {episode}/{NUM_EPISODES}, Score: {cumulative_reward}, Epsilon: {agent.epsilon}")

    # Plot and save model every 20 episodes
    if episode % 20 == 0:
        plt.plot(return_history, 'b')
        plt.xlabel('Episode')
        plt.ylabel('Return')
        plt.show(block=False)
        plt.pause(0.1)
        plt.savefig('dqn_training.png')

plt.pause(1.0)
