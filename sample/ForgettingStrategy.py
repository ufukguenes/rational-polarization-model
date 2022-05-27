"""
This module includes forgetting strategies
"""
import random


def simple_minded(agent, new_argument, new_argument_index):
    """
    simple minded forgetting-strategy

    :param agent: agent on which the forgetting strategy will be applied
    :param new_argument: the argument the agent will receive
    :param new_argument_index: the index of the argument in the argument pool, must be known
    :return: no returns, just side effects
    """

    length_before = len(agent)
    agent.update({new_argument_index: new_argument})

    if len(agent) == length_before:  # agent already has this argument, doesn't need to forget another one
        return

    # pick one key/index by random and remove the index, argument pair from its memory
    all_keys = list(agent.keys())
    random_key_index = random.randint(0, len(all_keys) - 1)
    random_key = all_keys[random_key_index]
    agent.pop(random_key)


def weight_minded(agent, new_argument, new_argument_index):
    """
    weight minded forgetting-strategy

    :param agent: agent on which the forgetting strategy will be applied
    :param new_argument: the argument the agent will receive
    :param new_argument_index: the index of the argument in the argument pool, must be known
    :return: no returns, just side effects
    """

    length_before = len(agent)
    agent.update({new_argument_index: new_argument})

    if len(agent) == length_before:  # agent already has this argument
        return

    # convert directory of index, argument pairs to list of pairs
    kv_arguments = list(agent.items())

    # find the overall absolut the weakest argument and the corresponding index
    current_weakest = abs(kv_arguments[0][1])
    current_weakest_index = kv_arguments[0][0]
    for i in range(1, len(kv_arguments)):
        if abs(kv_arguments[i][1]) < current_weakest:
            current_weakest = abs(kv_arguments[i][1])
            current_weakest_index = kv_arguments[i][0]

    # remove the index, argument pair from the memory
    agent.pop(current_weakest_index)


def coherence_minded(agent, new_argument, new_argument_index):
    """
    coherence minded forgetting-strategy

    :param agent: agent on which the forgetting strategy will be applied
    :param new_argument: the argument the agent will receive
    :param new_argument_index: the index of the argument in the argument pool, must be known
    :return: no returns, just side effects
    """

    length_before = len(agent)
    agent.update({new_argument_index: new_argument})

    if len(agent) == length_before:  # agent already has this argument
        return

    # convert directory of index, argument pairs to list of pairs
    kv_arguments = list(agent.items())

    # calculate the current opinion to later decide if a positiv or negativ argument should be forgotten
    current_opinion = new_argument
    for argument in kv_arguments:
        current_opinion += argument[1]

    weakest_positive = 0  # weakest argument which is a positive number
    weakest_positive_index = 0  # index of upper argument
    weakest_negative = 0
    weakest_negative_index = 0

    # find the weakest positive and negative argument
    for i in range(0, len(kv_arguments)):

        if kv_arguments[i][1] < 0 and (kv_arguments[i][1] > weakest_negative or weakest_negative == 0):
            weakest_negative = kv_arguments[i][1]
            weakest_negative_index = kv_arguments[i][0]
            continue
        if kv_arguments[i][1] > 0 and (kv_arguments[i][1] < weakest_positive or weakest_positive == 0):
            weakest_positive = kv_arguments[i][1]
            weakest_positive_index = kv_arguments[i][0]
            continue

    # check which argument should be forgotten
    if current_opinion < 0 and weakest_positive > 0:
        agent.pop(weakest_positive_index)
    elif current_opinion > 0 and weakest_negative < 0:
        agent.pop(weakest_negative_index)
    else:
        if weakest_positive == 0 and weakest_negative != 0:
            agent.pop(weakest_negative_index)
        elif weakest_negative == 0 and weakest_positive !=0:
            agent.pop(weakest_positive_index)
        elif abs(weakest_negative) < abs(weakest_positive):
            agent.pop(weakest_negative_index)
        else:
            agent.pop(weakest_positive_index)
