import os
import numpy as np
import matplotlib.pyplot as plt
from dqn_agent import DQNAgent
from game import Game

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress informational messages and warnings

# Hyperparameters
EPISODE_TIME = 50  # Episode duration in seconds
NUM_EPISODES = 300  # Number of episodes used for training
batch_size = 32  # Batch size used for experience replay

# Comment this line to enable training using your GPU
#  os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Initialize the game environment
speed_multiplier = 1

# Create the DQN agent
state_size = 11  # Your game state size
action_size = 3  # Number of actions: 0 (No action), 1 (Jump), 2 (Duck)
agent = DQNAgent(state_size, action_size)

reward_history = []
loss_history = []

# Training loop
for episode in range(1, NUM_EPISODES + 1):
    # Reset the environment
    game = Game(speed_multiplier, True, False)
    state = game.get_state()
    cumulative_reward = 0.0
    elapsed_time = 0
    episode_loss = 0.0

    while elapsed_time < EPISODE_TIME:
        # Select action
        action = agent.act(state)
        # Take action, observe reward and new state
        next_state, reward, speed_multiplier, game_over, dt = game.step(action)
        elapsed_time += dt
        done = game_over

        # Improve reward
        is_low = 1 if (state[5] > 400) else 0
        close_to_obstacle = 1 if (0 < state[2] < 150 or 0 < state[10] < 150) else 0
        if state[2] > 300:
            far_from_obstacle = 1
        elif 1200 > state[10] > 300 and not close_to_obstacle:  # if state[10] == 1200, then second obstacle doesn't exist
            far_from_obstacle = 1
        else:
            far_from_obstacle = 0
        is_jumping = state[6]
        is_ducking = state[8]

        # Penalize for not jumping over low obstacles
        reward += - (close_to_obstacle * is_low * (not is_jumping)) * 10

        # Penalize for jumping when far away from obstacles
        reward += - (far_from_obstacle * is_jumping and state[2] > 300) * 30

        # Penalize for not ducking below high birds
        reward += - (close_to_obstacle * (not is_low) * (not is_ducking)) * 10

        # Penalize for ducking when far away from obstacles
        reward += - (far_from_obstacle * is_ducking * state[2] > 300) * 30

        # Correct reward according to simulation speed
        reward = reward * speed_multiplier  # Since all rewards are per frame

        # Append experience to replay buffer
        agent.append_experience(state, action, reward, next_state, done)
        state = next_state

        # Accumulate reward
        cumulative_reward += reward

    # Update policy if enough experience
    if len(agent.replay_buffer) > 4 * batch_size:
        loss = agent.replay(batch_size)
        episode_loss = loss

    agent.update_epsilon()

    print(f"Episode: {episode}/{NUM_EPISODES}, Reward: {cumulative_reward}, Epsilon: {agent.epsilon}")

    reward_history.append(cumulative_reward)
    loss_history.append(episode_loss)

print(reward_history)
print(loss_history)
# nao ta funcionando (era pra plotar) !!!
# # Ensure the arrays are one-dimensional
# reward_history = np.squeeze(reward_history)
# loss_history = np.squeeze(loss_history)
#
# # Check the dimensions of the arrays
# print("Reward history shape:", reward_history.shape)
# print("Loss history shape:", loss_history.shape)
#
# # Plotting the histories
# plt.figure(figsize=(12, 5))
#
# # Plot loss history
# plt.subplot(1, 2, 1)
# plt.plot(loss_history, label='Loss per Epoch')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.title('Loss History')
# plt.legend()
#
# # Plot reward history
# plt.subplot(1, 2, 2)
# plt.plot(reward_history, label='Reward per Epoch')
# plt.xlabel('Epoch')
# plt.ylabel('Reward')
# plt.title('Reward History')
# plt.legend()
#
# plt.tight_layout()
# plt.show()

# Start playing indefinitely after trained
while True:
    game = Game(speed_multiplier, False, False)
    state = game.get_state()
    game_over = False

    while not game_over:
        action = agent.act(state)
        next_state, _, speed_multiplier, game_over, _ = game.step(action)
        state = next_state

    print("Game over! Restarting...")
