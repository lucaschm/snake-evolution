from snake import Movement, Map, Snake, Game

class GameVision():
    def __init__(self, game:Game):
        self.game = game
        self.width = self.game.map.width
        self.height = self.game.map.height

    def is_moving_up(self) -> bool:
        direction = self.game.snake.direction
        return Movement.equals(direction, Movement.UP)

    def is_moving_left(self) -> bool:
        direction = self.game.snake.direction
        return Movement.equals(direction, Movement.LEFT)

    def is_moving_down(self) -> bool:
        direction = self.game.snake.direction
        return Movement.equals(direction, Movement.DOWN)

    def is_moving_right(self) -> bool:
        direction = self.game.snake.direction
        return Movement.equals(direction, Movement.RIGHT)

    def get_upwards_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        y = head[1]
        return y / self.height

    def get_left_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        x = head[0]
        return 1.0 - x / self.width

    def get_downwards_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        y = head[1]
        return 1.0 - y / self.height

    def get_right_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        x = head[0]
        return x / self.width

    def get_upwards_proximity_to_food(self) -> float:
        head = self.game.snake.head()
        food = self.game.food
        if (head[0] == food[0] and head[1] < food[1]):
            return 1.0 - ((food[1] - head[1] - 1) / self.height)
        else:
            return 0.0

    def get_left_proximity_to_food(self) -> float:
        head = self.game.snake.head()
        food = self.game.food
        if (head[1] == food[1] and head[0] > food[0]):
            return 1.0 - ((head[0] - food[0] - 1) / self.width)
        else:
            return 0.0

    def get_downwards_proximity_to_food(self) -> float:
        head = self.game.snake.head()
        food = self.game.food
        if (head[0] == food[0] and head[1] > food[1]):
            return 1.0 - ((head[1] - food[1] - 1) / self.height)
        else:
            return 0.0

    def get_right_proximity_to_food(self) -> float:
        head = self.game.snake.head()
        food = self.game.food
        if (head[1] == food[1] and head[0] < food[0]):
            return 1.0 - ((food[0] - head[0] - 1) / self.width)
        else:
            return 0.0
