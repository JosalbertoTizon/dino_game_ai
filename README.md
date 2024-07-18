# Chrome Dinosaur Game using Deep Q-Learning

## Description
This project was created as the final exam for the course on Artificial Intelligence for Mobile Robotics. It features a Deep Q-Network (DQN) agent designed to autonomously play the Chrome Dino game. The project aims to use reinforcement learning to master the timing and control required to maximize game scores by avoiding obstacles.

## Features
- **Chrome Dino Simulation**: Leverages the popular Chrome Dino game to simulate an environment where the DQN agent learns obstacle avoidance.
- **DQN Agent Training**: Employs a DQN model to train the agent in making optimal decisions based on the game's dynamics.
- **Manual Gameplay Option**: Allows users to play the game manually, serving as a fun way to interact with the game and compare human performance to the AI agent.
- **Performance Evaluation**: Tracks the agent's performance, providing insights into its learning progress and efficiency improvements over time.

## Installation

### Prerequisites
Use Python 3.11, along with the following libraries:

- TensorFlow
- TF-Keras
- NumPy
- MatPlotLib

### Setup
Clone the repository and install the required dependencies:
```bash
git clone [repository URL]
cd [repository directory name]

# Install dependencies
pip install tensorflow numpy tf_keras matplotlib
# Or
pip install -r requirements.txt
```

## How To Use
To start training, simply run training.py:
```bash
python training.py
```
To change to manual mode, switch manual_playing from False to True in training.py:
```python
# Use the lines bellow to choose if playing manually
# manual_playing = False
manual_playing = True
```
### Controls

- `H` - Toggle Hitboxes
- `X` - Speed Up Simulation
- `Z` - Slow Down Simulation
- `Up Arrow` - Jump
- `Down Arrow` - Duck



