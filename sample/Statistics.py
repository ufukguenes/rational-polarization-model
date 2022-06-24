import copy

import matplotlib.pyplot as plt
import numpy as np

import MeasuringMethods as mes


class Statistics:
    max_index = -1
    steps = []
    average_opinion = []
    opinions_by_group_per_step = []
    index_by_group_per_step = []
    number_of_groups = []
    subgroup_divergence = []
    subgroup_consensus = []
    relative_subgroup_size = []
    time_to_polarize_average = [0, 0]
    time_to_polarize_reasons = [0, 0]
    converged_average = False
    converged_reasons = False

    def __init__(self):
        self.max_index = -1
        self.steps = []
        self.average_opinion = []
        self.opinions_by_group_per_step = []
        self.index_by_group_per_step = []
        self.number_of_groups = []
        self.subgroup_divergence = []
        self.subgroup_consensus = []
        self.relative_subgroup_size = []
        self.time_to_polarize_average = [0, 0]
        self.time_to_polarize_reasons = [0, 0]
        self.converged_average = False
        self.converged_reasons = False

    def calculate(self, agents, current_step):
        self.average_opinion.append(mes.get_average_opinions(agents))
        last_index = len(self.average_opinion) - 1
        opinions_by_group, index_by_group = mes.get_groups(self.average_opinion[last_index])
        self.opinions_by_group_per_step.append(opinions_by_group)
        self.index_by_group_per_step.append(index_by_group)

        self.subgroup_divergence.append(mes.subgroup_divergence_for_two_groups(opinions_by_group))
        self.subgroup_consensus.append(mes.subgroup_consensus(opinions_by_group))
        self.relative_subgroup_size.append(mes.relative_subgroup_size(opinions_by_group))
        self.steps.append(current_step)

        if not self.converged_average and mes.is_converged_average(opinions_by_group):
            self.time_to_polarize_average[1] = current_step
            self.converged_average = True
        elif not self.converged_average:
            self.time_to_polarize_average[0] = current_step
            self.time_to_polarize_average[1] = 0

        if not self.converged_reasons and mes.is_converged_reasons(agents, opinions_by_group, index_by_group):
            self.time_to_polarize_reasons[1] = current_step
            self.converged_reasons = True
        elif not self.converged_reasons:
            self.time_to_polarize_reasons[0] = current_step
            self.time_to_polarize_reasons[1] = current_step

        self.number_of_groups.append(len(opinions_by_group))

        self.max_index = len(self.steps) - 1

    def has_converged(self):
        return self.converged_average and self.converged_reasons

    def create_plot_general_stats(self):
        if self.max_index < 0:
            return
        print("polarized by average / by reasons: " + str(self.converged_average) + " / " + str(self.converged_reasons))
        print("Time to polarize average: ", self.time_to_polarize_average)
        print("Time to polarize reasons: ", self.time_to_polarize_reasons)

        subgroup_consensus_avg = list(map(np.average, self.subgroup_consensus))
        plt.plot(self.steps, subgroup_consensus_avg, label='average subgroup consensus', marker="o")
        plt.plot(self.steps, self.subgroup_divergence, label='subgroup divergence for two groups', marker="o")
        plt.plot(self.steps, self.number_of_groups, label='number of groups', marker="o")
        plt.xlabel("num of steps")
        plt.title("General stats after model converged")
        plt.legend(bbox_to_anchor=(1, 1))

    def plot_subgroup_consensus(self):
        subgroup_consensus_avg = list(map(np.average, self.subgroup_consensus))
        plt.plot(self.steps, subgroup_consensus_avg, marker="o")
        plt.title("Subgroup consensus")
        plt.xlabel("num of steps")

    def create_plot_subgroup_divergence(self):
        sub_sub = []
        sub_sub.append(self.subgroup_divergence[0])
        for i in range(1, len(self.subgroup_divergence)-1):
            if self.subgroup_divergence[i] != 0:
                sub_sub.append(self.subgroup_divergence[i])
            else:
                prev_dif_zero = i
                next_dif_zero = i
                while (self.subgroup_divergence[prev_dif_zero] == 0):
                    prev_dif_zero -= 1
                    if prev_dif_zero <= 0:
                        prev_dif_zero = 0
                        break
                while (self.subgroup_divergence[next_dif_zero] == 0):
                    next_dif_zero += 1
                    if next_dif_zero >= self.max_index:
                        next_dif_zero = self.max_index
                        break
                avg = self.subgroup_divergence[prev_dif_zero] + self.subgroup_divergence[next_dif_zero]
                avg = avg / 2
                sub_sub.append(avg)
        sub_sub.append(self.subgroup_divergence[self.max_index])
        plt.plot(self.steps, sub_sub, label='subgroup divergence for two groups', marker="o")
        plt.title("Subgroup divergence for two groups")
        plt.xlabel("num of steps")

    def create_plot_number_of_groups(self):
        plt.plot(self.steps, self.number_of_groups, marker="o")
        plt.title("Number of Groups")
        plt.xlabel("num of steps")

    def create_plot_relative_group_size(self):
        max_num_of_groups = max(map(len, self.relative_subgroup_size))
        for i in range(len(self.relative_subgroup_size)):
            while len(self.relative_subgroup_size[i]) < max_num_of_groups:
                self.relative_subgroup_size[i].append(0)

        transposed = np.transpose(self.relative_subgroup_size)
        for group in transposed:
            plt.plot(self.steps, group, label='subgroup_size', marker="o")
        plt.xlabel("num of steps")
        plt.title("Relative subgroup size")

    def create_plot_average_opinion(self):
        if self.max_index < 0:
            return
        max_index = self.max_index

        lower = min(-24, round(min(self.average_opinion[max_index])) - 5)
        upper = max(24, round(max(self.average_opinion[max_index])) + 5)
        width = 2

        plt.hist(self.average_opinion[max_index], bins=range(lower, upper, width))
        plt.title("Opinions after " + str(self.steps[max_index]) + " steps")
        plt.xlabel("opinion")
        plt.ylabel("number of agents")