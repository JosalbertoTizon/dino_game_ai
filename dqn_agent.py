import numpy as np
import random
from collections import deque
from tensorflow.keras import models, layers, optimizers, activations, losses


class DQNAgent:
    def __init__(self, state_size, action_size, gamma=0.95, epsilon=0.5, epsilon_min=0.01, epsilon_decay=0.98,
                 learning_rate=0.001, buffer_size=4098):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.learning_rate = learning_rate
        self.model = self.build_model()

    def build_model(self):
        model = models.Sequential()

        model.add(layers.Dense(2, activation='relu'))
        model.add(layers.Dense(2, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))

        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if not done:
                target[0][action] = reward + self.gamma * np.max(self.model.predict(next_state)[0])
            else:
                target[0][action] = reward
            # Filtering out states and targets for training
            states.append(state[0])
            targets.append(target[0])
        history = self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        # Keeping track of loss
        loss = history.history['loss'][0]
        return loss

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min
