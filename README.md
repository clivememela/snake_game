# 🐍 Snake Game

A classic Snake game built with Python and [pygame-ce](https://pyga.me/). Navigate the snake to eat food, grow longer, and beat your high score — without hitting the walls or yourself.

---

## Table of Contents

- [Preview](#preview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Controls](#controls)
- [Gameplay](#gameplay)
- [Game Mechanics](#game-mechanics)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Testing](#testing)
- [Configuration](#configuration)

---

## Preview

The snake grows longer each time it eats food. Speed increases with every meal. The game ends when the snake hits a wall or its own body.

---

## Requirements

- Python 3.10+
- pygame-ce 2.5.8

---

## Installation

1. Clone or download the repository:

```bash
git clone <repository-url>
cd snake_game
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Game

```bash
python main.py
```

---

## Controls

| Key     | Action                    |
| ------- | ------------------------- |
| ↑ Arrow | Move Up                   |
| ↓ Arrow | Move Down                 |
| ← Arrow | Move Left                 |
| → Arrow | Move Right                |
| R-r     | Restart (after game over) |
| Q-q     | Quit (anytime)            |

---

## Gameplay

- The snake starts with **3 segments** in the centre of the grid
- Eat food to grow longer and increase your score
- Each food eaten adds **+1 to the score** and slightly increases movement speed
- The game ends on collision with a **wall** or the **snake's own body**
- On game over, press **R** to restart or **Q** to quit

---

## Game Mechanics

### Movement

The snake moves one grid cell per tick in the current direction. The direction can be changed at any time, except reversing directly into itself (180° turns are blocked).

### Speed Scaling

| Event           | Speed Change       |
| --------------- | ------------------ |
| Game start      | 3 ticks/sec        |
| Each food eaten | +0.5 ticks/sec     |
| Maximum speed   | 20 ticks/sec (cap) |

### Collision Detection

- **Wall collision** — head moves outside the 20×20 grid boundary
- **Self collision** — head occupies the same cell as any body segment

### Food Spawning

Food spawns at a random grid cell that is not currently occupied by the snake. On being eaten, it immediately respawns at a new valid position.

### Sprite Rendering

Each snake segment is rendered with a directional sprite:

- **Head** — faces the current movement direction
- **Body (straight)** — vertical or horizontal depending on axis of travel
- **Body (turn)** — one of 4 corner sprites based on the incoming and outgoing directions
- **Tail** — faces away from the body toward the end of the snake

---

## Project Structure

```
snake_game/
├── main.py             # Entry point — initialises pygame and starts the game
├── game.py             # Game loop, input handling, update logic, rendering
├── snake.py            # Snake state, movement, collision detection, drawing
├── food.py             # Food position, random spawning, drawing
├── assets.py           # Loads and scales all sprite images from imgs/
├── settings.py         # Constants: grid size, colors, directions, turn sprite map
├── helpers.py          # Direction vector utilities (get_direction, direction_name)
├── requirements.txt    # Python dependencies (pygame-ce)
├── pytest.ini          # Pytest and coverage configuration
├── tests/
│   └── test_game.py    # Unit tests (37 tests, 83% coverage)
└── imgs/               # PNG sprite assets for snake and food
    ├── head-{up,down,left,right}.png
    ├── tail-{up,down,left,right}.png
    ├── body-vertical.png
    ├── body-horizontal.png
    ├── body-turn-{drrd,lddl,ullu,urru}.png
    └── food.png
```

---

## Architecture Overview

```
main.py
  └── Game (game.py)
        ├── Snake (snake.py)       # movement, collision, draw
        ├── Food (food.py)         # spawn, respawn, draw
        └── assets / settings      # sprites, constants
```

The `Game` class owns the main loop and orchestrates three responsibilities each frame:

1. **handle_input** — processes pygame events and updates snake direction
2. **update** — moves the snake, checks collisions, handles food eating
3. **draw** — renders background, food, snake, and UI overlay

State is fully reset via `Game.reset()`, which is called on both startup and restart.

---

## Testing

Tests are located in `tests/test_game.py` and cover core game logic without requiring a display.

### Run tests

```bash
python -m pytest tests/test_game.py -v
```

### Run with coverage report

```bash
python -m pytest tests/test_game.py -v --cov=. --cov-report=term-missing
```

### Coverage summary

| Module        | Coverage |
| ------------- | -------- |
| `helpers.py`  | 100%     |
| `settings.py` | 100%     |
| `snake.py`    | 100%     |
| `food.py`     | 83%      |
| `game.py`     | 47%      |
| **Total**     | **83%**  |

> `game.py` draw and input methods require a live pygame display and are excluded from automated testing.

### What is tested

- Direction helpers (`get_direction`, `direction_name`)
- Snake initialisation, direction changes, movement, growth, collision detection, and sprite drawing
- Food spawning, respawning, and grid boundary constraints
- Settings constants and turn sprite key mappings
- Game update logic: score, speed scaling, speed cap, grow flag, game over, and reset

---

## Configuration

Key constants in `settings.py`:

| Constant      | Value        | Description                   |
| ------------- | ------------ | ----------------------------- |
| `GRID_WIDTH`  | 20           | Number of columns in the grid |
| `GRID_HEIGHT` | 20           | Number of rows in the grid    |
| `CELL_SIZE`   | 32           | Pixel size of each grid cell  |
| `BG_COLOR`    | (25, 25, 35) | Background colour (dark navy) |

Starting speed and speed cap are configured in `game.py`:

```python
self.speed = 3          # initial ticks/sec
self.speed = min(self.speed + 0.5, 20)  # per food eaten, capped at 20
```
