import neat
import matplotlib.pyplot as plt

import os

import checkpoint
from agent import Agent, play_with_agent
from snake import Game

CHECKPOINT_NAME = "20250803_194949"
CHECKPOINT_FILE = f".log/net/{CHECKPOINT_NAME}.pkl"
NEAT_CONFIG = 'neat-config'
WIDTH = 25
HEIGHT = 12
SEED = None
SPEED = 100

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    neat_config = os.path.join(base_dir, NEAT_CONFIG)
    config = neat.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction, 
        neat.DefaultSpeciesSet, 
        neat.DefaultStagnation, 
        neat_config
    )
    return config

def save_scores(scores, filename):
    with open(filename, 'w') as f:
        for score in scores:
            f.write(f"{score}\n")

def load_scores(filename):
    with open(filename, 'r') as f:
        scores = [int(line.strip()) for line in f]
    return scores

def play(net, seed):
    game = Game(width=WIDTH, height=HEIGHT, random_seed=seed)
    agent = Agent(net, game)
    score = play_with_agent(agent, max_steps=10000, game_speed=SPEED)
    return score


def plot_scores_over_seeds(scores, view=False, filename='scores_over_seeds.svg'):
    fig = plt.figure()
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    seed = range(len(scores))

    plt.plot(seed, scores, 'b.', label="score")


    fig.suptitle("Scores over seeds", fontsize=16)
    # Figure subtitle
    fig.text(0.5, 0.9, f"", horizontalalignment="center")

    plt.xlabel("Seeds")
    plt.ylabel("Score")
    plt.grid()
    plt.legend()

    plt.savefig(filename)
    if view:
        plt.show()

    plt.close()

def test_multiple_seeds(seeds):
    config = load_config()
    net = checkpoint.load_net(config, filename=CHECKPOINT_FILE)

    scores = []
    for seed in seeds:
        print(f"Seed: {seed}")
        score = play(net,seed)
        scores.append(score)

    save_scores(scores, f"plots/scores_over_seeds/{CHECKPOINT_NAME}.txt")
    scores = None
    scores = load_scores(f"plots/scores_over_seeds/{CHECKPOINT_NAME}.txt")
    plot_scores_over_seeds(scores, filename=f"plots/scores_over_seeds/{CHECKPOINT_NAME}.svg")

def main():
    config = load_config()
    net = checkpoint.load_net(config, filename=CHECKPOINT_FILE)
    play(net, SEED)

if __name__ == '__main__':
    test_multiple_seeds(range(0,50))