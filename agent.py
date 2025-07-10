import neat
import pygame

import os
import sys
import time
from datetime import datetime
import configparser

from snake import Movement, Map, Snake, Game
from game_vision import GameVision
import visualize
import checkpoint

NEAT_CONFIG = 'neat-config'

# Map Size
WIDTH = 25
HEIGHT = 12
GAME_SEED = 1

# Constants
CELL_SIZE = 40
SPEED = 50

# Map colors
COLOR_BG = (255, 255, 255)
COLOR_SNAKE = (150, 230, 150)
COLOR_FOOD = (230, 100, 100)
COLOR_GRID = (225, 225, 225)

def is_relative_control_method() -> bool:
    # Create a parser and read the file
    config = configparser.ConfigParser()
    config.read(NEAT_CONFIG)

    # Get num_outputs from the DefaultGenome section
    num_outputs = int(config['DefaultGenome']['num_outputs'])

    print("num_outputs:", num_outputs)

    if (num_outputs == 3): return True
    elif (num_outputs == 5): return False
    else: raise ValueError("num_outputs in the neat config is wrong!")


# Movement control method
RELATIVE_CONTROLS = is_relative_control_method()

class Agent:
    
    def __init__(self, net, game:Game):
        self.net = net
        self.score = 0
        self.game = game
        self.game_vision = GameVision(self.game)
        self.max_score = self.game.map.width * self.game.map.height

    def activate_net(self, inputs):
        output = self.net.activate(inputs)
        return output.index(max(output))

    def relative_to_absolute_movement(self, relative_movement):
        unchanged = 0
        relative_left = 1
        relative_right = 2
        
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

    def get_movement_from_output(self, output, is_relative:bool):
        movement = None
        if not is_relative:
            match output:
                case 0: 
                    movement = Movement.UNCHANGED
                case 1:
                    movement = Movement.UP
                case 2:
                    movement = Movement.LEFT
                case 3:
                    movement = Movement.RIGHT
                case 4:
                    movement = Movement.DOWN
        elif is_relative:
            current_direction = self.game.snake.direction
            match output:
                case 0: 
                    movement = Movement.UNCHANGED
                case 1: # relative left
                    if Movement.equals(current_direction, Movement.UP): movement = Movement.LEFT
                    elif Movement.equals(current_direction, Movement.LEFT): movement = Movement.DOWN
                    elif Movement.equals(current_direction, Movement.DOWN): movement = Movement.RIGHT
                    elif Movement.equals(current_direction, Movement.RIGHT): movement = Movement.UP
                case 2: # relative right
                    if Movement.equals(current_direction, Movement.UP): movement = Movement.RIGHT
                    elif Movement.equals(current_direction, Movement.LEFT): movement = Movement.UP
                    elif Movement.equals(current_direction, Movement.DOWN): movement = Movement.LEFT
                    elif Movement.equals(current_direction, Movement.RIGHT): movement = Movement.DOWN
        return movement

    def move(self) -> bool:
        inputs = self._get_inputs()
        output = self.activate_net(inputs)

        movement = self.get_movement_from_output(output, is_relative=RELATIVE_CONTROLS)

        self.game.evaluate(movement)
        return output > 0 # this means that agent has changed the direction

    def _get_inputs(self):
        inputs = [

            self.game_vision.get_boundry_proximity_ahead(),
            self.game_vision.get_boundry_proximity_relative_left(),
            self.game_vision.get_boundry_proximity_relative_right(),

            self.game_vision.get_food_proximity_ahead(),
            self.game_vision.get_food_proximity_relative_left(),
            self.game_vision.get_food_proximity_relative_right(),

        ]
        return inputs


    def run(self):
        steps = 0
        MAX_STEPS = 1000
        active_movements = 0
        moves_towards_food = 0
        moves_away_from_food = 0
        visited_fields = set()
        while not self.game.game_over:
            
            distance_before_move = self.game_vision.get_pythagorean_distance_to_food()

            moved = self.move()
            active_movements += moved

            distance_after_move = self.game_vision.get_pythagorean_distance_to_food()
            if (distance_after_move > distance_before_move and moved):
                moves_towards_food += 1
            elif (distance_after_move < distance_before_move and moved):
                moves_away_from_food += 1
            
            # exploration bonus
            head = self.game.snake.head()
            field_index = self.get_coordinate_index(head[0], head[1])
            visited_fields.add(field_index)

            steps += 1
            if steps > MAX_STEPS:
                break
        
        # Keep fitness positive
        self.fitness = max(0.0, self.fitness_function(steps, active_movements, visited_fields, moves_towards_food, moves_away_from_food))

    def fitness_function(self, steps, active_movements, visited_fields, moves_towards_food, moves_away_from_food):
        map_size = self.game.map.width * self.game.map.height

        score_bonus = self.game.score / map_size
        exploration_bonus = len(visited_fields) / map_size
        movement_efficency = self.game.score / (active_movements + 0.000001)
        initial_movement_bonus = int(active_movements > 0)
        game_over_penalty = int(self.game.game_over)
        food_approach_balance = moves_towards_food - moves_away_from_food

        return self.game.score + food_approach_balance / 10 - game_over_penalty * 5

    def get_coordinate_index(self, x, y):
        return self.game.map.width * y + x

def eval_genomes(genomes, config):
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        agent = Agent(net, Game(width=WIDTH, height=HEIGHT, random_seed=GAME_SEED))
        agent.run()
        genome.fitness = agent.fitness

    return

def play_with_agent(agent, max_steps=1000, game_speed=SPEED):
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

    pygame.init()

    game = agent.game

    screen_width = game.map.width * CELL_SIZE
    screen_height = game.map.height * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    steps = 0
    while steps < max_steps:
        move = agent.move()

        screen.fill(COLOR_BG)
        draw_grid(screen, game.map)
        draw_snake(screen, game.snake)
        draw_food(screen, game.food)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(game_speed)

        steps += 1
    pygame.quit()

class VisualizeBestAgentReporter(neat.reporting.BaseReporter):
    def __init__(self, config, max_steps=1000, game_speed=SPEED):
        self.config = config
        self.max_steps = max_steps
        self.game_speed = game_speed

    def post_evaluate(self, config, population, species, best_genome):
        net = neat.nn.FeedForwardNetwork.create(best_genome, self.config)
        agent = Agent(net, Game(width=WIDTH, height=HEIGHT, random_seed=GAME_SEED))
        play_with_agent(agent, max_steps=self.max_steps, game_speed=self.game_speed)

def train():
    # Load neat config
    base_dir = os.path.dirname(os.path.abspath(__file__))
    neat_config = os.path.join(base_dir, NEAT_CONFIG)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        neat_config)

    # population
    p = neat.Population(config)

    # For console logging
    p.add_reporter(neat.StdOutReporter(False))

    # Stats-Logger for visalization of the net
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(VisualizeBestAgentReporter(config=config, max_steps=100, game_speed=100))


    # Run until a solution is found.
    winner = p.run(eval_genomes, 100) # up to X generations

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    visualize.draw_net(config=config, genome=winner, filename=f".log/graph/{timestamp}")
    visualize.plot_species(stats, filename=f".log/speciation/{timestamp}.svg")
    visualize.plot_stats(statistics=stats, filename=f".log/avg_fitness/{timestamp}.svg")
    checkpoint.save_genome(genome=winner, filename=f".log/net/{timestamp}.pkl")

    # execute 
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    agent = Agent(net, Game(width=WIDTH, height=HEIGHT))
    play_with_agent(agent, max_steps=10000)

if __name__ == '__main__':
    train()