"""
This module contains functions which represent the group interaction methods, these methods should also
call the forgetting strategies
"""
import random

import numpy as np

import MeasuringMethods as mes


def pure_deliberation(agents, argument_pool, forgetting_strategy):
    """
    group interaction method based on pure deliberation

    :param agents: the agents which are together in a discussion
    :param argument_pool: the pool of arguments from which an outside argument will be chosen
    :param forgetting_strategy: the strategy which will be used for forgetting
    :return: new agents and the same argument pool
    """

    # pick a random agent
    random_agent_index = random.randint(0, len(agents) - 1)

    # pick a random index and with that an argument of that agent
    all_keys = list(agents[random_agent_index].keys())
    random_key_index = random.randint(0, len(all_keys) - 1)
    random_key = all_keys[random_key_index]
    random_argument = agents[random_agent_index].get(random_key)

    return_agents = []
    # apply the forgetting strategy on each agent with the random argument
    for agent in agents:
        return_agents.append(forgetting_strategy(agent, random_argument, random_key))

    return return_agents, argument_pool


# returns "size of agents"-many arguments in a list, needs pure deliberation afterwards
def outside_deliberation(agents, argument_pool, forgetting_strategy):
    """
    group interaction method based on outside deliberation

    :param agents: the agents which are together in a discussion
    :param argument_pool: the pool of arguments from which an outside argument will be chosen
    :param forgetting_strategy: the strategy which will be used for forgetting
    :return: new agents and the same argument pool
    """

    # pick a new possibly different and new outside argument for each agent
    pure_deliberation_agents = []
    for i in range(len(agents)):
        random_argument_index = random.randint(0, len(argument_pool) - 1)
        pure_deliberation_agents.append(
            forgetting_strategy(agents[i], argument_pool[random_argument_index], random_argument_index))

    # second pure deliberation is applied
    return_agents, argument_pool = pure_deliberation(pure_deliberation_agents, argument_pool, forgetting_strategy)

    return return_agents, argument_pool

def rational_deliberation(agents, argument_pool, forgetting_strategy):
    # pick a random agent
    random_agent_index = random.randint(0, len(agents) - 1)
    random_agent_arguments = list(agents[random_agent_index].values())
    random_agent_opinion = np.average(random_agent_arguments)

    agents_with_opposite_view = list(filter(lambda a: np.average(list(a.values()))*random_agent_opinion < 0, agents))
    if len(agents_with_opposite_view) == 0:
        return pure_deliberation(agents, argument_pool, forgetting_strategy)

    current_max_argument_index = -1
    current_max_difference = 0
    avg_opinion_before = np.average(mes.get_average_opinions(agents_with_opposite_view))
    for argument_index in agents[random_agent_index]:
        current_agents = []
        if argument_pool[argument_index] * random_agent_opinion < 0:
            continue
        for i in range(len(agents_with_opposite_view)):
            current_agents.append(forgetting_strategy(agents_with_opposite_view[i], argument_pool[argument_index], argument_index))
        current_avg_opinion = np.average(mes.get_average_opinions(current_agents))
        if abs(avg_opinion_before - current_avg_opinion) > current_max_difference:
            current_max_argument_index = argument_index
            current_max_difference = abs(random_agent_opinion - current_avg_opinion)

    if current_max_argument_index < 0:
        return agents, argument_pool

    return_agents = []
    for agent in agents:
        return_agents.append(forgetting_strategy(agent, argument_pool[current_max_argument_index], current_max_argument_index))

    return return_agents, argument_pool

def rational_deliberation_simple(agents, argument_pool, forgetting_strategy):
    # pick a random agent
    random_agent_index = random.randint(0, len(agents) - 1)
    random_agent_arguments = list(agents[random_agent_index].values())
    random_agent_opinion = np.average(random_agent_arguments)

    current_max_index = 0
    for opinion in agents[random_agent_index]:
        if argument_pool[opinion] * random_agent_opinion > 0 and abs(argument_pool[current_max_index]) < abs(argument_pool[opinion]):
            current_max_index = opinion

    return_agents = []
    # apply the forgetting strategy on each agent with the random argument
    for agent in agents:
        return_agents.append(forgetting_strategy(agent, argument_pool[current_max_index], current_max_index))

    return return_agents, argument_pool
