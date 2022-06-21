"""
random distribution functions for generating a set of arguments
"""
import random
import numpy as np


def exponential_distribution_pool(number_of_arguments, scale_parameter=1):
    """
    distribution for the weights of the arguments in the pool

    :param scale_parameter: scale parameter = 1 / rate parameter = 1/lambda, mean = 1/ lambda
    :param number_of_arguments: number of arguments that will be generated
    :return: a pool of exponentialy distributed values/ argument-weights
    """
    argument_pool = []

    for i in range(number_of_arguments):
        argument = 0
        while argument == 0:  # no argument can be 0
            pos_or_neg = random.randint(1, 2)
            argument = pow(-1, pos_or_neg) * np.random.exponential(scale_parameter)

        argument_pool.append(argument)

    return argument_pool
