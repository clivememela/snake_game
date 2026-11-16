# cells & grid
CELL_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# colors
BG_COLOR = (25,25,35)
WHITE    = (240, 240, 240)

# ========== DIRECTIONS ==========
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

OPPOSITE = {
    UP:    DOWN,
    DOWN:  UP,
    LEFT:  RIGHT,
    RIGHT: LEFT,
}

# ========== TURN SPRITES ==========
# prev = segment - head_side_neighbour, next = segment - tail_side_neighbour
TURN_SPRITES = {
    # body-turn-drrd: snake body at bottom-right corner (right <-> down)
    (LEFT,  UP):   "body-turn-drrd",
    (UP,    LEFT): "body-turn-drrd",
    # body-turn-lddl: snake body at bottom-left corner (left <-> down)
    (RIGHT, UP):   "body-turn-lddl",
    (UP,    RIGHT):"body-turn-lddl",
    # body-turn-ullu: snake body at top-left corner (left <-> up)
    (RIGHT, DOWN): "body-turn-ullu",
    (DOWN,  RIGHT):"body-turn-ullu",
    # body-turn-urru: snake body at top-right corner (right <-> up)
    (LEFT,  DOWN): "body-turn-urru",
    (DOWN,  LEFT): "body-turn-urru",
}