import SetUp as su
import ForgettingStrategy as forg
import DeliberationStrategy as delib
import ArgumentPoolInitialisationStrategy as argp
import ManimVisualisation as mv
from datetime import datetime

if __name__ == '__main__':
    start = datetime.now()
    su.standard_set_up(argp.exponential_distribution_pool, forg.unlimited_minded, delib.pure_subset_deliberation)

    #su.statistical_set_up(argp.exponential_distribution_pool, forg.unlimited_minded,
     #                                    delib.pure_subset_deliberation, runs=100)


   # su.statistical_grouped_group_interaction(argp.exponential_distribution_pool, forg.coherence_minded, delib.outside_deliberation,
    #                                        talk_show=True, expert_group=True, runs=10, max_steps=10000)


    #stats_of_run = su.manim_set_up(argp.exponential_distribution_pool, forg.simple_minded, delib.pure_deliberation, frame_every_n_steps=100)

   # mv.visualise(stats_of_run)


    print("process finished in: " + str(datetime.now() - start))
