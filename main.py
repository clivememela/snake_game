import pygame

from settings import WIDTH, HEIGHT
from game import Game
from assets import load_sprites
# main function to run the game
def main():
    # Initialize Pygame
    pygame.init()
    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # Set the window title
    pygame.display.set_caption("Snake Game")
    # Create the font
    font = pygame.font.SysFont("Arial", 28, bold=True)

    # Create the clock
    clock = pygame.time.Clock()

    # Load sprites
    sprites = load_sprites()
    # Create the game instance
    game = Game(screen, font, sprites, clock)
    # Run the game
    game.run()
    
main()