import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
from datetime import datetime
import warnings

if __name__ == '__main__':
    warnings.simplefilter("error")
    start = datetime.now()
    #su.standard_set_up(argp.exponential_distribution_pool, forg.coherence_minded, delib.rational_deliberation_simple, max_steps=5000)

    #su.statistical_set_up(argp.exponential_distribution_pool, forg.weight_coherence_minded,
    #                                      delib.outside_deliberation, runs=1000)


    su.statistical_grouped_group_interaction(argp.exponential_distribution_pool, forg.coherence_minded, delib.outside_deliberation,
                                            talk_show=True, expert_group=True, runs=10, max_steps=10000)
    print("process finished in: " + str(datetime.now() - start))
