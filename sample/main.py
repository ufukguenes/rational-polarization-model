import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
import warnings



if __name__ == '__main__':
    warnings.filterwarnings("error")
    # su.standard_set_up(argp.exponential_distribution_pool, forg.simple_minded, delib.pure_deliberation)
    su.stand_set_up(argp.exponential_distribution_pool, forg.simple_minded, delib.outside_deliberation)
