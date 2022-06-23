import matplotlib.pyplot as plt
import numpy as np

import Statistics


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
    plot_every_n_steps = 1000
    plot_when_in = [5, 10, 50, 100, 150, 200, 250, 300, 400, 500, max_steps - 1]

    stats = Statistics.Statistics()

    agents_for_next_step, argument_pool = init(size_of_argument_pool, count_of_agents, count_of_memory,
                                               distribution)
    stats.calculate(agents_for_next_step, 0)
    stats.create_plot_average_opinion()
    plt.show()
    break_in_next_test = False

    for i in range(max_steps):
        agents_for_next_step, argument_pool = do_n_steps(1, argument_pool, agents_for_next_step, forgetting,
                                                         deliberation)

        if (i + 1) % plot_every_n_steps == 0 or (i + 1) in plot_when_in:
            stats.calculate(agents_for_next_step, i + 1)
            stats.create_plot_average_opinion()
            plt.show()
            if break_in_next_test:
                break

            if stats.has_converged():
                break_in_next_test = True
            else:
                break_in_next_test = False

    stats.create_plot_general_stats()
    plt.show()
    stats.create_plot_relative_group_size()
    plt.show()


def statistical_set_up(distribution, forgetting, deliberation, max_steps=100000, size_of_argument_pool=500,
                       count_of_agents=50, count_of_memory=7, runs=10):
    stats_every_n_steps = 1000
    stats_when_in = [5, 10, 50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, max_steps - 1]
    all_stats = []


    for k in range(runs):
        print("current run: " + str(k))
        break_in_next_test = False
        all_stats.append(Statistics.Statistics())

        agents_for_next_step, argument_pool = init(size_of_argument_pool, count_of_agents, count_of_memory,
                                                   distribution)
        all_stats[k].calculate(agents_for_next_step, 0)
        for i in range(max_steps):

            agents_for_next_step, argument_pool = do_n_steps(1, argument_pool, agents_for_next_step, forgetting,
                                                             deliberation)

            if (i + 1) % stats_every_n_steps == 0 or (i + 1) in stats_when_in:
                all_stats[k].calculate(agents_for_next_step, i + 1)

                if break_in_next_test:
                    break

                if all_stats[k].has_converged():
                    break_in_next_test = True
                else:
                    break_in_next_test = False



    # nur Statistiken zum anzeigen
    for stat in all_stats:
        stat.plot_subgroup_consensus()
    plt.show()

    for stat in all_stats:
        stat.create_plot_subgroup_divergence()
    plt.show()

    for stat in all_stats:
        stat.create_plot_number_of_groups()
    plt.show()

    # average stat at the end
    all_subgroup_divergence = 0
    all_subgroup_consensus = 0
    all_subgroup_size_biggest = 0
    all_max_step_avg = 0
    all_min_step_avg = 0
    all_max_step_res = 0
    all_min_step_res = 0
    relative_number_of_converged_runs_avg = len(all_stats)
    relative_number_of_converged_runs_res = len(all_stats)
    relative_number_of_groups_one = 0
    relative_number_of_groups_two = 0
    relative_number_of_groups_more = 0
    current_plot = 0

    for stat in all_stats:
        current_plot += 1
        index = stat.max_index
        all_subgroup_divergence += stat.subgroup_divergence[index]
        all_subgroup_consensus += list(map(np.average, stat.subgroup_consensus))[index]
        all_subgroup_size_biggest += max(stat.relative_subgroup_size[index])
        all_max_step_avg += stat.time_to_polarize_average[1]
        all_min_step_avg += stat.time_to_polarize_average[0]
        all_max_step_res += stat.time_to_polarize_reasons[1]
        all_min_step_res += stat.time_to_polarize_reasons[0]

        if stat.time_to_polarize_average[1] == 0:
            relative_number_of_converged_runs_avg -= 1

        if stat.time_to_polarize_reasons[1] == 0:
            relative_number_of_converged_runs_res -= 1

        if stat.number_of_groups[index] == 1:
            relative_number_of_groups_one += 1
        if stat.number_of_groups[index] == 2:
            relative_number_of_groups_two += 1
        if stat.number_of_groups[index] > 2:
            relative_number_of_groups_more += 1
            stat.create_plot_average_opinion()
            plt.title("plot num: " + str(current_plot))
            plt.show()

    stat_size = len(all_stats)
    all_subgroup_divergence = all_subgroup_divergence / stat_size
    all_subgroup_consensus = all_subgroup_consensus / stat_size
    all_subgroup_size_biggest = all_subgroup_size_biggest / stat_size
    all_max_step_avg = all_max_step_avg / stat_size
    all_min_step_avg = all_min_step_avg / stat_size
    all_max_step_res = all_max_step_res / stat_size
    all_min_step_res = all_min_step_res / stat_size
    relative_number_of_converged_runs_avg = relative_number_of_converged_runs_avg / stat_size
    relative_number_of_converged_runs_res = relative_number_of_converged_runs_res / stat_size
    relative_number_of_groups_one = relative_number_of_groups_one / stat_size
    relative_number_of_groups_two = relative_number_of_groups_two / stat_size
    relative_number_of_groups_more = relative_number_of_groups_more / stat_size

    print("average subgroup divergence: " + str(all_subgroup_divergence))
    print("average subgroup consensus: " + str(all_subgroup_consensus))
    print("average subgroup largest size: " + str(all_subgroup_size_biggest))
    print("average time to converge on opinion:  min:" + str(all_min_step_avg) + " max: " + str(all_max_step_avg))
    print("average time to converge on reasons:  min:" + str(all_min_step_res) + " max: " + str(all_max_step_res))
    print("relative number of runs which converged on opinions, in %: " + str(relative_number_of_converged_runs_avg*100))
    print("relative number of runs which converged on reasons, in %: " + str(relative_number_of_converged_runs_res*100))
    print("relative number of runs which ended in one group, in %: " + str(relative_number_of_groups_one*100))
    print("relative number of runs which ended in two groups, in %: " + str(relative_number_of_groups_two*100))
    print("relative number of runs which ended in more then two groups, in %: " + str(relative_number_of_groups_more*100))
