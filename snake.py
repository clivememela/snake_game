from settings import (
    UP, DOWN, RIGHT, LEFT,
    OPPOSITE, CELL_SIZE, TURN_SPRITES,
    GRID_HEIGHT, GRID_WIDTH
)

from helpers import get_direction, direction_name

class Snake:
    def __init__(self):
        self.body = [
            (9, 9),
            (10, 9),
            (11, 9),
        ]
        self.direction = LEFT
        self.grow = False

    def set_direction(self, new_direction):
        if new_direction != OPPOSITE[self.direction]:
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def check_collision(self):
        head_x, head_y = self.body[0]

        # Check wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True

        # Check self collision
        if (head_x, head_y) in self.body[1:]:
            return True

        return False

    # ======= Drawing Methods =======
    def draw(self, surface, sprites):
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if i == 0:
                # Draw head
                sprite_name = f"head-{direction_name(self.direction)}"
            elif i == len(self.body) - 1:
                # Draw tail
                prev_segment = self.body[i - 1]
                tail_direction = get_direction(prev_segment, segment)
                sprite_name = f"tail-{direction_name(tail_direction)}"
            else:
                # Draw body
                prev_segment = self.body[i - 1]
                next_segment = self.body[i + 1]
                prev_direction = get_direction(segment, prev_segment)
                next_direction = get_direction(segment, next_segment)

                if (prev_direction, next_direction) in TURN_SPRITES:
                    sprite_name = TURN_SPRITES[(prev_direction, next_direction)]
                elif prev_direction[0] == 0:
                    sprite_name = "body-vertical"
                else:
                    sprite_name = "body-horizontal"

            sprite_image = sprites[sprite_name]
            surface.blit(sprite_image, rect)