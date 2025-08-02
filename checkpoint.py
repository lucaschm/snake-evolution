import neat

import pickle

def save_genome(genome, filename):
    with open(filename, "wb") as f:
        pickle.dump(genome, f)
    print(f"Genome saved to: {filename}")

def load_genome(filename):
    with open(filename, "rb") as f:
        genome = pickle.load(f)
    return genome

def build_net_from_genome(genome, config):
    return neat.nn.FeedForwardNetwork.create(genome, config)

def load_net(config, filename):
    genome = load_genome(filename)
    return build_net_from_genome(genome, config)