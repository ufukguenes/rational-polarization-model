"""
Methods for calculating the measures for the analysis of the agent based simulations
"""

def opinion_of_each_agent(agents):
    """
    calculates the sum of all weights for each agent in the list

    :param agents: the agents for which the opinion will be calculated
    :return: a list of opinions/ doubles in the same order the agents where provided
    """
    opinions = []
    for arguments in agents:
        all_values = list(arguments.values())
        current_opinion = 0
        for value in all_values:
            current_opinion += value

        opinions.append(current_opinion)

    return opinions
