import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
import MeasuringMethods as mes

number_of_steps = 100000  # 100.000 in paper
plot_every_n_steps = 10000
plot_when_in = [0, 5, 10, 50, 100, 250, 500, 1000, 2500, 5000, 7500, 10000, 25000, 50000, number_of_steps - 1]

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
    number_of_groups = []
    subgroup_divergence = []
    subgroup_consensus = []
    relative_subgroup_size = []
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

            subgroup_divergence.append(mes.subgroup_divergence_for_two_groups(agents))
            subgroup_consensus.append(mes.subgroup_consensus(agents))
            relative_subgroup_size.append(mes.relative_subgroup_size(agents))
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

            average = mes.get_average_opinions(agents)
            groups_opinion, groups_agent_index = mes.get_groups(average)

            number_of_groups.append(len(groups_opinion))

            group_avg = []
            group_std = []
            for group in groups_opinion:
                group_avg.append(np.average(group))
                group_std.append(np.std(group))

            if converged_average and converged_reasons:
                break

    print("Time to polarize average: ", time_to_polarize_average)
    print("Time to polarize reasons: ", time_to_polarize_reasons)

    subgroup_consensus_avg = list(map(np.average, subgroup_consensus))
    plt.plot(steps, subgroup_consensus_avg, label='average subgroup consensus', marker="o")
    plt.plot(steps, subgroup_divergence, label='subgroup divergence for two groups', marker="o")
    plt.plot(steps, number_of_groups, label='number of groups', marker="o")
    plt.xlabel("num of steps")
    plt.legend()
    plt.show()

    max_num_of_groups = max(map(len, relative_subgroup_size))
    for i in range(len(relative_subgroup_size)):
        while len(relative_subgroup_size[i]) < max_num_of_groups:
            relative_subgroup_size[i].append(0)

    transposed = np.transpose(relative_subgroup_size)
    for group in transposed:
        plt.plot(steps, group, label='subgroup_size', marker="o")
    plt.xlabel("num of steps")
    plt.show()


def transpose(l1, l2):
    # iterate over list l1 to the length of an item
    for i in range(len(l1[0])):
        # print(i)
        row = []
        for item in l1:
            # appending to new list with values and index positions
            # i contains index position and item contains values
            row.append(item[i])
        l2.append(row)
    return l2


if __name__ == '__main__':
    init(number_of_steps, size_of_argument_pool, number_of_agents, size_of_memory,
         argp.exponential_distribution_pool, forg.coherence_minded,
         delib.outside_deliberation)
