import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
import MeasuringMethods as mes

number_of_steps = 100000  # 100.000 in paper
plot_every_n_steps = 10000
plot_when_in = [0, 5, 10, 50, 100, 250, 500, 1000, 10000, 25000, 50000, number_of_steps - 1]

size_of_argument_pool = 500  # 500 in paper

scale_parameter_exp_distri = 1  # 1 in paper

number_of_agents = 50  # 50 in paper
size_of_memory = 7  # 7 or unlimited in paper


def init(num_steps, num_arguments, num_agents, size_memory, distribution, forgetting, deliberation):
    # init all the available arguments
    argument_pool = distribution(size_of_argument_pool)

    agents = []

    # give each agent random arguments
    for i in range(num_agents):
        arguments_of_one = []

        # TODO bei unlimeted memory, hat jeder dann alle argumente?
        '''
        for k in range(size_of_memory):
            random_index = random.randint(0, size_of_argument_pool - 1)
            next_argument = argument_pool[random_index]
            arguments_of_one.append((random_index, next_argument))
        '''

        # permutiere alle indizes der Argumente, um die ersten size_memory vielen indizes herrauszunehmen.
        random_indices_permutation = np.random.permutation(num_arguments)
        indices_to_take = list(range(0, size_of_memory))
        indices_of_one = np.take(random_indices_permutation, indices_to_take).tolist()

        # bilde aus den permutierten Indizes paare der form (Index, Argument)
        for index in indices_of_one:
            arguments_of_one.append((index, argument_pool[index]))

        # füge die Index, Argument paare in eine HashMap/ Directory ein
        argument_dictionary = dict(arguments_of_one)
        agents.append(argument_dictionary)

    # je ein Schritt der Simulation
    std = []
    steps = []
    subgroup_divergence = []
    subgroup_consensus = []
    relative_subgroup_size_diff = []
    time_to_polarize_average = [0, 0]
    time_to_polarize_reasons = [0, 0]
    converged_average = False
    converged_reasons = False
    for i in range(num_steps):
        # hier wird die deliberation-Strategie und die Vergessens-Strategie angewandt
        deliberation(agents, argument_pool, forgetting)

        # Ergebnisse plotten
        if i % plot_every_n_steps == 0 or i in plot_when_in:

            mes.opinion_of_each_agent(agents, i)
            plt.show()

            subgroup_divergence.append(mes.subgroup_divergence(agents))
            subgroup_consensus.append(mes.subgroup_consensus(agents))
            relative_subgroup_size_diff.append(mes.relative_subgroup_size_differnece(agents))
            steps.append(i)

            if converged_average:
                continue
            elif mes.is_converged_average(agents):
                time_to_polarize_average[1] = i
                converged_average = True
            else:
                time_to_polarize_average[0] = i

            if converged_reasons:
                continue
            elif mes.is_converged_reasons(agents):
                time_to_polarize_reasons[1] = i
                converged_reasons = True
            else:
                time_to_polarize_reasons[0] = i

    plt.plot(steps, subgroup_consensus, label='consensus')
    plt.plot(steps, subgroup_divergence, label='divergence')
    plt.plot(steps, relative_subgroup_size_diff, label='subgroup_size')
    plt.xlabel("num of steps")
    plt.legend()
    plt.show()

    print("Time to polarize average: ", time_to_polarize_average)
    print("Time to polarize reasons: ", time_to_polarize_reasons)


if __name__ == '__main__':
    init(number_of_steps, size_of_argument_pool, number_of_agents, size_of_memory,
         argp.exponential_distribution_pool, forg.coherence_minded,
         delib.outside_deliberation)
