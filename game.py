import pygame
import sys
# from settings import *
from settings import (
    BG_COLOR, WHITE, HEIGHT, WIDTH,
    UP, DOWN, LEFT, RIGHT
)

from snake import Snake
from food import Food
# from helpers import get_direction, direction_name
#================ GAME CLASS =================
class Game:
    # === INIT ===
    def __init__(self, screen, font, sprites, clock):
        self.screen = screen
        self.font = font
        self.sprites = sprites
        self.clock = clock
        self.reset()

    # === GAME LOGIC ===
    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.paused = True
        self.speed = 3

    # === INPUT HANDLING ===
    def handle_input(self):
        # ==== Handle Events ====
        for event in pygame.event.get():
            # === QUIT ====
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # === KEYDOWN ====
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.paused = not self.paused

            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                 if not self.game_over:
                    arrow_keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
                    if event.key in arrow_keys:
                        self.paused = False
                    if   event.key == pygame.K_UP:    self.snake.set_direction(UP)
                    elif event.key == pygame.K_DOWN:  self.snake.set_direction(DOWN)
                    elif event.key == pygame.K_LEFT:  self.snake.set_direction(LEFT)
                    elif event.key == pygame.K_RIGHT: self.snake.set_direction(RIGHT)
                 else:
                    if event.key == pygame.K_r:
                        self.reset()

    # ===== UI =====
    # ===== Drawing Methods =====
    # Draw the score and game over message
    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.paused and not self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(170)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("SNAKE", True, WHITE)
            hint  = self.font.render("Press any arrow key or click to start", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            self.screen.blit(hint,  hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(170)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            game_over = self.font.render("GAME OVER", True, WHITE)
            restart   = self.font.render("Press R-r To Restart", True, WHITE)
            quit_text = self.font.render("Press Q-q To Quit", True, WHITE)

            self.screen.blit(
                game_over,
                game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            )
            self.screen.blit(
                restart,
                restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            )
            self.screen.blit(
                quit_text,
                quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45))
            )

    # === DRAWING ===
    def draw(self):
        # Fill the background
        self.screen.fill(BG_COLOR)

        self.food.draw(self.screen, self.sprites)
        self.snake.draw(self.screen, self.sprites)

        self.draw_ui()
        pygame.display.flip()

    def update(self):
        # ==== Update Snake Position ====
        if self.game_over or self.paused:
            return

        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True
            return

        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.food.respawn(self.snake.body)
            self.score += 1
            self.speed = min(self.speed + 0.5, 20)

    # === MAIN LOOP ===
    def run(self):
        # === Main Game Loop ===
        while True:
            # handle inputs
            self.handle_input()
            # update game status
            self.update()
            # draw game components
            self.draw()
            # delay
            self.clock.tick(self.speed)
            