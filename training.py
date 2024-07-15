import os
import matplotlib.pyplot as plt
from dqn_agent import DQNAgent
from game import Game

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress informational messages and warnings

# Hyperparameters
EPISODE_TIME = 100  # Episode duration in seconds
NUM_EPISODES = 150  # Number of episodes used for training
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
    cumulative_reward = 0.0
    elapsed_time = 0

    while elapsed_time < EPISODE_TIME:
        # Select action
        action = agent.act(state)
        # Take action, observe reward and new state
        next_state, reward, speed_multiplier, game_over, dt = game.step(action)
        elapsed_time += dt
        done = game_over

        # Improve reward
        is_low = 1 if (state[5] > 400) else 0
        close_to_obstacle = 1 if 0 < state[2] < 200 else 0
        is_jumping = state[6]
        is_ducking = state[8]

        # Penalize for not jumping over low obstacles
        reward += - close_to_obstacle * is_low * (not is_jumping) * 30

        # Penalize for jumping when far away from low obstacles
        reward += - (not close_to_obstacle) * is_low * is_jumping * 100

        # Penalize for not ducking below high birds
        reward += - close_to_obstacle * (not is_low) * (not is_ducking) * 30

        # Penalize severely for ducking when far away from high birds
        reward += - (not close_to_obstacle) * (not is_low) * is_ducking * 100

        # Add a small reward for jumping so that it doesn't duck all time
        reward += is_jumping * 10

        # Correct reward according to simulation speed
        reward = reward * speed_multiplier  # Since all rewards are per frame

        # Append experience to replay buffer
        agent.append_experience(state, action, reward, next_state, done)
        state = next_state

        # Accumulate reward
        cumulative_reward += reward

    # Update policy if enough experience
    if len(agent.replay_buffer) > 4 * batch_size and episode % 5 == 0:  # The policy will not be updated after
        loss = agent.replay(batch_size)                                 # each epoch since it's too time-consuming

    agent.update_epsilon()

    print(f"Episode: {episode}/{NUM_EPISODES}, Reward: {cumulative_reward}, Epsilon: {agent.epsilon}")

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
    game_over = False

    while not game_over:
        action = agent.act(state)
        next_state, _, speed_multiplier, game_over, _ = game.step(action)
        state = next_state

    print("Game over! Restarting...")
