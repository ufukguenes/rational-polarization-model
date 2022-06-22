import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp


if __name__ == '__main__':
    #su.standard_set_up(argp.exponential_distribution_pool, forg.simple_minded, delib.pure_deliberation)
    su.statistical_set_up(argp.exponential_distribution_pool, forg.coherence_minded, delib.outside_deliberation, runs=2)
