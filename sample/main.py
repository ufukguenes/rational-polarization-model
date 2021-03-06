import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
from datetime import datetime

if __name__ == '__main__':
    start = datetime.now()
    su.standard_set_up(argp.gaussian_distribution_pool, forg.coherence_minded, delib.outside_deliberation)

    #su.statistical_set_up(argp.exponential_distribution_pool, forg.coherence_minded,
    #                                     delib.outside_deliberation, runs=100)


   # su.statistical_grouped_group_interaction(argp.exponential_distribution_pool, forg.coherence_minded, delib.outside_deliberation,
    #                                        talk_show=True, expert_group=True, runs=10, max_steps=10000)
    print("process finished in: " + str(datetime.now() - start))
