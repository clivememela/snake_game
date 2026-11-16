# Snake Game

A classic Snake game built with Python and pygame-ce.

## Preview

The snake grows longer each time it eats food. The game ends if the snake hits a wall or itself. Try to beat your high score!

## Requirements

- Python 3.10+
- pygame-ce 2.5.8

## Installation

1. Clone or download the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

| Key     | Action                    |
| ------- | ------------------------- |
| ↑ Arrow | Move Up                   |
| ↓ Arrow | Move Down                 |
| ← Arrow | Move Left                 |
| → Arrow | Move Right                |
| R/r     | Restart (after game over) |
| Q/q     | Quit                      |

## Gameplay

- The snake starts with 3 segments and moves at a base speed of 5
- Each piece of food eaten increases the score by 1 and slightly increases speed
- The game ends if the snake collides with a wall or its own body
- Press **R** to restart or **Q** to quit when the game is over

## Project Structure

```
snake_game/
├── main.py             # Entry point
├── game.py             # Main game loop, input handling, rendering
├── snake.py            # Snake movement, collision, drawing
├── food.py             # Food spawning and drawing
├── assets.py           # Sprite loading
├── settings.py         # Constants (grid size, colors, directions, sprites)
├── helpers.py          # Direction utilities
├── requirements.txt    # Pygame depency comminity edition (pygame-ce)
└── imgs/               # Sprite assets
```
