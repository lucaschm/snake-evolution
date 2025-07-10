import neat

import os

import checkpoint
from agent import Agent, play_with_agent
from snake import Game

NEAT_CONFIG = 'neat-config'
WIDTH = 25
HEIGHT = 12
SPEED = 100

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    neat_config = os.path.join(base_dir, NEAT_CONFIG)
    config = neat.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction, 
        neat.DefaultSpeciesSet, 
        neat.DefaultStagnation, 
        neat_config
    )

    net = checkpoint.load_net(config, filename=".log/net/20250710_213704.pkl")

    game = Game(width=WIDTH, height=HEIGHT)
    agent = Agent(net, game)
    play_with_agent(agent, max_steps=10000, game_speed=SPEED)

if __name__ == '__main__':
    main()