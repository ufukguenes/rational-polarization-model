import matplotlib.pyplot as plt
import numpy as np

import MeasuringMethods as mes


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


def statistical_set_up(distribution, forgetting, deliberation, runs=10, max_steps=100000, size_of_argument_pool=500, count_of_agents=50, count_of_memory=7):
    stats_every_n_steps = 1000
    stats_when_in = [0, 5, 10, 50, 100, 150, 200, 250, 300, 400, 500, max_steps - 1]
    all_steps = []
    all_number_of_groups = []
    all_subgroup_divergence = []
    all_subgroup_consensus = []
    all_relative_subgroup_size = []
    all_time_to_polarize_average = []
    all_time_to_polarize_reasons = []



    for k in range(runs):
        print("run started: " + str(k))
        steps = []
        number_of_groups = []
        subgroup_divergence = []
        subgroup_consensus = []
        relative_subgroup_size = []
        time_to_polarize_average = [0, 0]
        time_to_polarize_reasons = [0, 0]
        converged_average = False
        converged_reasons = False

        agents_for_next_step, argument_pool = init(size_of_argument_pool, count_of_agents, count_of_memory,
                                                   distribution)
        for i in range(max_steps):
            agents_for_next_step, argument_pool = do_n_steps(1, argument_pool, agents_for_next_step, forgetting,
                                                     deliberation)

            if i % stats_every_n_steps == 0 or i in stats_when_in:

                average_opinion = mes.get_average_opinions(agents_for_next_step)
                opinions_by_group, index_by_group = mes.get_groups(average_opinion)


                subgroup_divergence.append(mes.subgroup_divergence_for_two_groups(opinions_by_group))
                subgroup_consensus.append(mes.subgroup_consensus(opinions_by_group))
                relative_subgroup_size.append(mes.relative_subgroup_size(opinions_by_group))
                steps.append(i)

                if converged_average:
                    continue
                elif mes.is_converged_average(opinions_by_group):
                    time_to_polarize_average[1] = i
                    converged_average = True
                else:
                    time_to_polarize_average[0] = i

                if converged_reasons:
                    continue
                elif mes.is_converged_reasons(agents_for_next_step, opinions_by_group, index_by_group):
                    time_to_polarize_reasons[1] = i
                    converged_reasons = True
                else:
                    time_to_polarize_reasons[0] = i

                number_of_groups.append(len(opinions_by_group))

                if converged_average and converged_reasons:
                    break

        all_steps.append(steps)
        all_number_of_groups.append(number_of_groups)
        all_subgroup_divergence.append(subgroup_divergence)
        all_subgroup_consensus.append(subgroup_consensus)
        all_relative_subgroup_size.append(relative_subgroup_size)
        all_time_to_polarize_average.append(time_to_polarize_average[1])
        all_time_to_polarize_reasons.append(time_to_polarize_reasons[1])



def standard_set_up(distribution, forgetting, deliberation, max_steps=100000, size_of_argument_pool=500, count_of_agents=50, count_of_memory=7):
    plot_every_n_steps = 10000
    plot_when_in = [0, 5, 10, 50, 100, 150, 200, 250, 300, 400, 500, 1000, 2500, 5000, 7500, 10000, 25000, 50000,
                    max_steps - 1]

    # je ein Schritt der Simulation
    steps = []
    number_of_groups = []
    subgroup_divergence = []
    subgroup_consensus = []
    relative_subgroup_size = []
    time_to_polarize_average = [0, 0]
    time_to_polarize_reasons = [0, 0]
    converged_average = False
    converged_reasons = False

    agents_for_next_step, argument_pool = init(size_of_argument_pool, count_of_agents, count_of_memory,
                                               distribution)

    for i in range(max_steps):
        # hier wird die deliberation-Strategie und die Vergessens-Strategie angewandt
        agents_for_next_step, argument_pool = do_n_steps(1, argument_pool, agents_for_next_step, forgetting,
                                                         deliberation)

        # Ergebnisse plotten
        if i % plot_every_n_steps == 0 or i in plot_when_in:

            average_opinion = mes.get_average_opinions(agents_for_next_step)
            opinions_by_group, index_by_group = mes.get_groups(average_opinion)

            lower = min(-24, round(min(average_opinion)) - 5)
            upper = max(24, round(max(average_opinion)) + 5)
            width = 2

            plt.hist(average_opinion, bins=range(lower, upper, width))
            plt.title("Opinions after " + str(i) + " steps")
            plt.xlabel("opinion")
            plt.ylabel("number of agents")

            plt.show()

            subgroup_divergence.append(mes.subgroup_divergence_for_two_groups(opinions_by_group))
            subgroup_consensus.append(mes.subgroup_consensus(opinions_by_group))
            relative_subgroup_size.append(mes.relative_subgroup_size(opinions_by_group))
            steps.append(i)

            if converged_average:
                continue
            elif mes.is_converged_average(opinions_by_group):
                time_to_polarize_average[1] = i
                converged_average = True
            else:
                time_to_polarize_average[0] = i

            if converged_reasons:
                continue
            elif mes.is_converged_reasons(agents_for_next_step, opinions_by_group, index_by_group):
                time_to_polarize_reasons[1] = i
                converged_reasons = True
            else:
                time_to_polarize_reasons[0] = i

            number_of_groups.append(len(opinions_by_group))

            if converged_average and converged_reasons:
                break

    # Ergebnisse plotten
    print("Time to polarize average: ", time_to_polarize_average)
    print("Time to polarize reasons: ", time_to_polarize_reasons)

    subgroup_consensus_avg = list(map(np.average, subgroup_consensus))
    plt.plot(steps, subgroup_consensus_avg, label='average subgroup consensus', marker="o")
    plt.plot(steps, subgroup_divergence, label='subgroup divergence for two groups', marker="o")
    plt.plot(steps, number_of_groups, label='number of groups', marker="o")
    plt.xlabel("num of steps")
    plt.title("General stats after model converged")
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
    plt.title("Number of groups after model converged")
    plt.show()
