import random

import numpy as np

class Movement():
    UNCHANGED = np.array([0, 0])
    UP = np.array([0, -1])
    LEFT = np.array([-1, 0])
    DOWN = np.array([0, 1])
    RIGHT = np.array([1, 0])

    def equals(a, b):
        return (a == b).all()

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_center_coordinates(self):
        return [round(self.width/2.0), round(self.height/2.0)]

    def is_in_map(self, coordinates) -> bool:
        x = coordinates[0]
        y = coordinates[1]
        return -1 < x < self.width and -1 < y < self.height

    def is_boundry(self, coordinates) -> bool:
        return not self.is_in_map(coordinates)

    def get_random_coordinates(self) -> list:
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return [x, y]

class Snake():
    def __init__(self, x, y) -> None:
        self.body = [np.array([x, y])]
        self.direction = Movement.UNCHANGED

    def opposite_direction(self, move:Movement) -> bool:
        return Movement.equals(move + self.direction, Movement.UNCHANGED)

    def update_direction(self, move:Movement):
        if (move != Movement.UNCHANGED).any() and not self.opposite_direction(move):
            self.direction = move

    def head(self):
        return self.body[-1]

    def get_next_head(self):
        return self.head() + self.direction

    def move(self, growing=False):
        new_head = self.get_next_head()
        self.body.append(new_head)

        if not growing:
            self.body.pop(0) # remove last tail element

    def is_snake_body(self, coordinates, ignore_tail_elemts:int=1):
        result = False
        for i in range(ignore_tail_elemts, len(self.body)):
            if (self.body[i] == coordinates).all():
                result = True
        return result

class Game():
    def __init__(self, width, height) -> None:
        self.map = Map(width, height)
        center = self.map.get_center_coordinates()
        self.snake = Snake(x=center[0], y=center[1])
        self.food = None
        self.generate_food()
        self.game_over = False
        self.score = 0

    def generate_food(self):
        while True:
            food_candidate = self.map.get_random_coordinates()
            if not self.snake.is_snake_body(food_candidate, ignore_tail_elemts=0):
                self.food = np.array(food_candidate)
                break

    def evaluate(self, move:Movement):
        self.snake.update_direction(move)
        next_head = self.snake.get_next_head()

        if (self.map.is_boundry(next_head) or self.snake.is_snake_body(next_head)):
            print("Game Over!")
            self.game_over = True
        elif (next_head == self.food).all():
            self.snake.move(growing=True)
            self.generate_food()
            self.score += 1
        else:
            self.snake.move(growing=False)
