"""
Playing Ping Pong using a feed-forward neural network.
"""

import multiprocessing
import os
import pickle
import numpy as np
import neat
import random

from ping_pong_ai.ping_pong import PongPin

runs_per_net = 5


def get_move(outputs):
    """Returns index for max value or random index from biggest values"""
    c_max = np.max(outputs)
    res = [i for i, o in enumerate(outputs) if o >= c_max]
    return random.choice(res)


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitnesses = []
    for runs in range(runs_per_net):
        # Initiate ping pong with matrix size
        pong = PongPin((15, 20))

        # Run the given simulation for up to num_steps time steps.
        fitness = 0
        run_game = True
        cnt = 0
        while run_game:
            inputs = list(pong.ball) + pong.racquet_1 + [pong.ball_dir]
            action = net.activate(inputs)
            # Get action for the racquet_1
            force = get_move(action)
            pong.move(force)
            pong.robot_play()
            reward = pong.collide()
            pong.ball_move()
            pong.render_matrix()
            run_game = pong.check_alive()
            cnt += 1
            fitness += reward * 0.1
            if cnt == 6000:
                run_game = False
        fitnesses.append(fitness)
    min_fit = min(fitnesses)
    if min_fit > 60:
        with open(f'pkl/pong_{round(min_fit, 1)}', 'wb') as f:
            pickle.dump(net, f)
        with open(f'pkl/pong_genome{round(min_fit, 1)}', 'wb') as f:
            pickle.dump(genome, f)
    # The genome's fitness is its worst performance across all runs.
    return min_fit


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.getcwd()
    config_path = os.path.join(local_dir, 'config-feedforward')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    best_w = pop.run(pe.evaluate)
    winner = neat.nn.FeedForwardNetwork.create(best_w, config)

    # Save the winner.
    with open('pkl/winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(best_w)


if __name__ == '__main__':
    run()
