import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from settings import UP, DOWN, LEFT, RIGHT, OPPOSITE, TURN_SPRITES, GRID_WIDTH, GRID_HEIGHT
from helpers import get_direction, direction_name
from snake import Snake
from food import Food


# ─── helpers ────────────────────────────────────────────────────────────────

class TestGetDirection:
    def test_right(self):
        assert get_direction((2, 0), (1, 0)) == RIGHT

    def test_left(self):
        assert get_direction((1, 0), (2, 0)) == LEFT

    def test_down(self):
        assert get_direction((0, 2), (0, 1)) == DOWN

    def test_up(self):
        assert get_direction((0, 1), (0, 2)) == UP


class TestDirectionName:
    def test_all(self):
        assert direction_name(UP)    == "up"
        assert direction_name(DOWN)  == "down"
        assert direction_name(LEFT)  == "left"
        assert direction_name(RIGHT) == "right"


# ─── snake ──────────────────────────────────────────────────────────────────

class TestSnakeInit:
    def test_initial_length(self):
        assert len(Snake().body) == 3

    def test_initial_direction(self):
        assert Snake().direction == LEFT

    def test_grow_false(self):
        assert Snake().grow is False


class TestSnakeSetDirection:
    def test_changes_direction(self):
        s = Snake()
        s.set_direction(UP)
        assert s.direction == UP

    def test_ignores_opposite(self):
        s = Snake()
        s.direction = RIGHT
        s.set_direction(LEFT)
        assert s.direction == RIGHT

    def test_allows_perpendicular(self):
        s = Snake()
        s.direction = UP
        s.set_direction(RIGHT)
        assert s.direction == RIGHT


class TestSnakeMove:
    def test_head_advances(self):
        s = Snake()
        s.direction = LEFT
        old_head = s.body[0]
        s.move()
        assert s.body[0] == (old_head[0] - 1, old_head[1])

    def test_length_unchanged_without_grow(self):
        s = Snake()
        length = len(s.body)
        s.move()
        assert len(s.body) == length

    def test_grows_when_flag_set(self):
        s = Snake()
        length = len(s.body)
        s.grow = True
        s.move()
        assert len(s.body) == length + 1
        assert s.grow is False


class TestSnakeCollision:
    def test_no_collision_initially(self):
        assert Snake().check_collision() is False

    def test_wall_left(self):
        s = Snake()
        s.body[0] = (-1, 5)
        assert s.check_collision() is True

    def test_wall_right(self):
        s = Snake()
        s.body[0] = (GRID_WIDTH, 5)
        assert s.check_collision() is True

    def test_wall_top(self):
        s = Snake()
        s.body[0] = (5, -1)
        assert s.check_collision() is True

    def test_wall_bottom(self):
        s = Snake()
        s.body[0] = (5, GRID_HEIGHT)
        assert s.check_collision() is True

    def test_self_collision(self):
        s = Snake()
        s.body = [(5, 5), (5, 6), (5, 7), (5, 5)]
        assert s.check_collision() is True


# ─── snake draw ──────────────────────────────────────────────────────────────

def make_sprites():
    return {k: MagicMock() for k in [
        "head-up", "head-down", "head-left", "head-right",
        "tail-up", "tail-down", "tail-left", "tail-right",
        "body-vertical", "body-horizontal",
        "body-turn-drrd", "body-turn-lddl", "body-turn-ullu", "body-turn-urru",
    ]}


class TestSnakeDraw:
    def test_draw_calls_blit_for_each_segment(self):
        s = Snake()
        s.body = [(5, 5), (6, 5), (7, 5)]
        s.direction = LEFT
        surface = MagicMock()
        s.draw(surface, make_sprites())
        assert surface.blit.call_count == 3

    def test_draw_vertical_body(self):
        s = Snake()
        s.body = [(5, 5), (5, 6), (5, 7)]
        s.direction = UP
        surface = MagicMock()
        s.draw(surface, make_sprites())
        assert surface.blit.call_count == 3

    def test_draw_with_turn(self):
        s = Snake()
        s.body = [(5, 5), (6, 5), (6, 6)]
        s.direction = LEFT
        surface = MagicMock()
        s.draw(surface, make_sprites())
        assert surface.blit.call_count == 3


# ─── food ────────────────────────────────────────────────────────────────────

class TestFood:
    def test_not_on_snake(self):
        s = Snake()
        f = Food(s.body)
        assert f.position not in s.body

    def test_respawn_not_on_snake(self):
        s = Snake()
        f = Food(s.body)
        f.respawn(s.body)
        assert f.position not in s.body

    def test_position_within_grid(self):
        s = Snake()
        f = Food(s.body)
        x, y = f.position
        assert 0 <= x < GRID_WIDTH
        assert 0 <= y < GRID_HEIGHT

    def test_respawn_forced_to_only_free_cell(self):
        all_cells = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        free = (0, 0)
        occupied = [c for c in all_cells if c != free]
        f = Food([])
        f.respawn(occupied)
        assert f.position == free


# ─── settings ────────────────────────────────────────────────────────────────

class TestSettings:
    def test_opposites(self):
        assert OPPOSITE[UP]    == DOWN
        assert OPPOSITE[DOWN]  == UP
        assert OPPOSITE[LEFT]  == RIGHT
        assert OPPOSITE[RIGHT] == LEFT

    def test_turn_sprites_keys(self):
        for pair in [(LEFT, UP), (UP, LEFT), (RIGHT, UP), (UP, RIGHT),
                     (RIGHT, DOWN), (DOWN, RIGHT), (LEFT, DOWN), (DOWN, LEFT)]:
            assert pair in TURN_SPRITES

    def test_turn_sprites_count(self):
        assert len(TURN_SPRITES) == 8


# ─── game update logic ───────────────────────────────────────────────────────

def make_game():
    import pygame
    pygame.init()
    screen  = MagicMock()
    clock   = MagicMock()
    font    = MagicMock()
    font.render.return_value = MagicMock(get_rect=MagicMock(return_value=MagicMock()))
    from game import Game
    return Game(screen, font, make_sprites(), clock)


def place_food_at_next_head(g):
    hx, hy = g.snake.body[0]
    dx, dy = g.snake.direction
    g.food.position = (hx + dx, hy + dy)


class TestGameUpdate:
    def test_no_update_when_game_over(self):
        g = make_game()
        g.game_over = True
        head_before = g.snake.body[0]
        g.update()
        assert g.snake.body[0] == head_before

    def test_collision_sets_game_over(self):
        g = make_game()
        g.snake.direction = LEFT
        g.snake.body[0] = (0, 5)
        g.update()
        assert g.game_over is True

    def test_eating_food_increases_score(self):
        g = make_game()
        place_food_at_next_head(g)
        g.update()
        assert g.score == 1

    def test_eating_food_sets_grow(self):
        g = make_game()
        place_food_at_next_head(g)
        g.update()
        assert g.snake.grow is True

    def test_eating_food_increases_speed(self):
        g = make_game()
        speed_before = g.speed
        place_food_at_next_head(g)
        g.update()
        assert g.speed > speed_before

    def test_speed_capped_at_20(self):
        g = make_game()
        g.speed = 19.5
        place_food_at_next_head(g)
        g.update()
        assert g.speed == 20

    def test_reset_restores_state(self):
        g = make_game()
        g.score = 10
        g.game_over = True
        g.speed = 15
        g.reset()
        assert g.score == 0
        assert g.game_over is False
        assert g.speed == 3
