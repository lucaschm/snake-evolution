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

    def get_upwards_distance_to_boundry(self) -> float:
        head = self.game.snake.head()
        y = head[1]
        return y

    def get_left_distance_to_boundry(self) -> float:
        head = self.game.snake.head()
        x = head[0]
        return x

    def get_downwards_distance_to_boundry(self) -> float:
        head = self.game.snake.head()
        y = head[1]
        return self.height - 1 - y 

    def get_right_distance_to_boundry(self) -> float:
        head = self.game.snake.head()
        x = head[0]
        return self.width - 1 - x

    def get_upwards_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        y = head[1]
        return 1.0 - y / self.height

    def get_left_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        x = head[0]
        return 1.0 - x / self.width

    def get_downwards_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        y = head[1]
        return (y + 1) / self.height

    def get_right_proximity_to_boundry(self) -> float:
        head = self.game.snake.head()
        x = head[0]
        return (x + 1) / self.width

    def get_upwards_proximity_to_food(self) -> float:
        head = self.game.snake.head()
        food = self.game.food
        if (head[0] == food[0] and head[1] > food[1]):
            return 1.0 - ((head[1] - food[1] - 1) / self.height)
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
        if (head[0] == food[0] and head[1] < food[1]):
            return 1.0 - ((food[1] - head[1] - 1) / self.height)
        else:
            return 0.0

    def get_right_proximity_to_food(self) -> float:
        head = self.game.snake.head()
        food = self.game.food
        if (head[1] == food[1] and head[0] < food[0]):
            return 1.0 - ((food[0] - head[0] - 1) / self.width)
        else:
            return 0.0

### AHEAD METHODS ###
    # def get_food_distance_ahead(self) -> int:
    #     ...
    def get_food_proximity_ahead(self) -> float:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_upwards_proximity_to_food()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_left_proximity_to_food()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_downwards_proximity_to_food()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_right_proximity_to_food()

    def get_boundry_distance_ahead(self) -> int:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_upwards_distance_to_boundry()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_left_distance_to_boundry()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_downwards_distance_to_boundry()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_right_distance_to_boundry()

    def get_boundry_proximity_ahead(self) -> float:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_upwards_proximity_to_boundry()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_left_proximity_to_boundry()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_downwards_proximity_to_boundry()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_right_proximity_to_boundry()

### RELATIVE ###
    def get_boundry_proximity_relative_left(self) -> float:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_left_proximity_to_boundry()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_downwards_proximity_to_boundry()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_right_proximity_to_boundry()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_upwards_proximity_to_boundry()

    def get_boundry_proximity_relative_right(self) -> float:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_right_proximity_to_boundry()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_upwards_proximity_to_boundry()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_left_proximity_to_boundry()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_downwards_proximity_to_boundry()

    def get_food_proximity_relative_left(self) -> float:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_left_proximity_to_food()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_downwards_proximity_to_food()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_right_proximity_to_food()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_upwards_proximity_to_food()

    def get_food_proximity_relative_right(self) -> float:
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.UNCHANGED): 
            return -1
        elif Movement.equals(direction, Movement.UP):
            return self.get_right_proximity_to_food()
        elif Movement.equals(direction, Movement.LEFT):
            return self.get_upwards_proximity_to_food()
        elif Movement.equals(direction, Movement.DOWN):
            return self.get_left_proximity_to_food()
        elif Movement.equals(direction, Movement.RIGHT):
            return self.get_downwards_proximity_to_food()



### COORDINATES ###
    def get_nomalized_x_coordinate_food(self) -> float:
        x = self.game.food[0]
        return x / (self.width - 1)

    def get_nomalized_y_coordinate_food(self) -> float:
        y = self.game.food[1]
        return y / (self.height - 1)

    def get_nomalized_x_coordinate_head(self) -> float:
        x = self.game.snake.head()[0]
        return x / (self.width - 1)

    def get_nomalized_y_coordinate_head(self) -> float:
        y = self.game.snake.head()[1]
        return y / (self.height - 1)

### DISTANCE TO FOOD ###
    def get_pythagorean_distance_to_food(self) -> int:
        head = self.game.snake.head()
        food = self.game.food

        distance = (food[0] - head[0])**2 + (food[1] - head[1])**2
        return distance

### INCLUDE TAIL ###
    def get_obstacle_distance_ahead(self) -> float:
        cursor = self.game.snake.head()
        direction = self.game.snake.direction
        boundry_distance = self.get_boundry_distance_ahead()
        obstacle_distance = 0

        for _ in range(boundry_distance):
            cursor = cursor + direction
            if self.game.snake.is_snake_body(cursor, ignore_tail_elemts=1):
                break
            obstacle_distance += 1
        return obstacle_distance
        
    def get_obstacle_proximity_ahead(self) -> float:
        obstacle_distance = self.get_obstacle_distance_ahead()
        direction = self.game.snake.direction
        if Movement.equals(direction, Movement.LEFT) or Movement.equals(direction, Movement.RIGHT):
            return 1.0 - obstacle_distance / self.width
        else:
            return 1.0 - obstacle_distance / self.height
