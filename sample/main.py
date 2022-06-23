import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
from datetime import datetime



if __name__ == '__main__':
    start = datetime.now()
    # su.standard_set_up(argp.exponential_distribution_pool, forg.unlimited_minded, delib.pure_deliberation, max_steps=10000)

    su.statistical_set_up(argp.exponential_distribution_pool, forg.coherence_minded, delib.outside_deliberation,
                          size_of_argument_pool=500, count_of_memory=7, runs=100)
    print("process finished in: " + str(datetime.now() - start))
