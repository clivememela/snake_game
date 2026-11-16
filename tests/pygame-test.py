import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Snake Game Test")
font = pygame.font.SysFont("Arial", 28, bold=True)
text = font.render("Hello, Snake Game!", True, (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    screen.blit(text, (50, 100))
    pygame.display.flip()