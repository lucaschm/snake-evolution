import pygame

import sys
import time

from snake import Movement, Snake, Map, Game
from game_vision import GameVision

# Map Size
WIDTH = 25
HEIGHT = 12

# Constants
CELL_SIZE = 40
SPEED = 3

# Map colors
COLOR_BG = (255, 255, 255)
COLOR_SNAKE = (150, 230, 150)
COLOR_FOOD = (230, 100, 100)
COLOR_GRID = (225, 225, 225)

# Input mapping
KEY_TO_MOVE = {
    pygame.K_UP: Movement.UP,
    pygame.K_DOWN: Movement.DOWN,
    pygame.K_LEFT: Movement.LEFT,
    pygame.K_RIGHT: Movement.RIGHT,
}

def draw_grid(screen, game_map):
    for x in range(game_map.width):
        for y in range(game_map.height):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)

def draw_snake(screen, snake):
    for segment in snake.body:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLOR_SNAKE, rect)
        pygame.draw.rect(screen, COLOR_GRID, rect, 1)

def draw_food(screen, food):
    center_x = food[0] * CELL_SIZE + CELL_SIZE // 2
    center_y = food[1] * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2

    pygame.draw.circle(screen, COLOR_FOOD, (center_x, center_y), radius)


def run_game():
    pygame.init()

    game = Game(width=WIDTH, height=HEIGHT)
    game_vision = GameVision(game)
    
    screen_width = game.map.width * CELL_SIZE
    screen_height = game.map.height * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    while not game.game_over:
        move = Movement.UNCHANGED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_MOVE:
                    move = KEY_TO_MOVE[event.key]

        game.evaluate(move)

        screen.fill(COLOR_BG)
        draw_grid(screen, game.map)
        draw_snake(screen, game.snake)
        draw_food(screen, game.food)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(SPEED)

    print(f"Final Score: {game.score}")
    time.sleep(2)
    pygame.quit()

if __name__ == "__main__":
    run_game()
