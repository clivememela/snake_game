import os
import pygame

from settings import CELL_SIZE

def load_image(name):
    path = os.path.join("imgs", name)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image file '{name}' not found in '{path}' directory.")

    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

def load_sprites():
    return {
        "food":            load_image("food.png"),

        "head-up":         load_image("head-up.png"),
        "head-down":       load_image("head-down.png"),
        "head-left":       load_image("head-left.png"),
        "head-right":      load_image("head-right.png"),

        "tail-up":         load_image("tail-up.png"),
        "tail-down":       load_image("tail-down.png"),
        "tail-left":       load_image("tail-left.png"),
        "tail-right":      load_image("tail-right.png"),

        "body-vertical":   load_image("body-vertical.png"),
        "body-horizontal": load_image("body-horizontal.png"),

        "body-turn-drrd": load_image("body-turn-drrd.png"),
        "body-turn-lddl": load_image("body-turn-lddl.png"),
        "body-turn-ullu": load_image("body-turn-ullu.png"),
        "body-turn-urru": load_image("body-turn-urru.png"),
    }
