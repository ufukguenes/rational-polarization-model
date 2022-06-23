import matplotlib.pyplot as plt
import numpy as np

import MeasuringMethods as mes
import Statistics as stat


def init(number_of_arguments, number_of_agents, size_of_memory, distribution):
    # TODO bei unlimeted memory, hat jeder dann alle argumente?
    '''
    for k in range(size_of_memory):
        random_index = random.randint(0, size_of_argument_pool - 1)
        next_argument = argument_pool[random_index]
        arguments_of_one.append((random_index, next_argument))
    '''

    # init all the available arguments
    argument_pool = distribution(number_of_arguments)
    agents = []

    # give each agent random arguments
    for i in range(number_of_agents):
        arguments_of_one = []

        # permutiere alle indizes der Argumente, um die ersten size_memory vielen indizes herrauszunehmen.
        random_indices_permutation = np.random.permutation(number_of_arguments)
        indices_to_take = list(range(0, size_of_memory))
        indices_of_one = np.take(random_indices_permutation, indices_to_take).tolist()

        # bilde aus den permutierten Indizes paare der form (Index, Argument)
        for index in indices_of_one:
            arguments_of_one.append((index, argument_pool[index]))

        # füge die Index, Argument paare in eine HashMap/ Directory ein
        argument_dictionary = dict(arguments_of_one)
        agents.append(argument_dictionary)

    return agents, argument_pool


def do_n_steps(number_of_steps, argument_pool, agents, forgetting, deliberation):
    # je ein Schritt der Simulation
    agents_for_next_step = agents
    for i in range(number_of_steps):
        # hier wird die deliberation-Strategie und die Vergessens-Strategie angewandt
        agents_for_next_step, argument_pool = deliberation(agents_for_next_step, argument_pool, forgetting)

    return agents_for_next_step, argument_pool


def standard_set_up(distribution, forgetting, deliberation, max_steps=100000, size_of_argument_pool=500,
                       count_of_agents=50, count_of_memory=7):
    stats_every_n_steps = 1000
    stats_when_in = [5, 10, 50, 100, 150, 200, 250, 300, 400, 500, max_steps - 1]

    stats = stat.Statistics()

    agents_for_next_step, argument_pool = init(size_of_argument_pool, count_of_agents, count_of_memory,
                                               distribution)
    stats.calculate(agents_for_next_step, 0)
    stats.plot_average_opinion()

    for i in range(max_steps):
        agents_for_next_step, argument_pool = do_n_steps(1, argument_pool, agents_for_next_step, forgetting,
                                                         deliberation)

        if (i+1) % stats_every_n_steps == 0 or (i+1) in stats_when_in:
            stats.calculate(agents_for_next_step, i)
            stats.plot_average_opinion()
            if stats.has_converged():
                break

    stats.plot_general_stats()


