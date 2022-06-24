"""
This module contains functions which represent the group interaction methods, these methods should also
call the forgetting strategies
"""
import random


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