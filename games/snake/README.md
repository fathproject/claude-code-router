# Snake Game

A classic Snake game implementation using Python and Pygame.

## Features

- **Classic Gameplay**: Control a snake to eat food and grow longer
- **Collision Detection**: Game ends when snake hits walls or itself
- **Scoring System**: Earn 10 points for each food item eaten
- **Restart Functionality**: Press 'R' to restart after game over
- **Smooth Controls**: Use arrow keys to control the snake

## Requirements

- Python 3.6 or higher
- Pygame library

## Installation

1. Make sure you have Python installed on your system
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install pygame directly:

```bash
pip install pygame
```

## How to Play

1. Run the game:

```bash
python snake_game.py
```

2. **Controls**:
   - **Arrow Keys**: Move the snake (Up, Down, Left, Right)
   - **R**: Restart the game (when game over)
   - **ESC**: Quit the game

3. **Objective**: 
   - Control the green snake to eat the red food
   - Each food eaten increases your score by 10 points
   - The snake grows longer with each food consumed
   - Avoid hitting the walls or the snake's own body

## Game Rules

- The snake moves continuously in the direction of the last arrow key pressed
- You cannot move directly backward into the snake's body
- Game ends when the snake hits a wall or collides with itself
- Score increases by 10 for each food item eaten

## Game Features

- **Grid-based Movement**: Smooth movement on a 20x20 pixel grid
- **Visual Feedback**: Different colors for snake head and body
- **Score Display**: Real-time score tracking
- **Game Over Screen**: Clear indication when game ends with restart option

Enjoy playing the classic Snake game!