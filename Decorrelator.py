## This is my attempt at trying to make a decorrelator to measure the deviation

import numpy as np
from Symplectic_Dynamics_Calculator import time_step, midpoint_configuration_calculator
import copy
from SpinSystem import SpinSystem

# The Symplectic_Dynamics_Calculator gives out new = which is exactly a system
#
#


def decorrelator(system):

    Target = system.N // 2
    time = 50

    # this is for the butterfly velocity

    velocity_time = []
    velocity_distance = []

    original = copy.deepcopy(system)
    perturbed = copy.deepcopy(system)

    # Now I give it a very small perturbation:
    perturbed.perturbation(Target, 0.05)

    ## Now simply let them two evolve:

    for i in range(time):
        original, energy_original = time_step(original, 0.001, 0.1)

        perturbed, perturbed_original = time_step(perturbed, 0.001, 0.1)

        for k in range(system.N):
            local_decorrelator = 1 - np.dot(original.spins[k], perturbed.spins[k])

            if local_decorrelator > 0.01:
                print("The perturbation has spread to:", local_decorrelator, k)

                velocity_time_temp = time
                velocity_time.append(velocity_time_temp)

                velocity_distance.append(k)

                velocity = 1 / time

                # assuming that all the points are unit distance

        local_overlap = np.sum(original.spins * perturbed.spins, axis=1)

        # global_decorelator = 1 - np.mean(local_overlap)
        # print("the total scrabling of the system is:", global_decorelator)

    # The butterfly speed is how quick the perturbation affects the spins of the rest of the system
    #
    #
    # Pseudocode here:
    #
    # need to record where the perturbation spread to at which time step.
    # From which at each instance I can define a butterfly velocity
    # This velocity then I can use to fit the curve as well as the decorrelator
