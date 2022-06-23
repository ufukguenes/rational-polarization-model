"""
Methods for calculating the measures for the analysis of the agent based simulations and creating plots
"""

import numpy as np


# is stable/ order of indices won't change
def get_average_opinions(agents):
    opinions = []
    for arguments in agents:
        all_values = list(arguments.values())
        opinions.append(sum(all_values))

    return opinions


def find_max_index(values):
    """
    finds the indices of the maxima in the given list

    :@param values: list in which maxima shall be found
    :return: list of indices
    """

    maxima = []

    values = np.insert(values, 0,
                       0)  # am anfang und ende eine 0 einfügen um auch den ersten und letzten wert zu betrachten
    values = np.append(values, 0)
    for i in range(1, len(values) - 1):
        if values[i + 1] < values[i] and values[i - 1] < values[i]:
            maxima.append(i - 1) # -1 weil wir ja gerade künstlich einen wert am anfang hinzugefügt haben
    return maxima


def get_groups(opinions, group_range=7):
    """
    berechnet die gruppen basierend auf maxima. Um ein Maxima werden alle elemente innerhalb der group range zu
    einer Gruppe zusammen gelegt

    :@param opinions: die daten, die grupiert werden sollen
    :@param group_range: die Weite mit der jede Gruppe gebildet werden soll
    :return: Gruppierung nach Meinung und Gruppierung nach Index
    """

    bins = np.digitize(opinions, bins=np.arange(-100, 100, 1))
    bincount = np.bincount(bins)
    maxima = find_max_index(bincount)

    # pick the boarders for each group and remove unnecessary maxima
    split = maxima
    remove = []
    for i in range(len(maxima) - 1):
        if abs(maxima[i + 1] - maxima[i]) <= group_range:
            remove.append(maxima[i])

    for rem in remove:
        split.remove(rem)

    # if no maxima remain, then there is only one group
    if len(split) == 0:
        return [opinions], [list(range(len(opinions)))]

    # finde die gruppen bassierend auf einer Gruppen-weite
    opinions_by_group = []  # agents with bins in similar range are in one group
    index_by_group = []

    for i in range(len(split)):
        opinions_by_group.append([])
        index_by_group.append([])

    not_used_indices = list(range(len(opinions)))

    for i in range(len(bins)):
        for k in range(len(split)):
            if bins[i] <= split[k] + group_range:  # untere grenze muss man nicht überprüfen, weil sie sonst eh in vorheriger gruppe ist
                opinions_by_group[k].append(opinions[i])
                index_by_group[k].append(i)
                not_used_indices.remove(i)
                break

    # alle die die größer als die letzte Gruppe sind, kommen auch in die letzte Gruppe
    for index in not_used_indices:
        opinions_by_group[len(split) - 1].append(opinions[index])
        index_by_group[len(split) - 1].append(index)

    return opinions_by_group, index_by_group


def subgroup_divergence_for_two_groups(opinions_by_group):
    """
    calculates subgroup divergence by assuming there are exactly two groups and calculating the difference in their
    average opinion

    :@param opinions_by_group: the opinions of agents grouped
    :return: difference from average opinions
    """

    if len(opinions_by_group) != 2:
        return 0

    fst_avg = np.average(opinions_by_group[0])
    snd_avg = np.average(opinions_by_group[1])

    return abs(fst_avg - snd_avg)


def subgroup_consensus(opinions_by_group):
    """
    calculates subgroup consensus by calculating the standard deviation of opinions per group

    :@param opinions_by_group: the opinions of agents grouped
    :return: a list of std for each group by opinion
    """

    std_per_group = []
    for group in opinions_by_group:
        std_per_group.append(np.std(group))

    return std_per_group


def relative_subgroup_size(opinions_by_group):
    """
    calculates the subgroup size

    :@param opinions_by_group: the opinions of agents grouped
    :return: size of each subgroup
    """

    size_per_group = []
    for group in opinions_by_group:
        size_per_group.append(len(group))

    return size_per_group


def is_converged_average(opinions_by_group, epsilon=0.00001):
    """
    tests if a group is converged by comparing their average opinions for each group

    :@param opinions_by_group: the opinions of agents grouped
    :@param epsilon: the tolerance for comparing floats
    :return: true if converged, otherwise false
    """
    for i in range(len(opinions_by_group)):
        curr_group = opinions_by_group[i]
        test_opinion = curr_group[0]
        for opinion in curr_group:
            if not abs(test_opinion - opinion) < epsilon:
                return False
    return True


def is_converged_reasons(agents, opinions_by_group, index_by_group):
    """
    tests if a group is converged by comparing their reasons for each group

    :@param agents: the agents to be tested on
    :@param opinions_by_group: the opinions of agents grouped
    :@param index_by_group: the indices of agents grouped
    :return: true if converged, otherwise false
    """

    for i in range(len(opinions_by_group)):
        curr_group_index = index_by_group[i]
        test_index = curr_group_index[0]
        test_agent_keys = list(agents[test_index].keys())

        for index in curr_group_index:
            for argument in agents[index]:
                if argument not in test_agent_keys:
                    return False
    return True
