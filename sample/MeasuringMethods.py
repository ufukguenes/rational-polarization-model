"""
Methods for calculating the measures for the analysis of the agent based simulations and creating plots
"""
import copy

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelmax


def get_average_opinions(agents):
    opinions = []
    for arguments in agents:
        all_values = list(arguments.values())
        current_opinion = 0
        for value in all_values:
            current_opinion += value

        opinions.append(current_opinion)

    return opinions


def get_two_groups_as_opinions(opinions):

    bins = np.digitize(opinions, bins=np.arange(-100, 100, 1))

    bincount = np.bincount(bins)
    maxima = argrelmax(bincount)

    maxima = list(maxima[0])

    maxima.sort()

    group_range = 7

    # pick the boarders for each group,
    split = maxima
    remove = []
    for i in range(len(maxima) - 1):
        if maxima[i+1] - maxima[i] <= group_range:
            remove.append(maxima[i])

    for rem in remove:
        split.remove(rem)

    groups = [] # agents with bins in simmilar range are in one group
    for i in range(len(split)+1):
        groups.append([])

    for i in range(len(bins)):
        in_last = True
        for k in range(len(split)):
            bin = bins[i]
            spl = split[k]
            splmin = spl + group_range
            if bins[i] <= split[k] + group_range: # untere grenze muss man nicht überprüfen, weil sie sonst eh in vorheriger gruppe ist
                groups[k].append(i)
                in_last = False
                break
        if in_last:
            groups[len(split)].append(opinions[i])

    return groups


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


def subgroup_divergence(agents):
    average_opinions = get_average_opinions(agents)

    groups = get_two_groups_as_opinions(average_opinions)

    average_per_group = []
    for group in groups:
        average_per_group.append(np.average(group))

    X, Y = np.meshgrid(average_per_group, average_per_group)

    pairwise_differences = abs(X - Y)

    return pairwise_differences


def subgroup_consensus(agents):
    average_opinions = get_average_opinions(agents)

    groups = get_two_groups_as_opinions(average_opinions)

    std_per_group = []
    for group in groups:
        std_per_group.append(np.std(group))

    return std_per_group


def relative_subgroup_size_differnece(agents):
    average_opinions = get_average_opinions(agents)

    groups = get_two_groups_as_opinions(average_opinions)

    size_per_group = []
    for group in groups:
        size_per_group.append(len(group))

    return size_per_group


def is_converged_average(agents):
    average_opinion = get_average_opinions(agents)
    epsilon = 0.0001
    test_opinion = average_opinion[0]
    for opinion in average_opinion:
        if not abs(test_opinion - opinion) < epsilon:
            return False
    return True


def is_converged_reasons(agents):
    test_agent_keys = list(agents[0].keys())

    for agent in agents:
        comparison_agent_keys = list(agent.keys())
        for argument in agent:
            if argument not in test_agent_keys:
                return False
    return True