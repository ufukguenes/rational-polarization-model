import matplotlib.pyplot as plt
import numpy as np

import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
import MeasuringMethods as mes

number_of_steps = 100000  # 100.000 in paper
plot_every_n_steps = 10000
plot_when_in = [0, 5, 10, 50, 100, 250, 500, 1000, 10000, 25000, 50000, number_of_steps-1]

argument_pool = []  # 500 in paper
size_of_argument_pool = 500  # 500 in paper

scale_parameter_exp_distri = 1  # 1 in paper

number_of_agents = 50  # 50 in paper
size_of_memory = 7  # 7 or unlimited in paper
agents = []

if __name__ == '__main__':
    argument_pool = argp.exponential_distribution_pool(scale_parameter_exp_distri, size_of_argument_pool)

    # give each agent random arguments
    for i in range(number_of_agents):
        arguments_of_one = []

        # TODO bei unlimeted memory, hat jeder dann alle argumente?
        '''
        for k in range(size_of_memory):
            random_index = random.randint(0, size_of_argument_pool - 1)
            next_argument = argument_pool[random_index]
            arguments_of_one.append((random_index, next_argument))
        '''

        # permutiere alle indizes der Argumente, um die ersten size_of_memory vielen indizes herrauszunehmen.
        random_indices_permutation = np.random.permutation(size_of_argument_pool)
        indices_to_take = list(range(0, size_of_memory))
        indices_of_one = np.take(random_indices_permutation, indices_to_take).tolist()

        # bilde aus den permutierten Indizes paare der form (Index, Argument)
        for index in indices_of_one:
            arguments_of_one.append((index, argument_pool[index]))

        # füge die Index, Argument paare in eine HashMap/ Directory ein
        argument_dictionary = dict(arguments_of_one)
        agents.append(argument_dictionary)

    # je ein Schritt der Simulation
    for i in range(number_of_steps):
        # hier wird die deliberation-Strategie und die Vergessens-Strategie angewandt
        delib.outside_deliberation(agents, argument_pool, forg.coherence_minded)

        # Ergebnisse plotten
        if i % plot_every_n_steps == 0 or i in plot_when_in:
            average = mes.opinion_of_each_agent(agents)
            plt.hist(average)
            plt.title("after " + str(i) + " steps")
            plt.xlabel("opinion")
            plt.ylabel("number of agents")
            plt.show()
