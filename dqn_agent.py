import numpy as np
import random
from collections import deque
from tensorflow.keras import models, layers, optimizers, activations, losses
from constants import *


def normalize_state(state):
    state[0][0] = state[0][0] / MAX_SPEED
    state[0][1] = state[0][1] / SCREEN_HEIGHT
    state[0][2] = state[0][2] / SCREEN_WIDTH
    state[0][3] = state[0][3] / SCREEN_HEIGHT
    state[0][4] = state[0][4] / SCREEN_WIDTH
    state[0][5] = state[0][5] / SCREEN_HEIGHT

    return state


class DQNAgent:
    def __init__(self, state_size, action_size, gamma=0.95, epsilon=0.5, epsilon_min=0.01, epsilon_decay=0.98,
                 learning_rate=0.001, buffer_size=4098):
        self.state_size = state_size
        self.action_size = action_size
        self.replay_buffer = deque(maxlen=buffer_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.learning_rate = learning_rate
        self.model = self.build_model()

    def build_model(self):
        model = models.Sequential()
        model.add(layers.Dense(32, activation='relu', input_dim=10))  # Assuming 10 input states
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def append_experience(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def act(self, state):
        state = np.reshape(state, [1, self.state_size])
        normalized_state = normalize_state(state)

        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        act_values = self.model.predict(normalized_state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.replay_buffer, batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in minibatch:
            state = np.reshape(state, [1, self.state_size])
            normalized_state = normalize_state(state)
            next_state = np.reshape(next_state, [1, self.state_size])
            normalized_next_state = normalize_state(next_state)

            target = self.model.predict(normalized_state, verbose=0)
            if not done:
                target[0][action] = reward + self.gamma * np.max(
                    self.model.predict(normalized_next_state, verbose=0)[0])
            else:
                target[0][action] = reward
            # Filtering out states and targets for training
            states.append(state[0])
            targets.append(target[0])
        history = self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        # Keeping track of loss
        loss = history.history['loss'][0]

        # Inform the user about the learning process
        print(f"Replay complete. Loss from network training with minibatch: {loss:.4f}")

        return loss

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min
