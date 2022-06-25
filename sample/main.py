import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
from datetime import datetime
import warnings

if __name__ == '__main__':
    warnings.simplefilter("error")
    start = datetime.now()
    #su.standard_set_up(argp.exponential_distribution_pool, forg.coherence_minded, delib.rational_deliberation, max_steps=10000)

    su.statistical_set_up(argp.exponential_distribution_pool, forg.coherence_minded,
                                           delib.rational_deliberation, runs=10)

    #su.statistical_grouped_group_interaction(argp.exponential_distribution_pool, forg.coherence_minded,
     #                                        delib.pure_deliberation,
     #                                        talk_show=True, expert_group=False, runs=2)
    print("process finished in: " + str(datetime.now() - start))
