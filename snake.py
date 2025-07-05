import numpy as np
from enum import Enum, auto

class Movement():
    UNCHANGED = np.array([0, 0])
    UP = np.array([0, 1])
    LEFT = np.array([-1, 0])
    DOWN = np.array([0, -1])
    RIGHT = np.array([1, 0])

class Health(Enum):
    ALIVE = "alive"
    DEAD = "dead"

class Snake():
    def __init__(self, x, y) -> None:
        self.body = [np.array([x, y])]
        self.direction = Movement.UNCHANGED



    def opposite_direction(self, move:Movement) -> bool:
        return sum(move + self.direction) == 0

    def update_direction(self, move:Movement):
        if move != Movement.UNCHANGED and not self.opposite_direction(move):
            self.direction = move



    def get_next_head(self):
        return self.body.head() + self.direction

    def head(self):
        return self.body[-1]

    def move(self, growing=False):
        new_head = self.get_next_head()
        self.body.append(new_head)

        if not growing:
            self.body.pop(0) # remove last tail element

    def is_snake_body(self, coordinates):
        result = False
        for i in range(1, self.body.len()): # ignore last tail element
            if (self.body[i] == coordinates).all():
                result = True
        return result

class Game():
    ... # TODO

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_center_position(self):
        return [round(self.width/2.0), round(self.height/2.0)]


if __name__ == '__main__':
    pos = np.array([5, 6])
    segment = np.array([4, 6])

    print((pos == segment).all())

