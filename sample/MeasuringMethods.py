"""
Methods for calculating the measures for the analysis of the agent based simulations and creating plots
"""
import copy

import matplotlib.pyplot as plt
import numpy as np


def get_average_opinions(agents):
    opinions = []
    for arguments in agents:
        all_values = list(arguments.values())
        current_opinion = 0
        for value in all_values:
            current_opinion += value

        opinions.append(current_opinion)

    return opinions


def find_max_index(values):
    maxima = []

    values = np.insert(values, 0, 0) # am anfang und ende eine 0 einfügen um auch den ersten und letzten wert zu betrachten
    values = np.append(values, 0)
    for i in range(1, len(values)-1):
        if values[i+1] < values[i] and values[i-1] < values[i]:
            maxima.append(i)
    return maxima


def get_groups(opinions):

    bins = np.digitize(opinions, bins=np.arange(-100, 100, 1))
    bincount = np.bincount(bins)
    maxima = find_max_index(bincount)
    group_range = 7

    # pick the boarders for each group,
    split = maxima
    remove = []
    for i in range(len(maxima) - 1):
        if abs(maxima[i+1] - maxima[i]) <= group_range:
            remove.append(maxima[i])

    for rem in remove:
        split.remove(rem)

    if len(split) == 0:
        return [opinions], [list(range(len(opinions)))]

    groups_opinion = [] # agents with bins in simmilar range are in one group
    groups_agent_index = []

    for i in range(len(split)):
        groups_opinion.append([])
        groups_agent_index.append([])

    not_used_indices = list(range(len(opinions)))

    for i in range(len(bins)):
        in_last = True
        for k in range(len(split)):
            bin = bins[i]
            curr = split[k]
            currplus = curr + group_range
            if bins[i] <= split[k] + group_range: # untere grenze muss man nicht überprüfen, weil sie sonst eh in vorheriger gruppe ist
                groups_opinion[k].append(opinions[i])
                groups_agent_index[k].append(i)
                not_used_indices.remove(i)
                in_last = False
                break

    for index in not_used_indices:
        groups_opinion[len(split) - 1].append(opinions[index])
        groups_agent_index[len(split) - 1].append(index)

    return groups_opinion, groups_agent_index


def opinion_of_each_agent(agents, steps):
    """
    calculates the sum of all weights for each agent in the list

    :param agents: the agents for which the opinion will be calculated
    :param steps: iteration of the model; to display the iteration step in the graph
    :return: a list of opinions/ doubles in the same order the agents where provided
    """

    opinions = get_average_opinions(agents)

    lower = min(-24, round(min(opinions))-5)
    upper = max(24, round(max(opinions))+5)
    width = 2

    plt.hist(opinions, bins=range(lower, upper, width))
    plt.title("Opinions after " + str(steps) + " steps")
    plt.xlabel("opinion")
    plt.ylabel("number of agents")


def standard_dev(agents):
    average_opinion = get_average_opinions(agents)
    std = np.std(average_opinion)
    return std


def subgroup_divergence_for_two_groups(agents):
    average_opinions = get_average_opinions(agents)

    groups_opinion, groups_agent_index = get_groups(average_opinions)

    if len(groups_opinion) != 2:
        return 0

    fst_avg = np.average(groups_opinion[0])
    snd_avg = np.average(groups_opinion[1])

    return abs(fst_avg - snd_avg)


def subgroup_consensus(agents):
    average_opinions = get_average_opinions(agents)

    groups_opinion, groups_agent_index = get_groups(average_opinions)

    std_per_group = []
    for group in groups_opinion:
        std_per_group.append(np.std(group))

    return std_per_group


def relative_subgroup_size(agents):
    average_opinions = get_average_opinions(agents)

    groups_opinion, groups_agent_index = get_groups(average_opinions)

    size_per_group = []
    for group in groups_opinion:
        size_per_group.append(len(group))

    return size_per_group


def is_converged_average(agents):
    average_opinion = get_average_opinions(agents)
    epsilon = 0.001

    groups_opinion, groups_agent_index = get_groups(average_opinion)

    for i in range(len(groups_opinion)):
        curr_group = groups_opinion[i]
        test_opinion = curr_group[0]
        for opinion in curr_group:
            if not abs(test_opinion - opinion) < epsilon:
                return False
    return True


def is_converged_reasons(agents):
    average_opinion = get_average_opinions(agents)
    groups_opinion, groups_agent_index = get_groups(average_opinion)

    for i in range(len(groups_opinion)):
        curr_group_opinion = groups_opinion[i]
        curr_group_index = groups_agent_index[i]
        start_index = curr_group_index[0]
        test_agent_keys = list(agents[start_index].keys())

        for index in curr_group_index:
            for argument in agents[index]:
                if argument not in test_agent_keys:
                    return False
    return True
