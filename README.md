# Pong AI Project

A collaborative project where we implemented intelligent AI for the classic Pong game.

## Overview

This project demonstrates our work on creating advanced AI for a Pong-like game. We focused on developing smart algorithms that can effectively control paddles and compete against human players or each other.

## Features of Our AI Implementation

- Predictive movement based on ball trajectory
- Strategic use of power-ups
- Momentum transfer handling
- Adaptive speed control

## Files

- `assets.py`: Contains the core game classes (Ball, Paddle) with our AI logic integrated
- `csp_pong.py`: Main game logic and mechanics
- `main.py`: Entry point for running the game with AI demonstration

## How to Run

1. Clone this repository:
   ```
   git clone https://github.com/liv-skeete/pong.git
   ```

2. Navigate to the project directory:
   ```
   cd pong
   ```

3. Install Pygame if you haven't already:
   ```
   pip install pygame
   ```

4. Run the game using Python:
   ```
   python main.py
   ```

## AI Implementation Details

Our AI implementation is focused on two main aspects:

1. **Predictive Movement**: The AI predicts where the ball will be based on its current trajectory and moves to intercept it.

2. **Strategic Power-up Use**: The AI uses power-ups at optimal times to gain an advantage, such as extending the paddle when necessary.

You can find our AI logic in the `assets.py` file, particularly in the Ball and Paddle classes.

## Contributors

- [Your Name]
- [Your Friend's Name]

## License

This project is open source and available under the MIT License.