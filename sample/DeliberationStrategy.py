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
    :return: no returns, just side effects
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

    return return_agents


# returns "size of agents"-many arguments in a list, needs pure deliberation afterwards
def outside_deliberation(agents, argument_pool, forgetting_strategy):
    """
    group interaction method based on outside deliberation

    :param agents: the agents which are together in a discussion
    :param argument_pool: the pool of arguments from which an outside argument will be chosen
    :param forgetting_strategy: the strategy which will be used for forgetting
    :return: no returns, just side effects
    """

    # pick a new possibly different and new outside argument for each agent
    new_arguments = []
    new_argument_indices = []
    for i in range(len(agents)):
        random_argument_index = random.randint(0, len(argument_pool) - 1)
        new_arguments.append(argument_pool[random_argument_index])
        new_argument_indices.append(random_argument_index)

    pure_deliberation_agents = []
    # first each agent applies its forgetting strategy on the outside argument
    for i in range(len(agents)):
        pure_deliberation_agents.append(forgetting_strategy(agents[i], new_arguments[i], new_argument_indices[i]))

    # second pure deliberation is applied
    return_agents = pure_deliberation(agents, argument_pool, forgetting_strategy)

    return return_agents

    '''
    wenn ein agent eine argument bekommt, dass er noch nicht kennt, erhöht sich die anzahl seiner argumente.
    wenn er dann weiter zu pure deliberation gegeben wird, wird dieser auch wieder mit der erhöten anzhal an
    argumenten zurückgegeben und hatte im pure deliberation step zwei argumente mehr als am anfang
    oder muss ih die vergessens strategie zweimal anwenden bei outside deliberation
    wenn es zweimal angewendet wird, wass wenn man dann unterschiedliche strategien verwendet
    '''
