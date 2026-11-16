import random

from settings import GRID_HEIGHT, GRID_WIDTH, CELL_SIZE

#================ FOOD CLASS =================
class Food:
    # ================ INIT =================
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)

    # ====== GENERATE RANDOM POSITION ========
    def generate_position(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)

            if position not in snake_body:
                return position

    # ======= DRAWING METHODS ========
    # Draw the food on the screen
    def draw(self, surface, sprites):
        x, y = self.position
        rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        surface.blit(
            sprites["food"],
            (x * CELL_SIZE, y * CELL_SIZE)
        )
    # ======= RESPAWN ========
    def respawn(self, snake_body):
        self.position = self.generate_position(snake_body)

    