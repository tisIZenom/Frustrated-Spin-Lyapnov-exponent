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
    time = 100

    original = copy.deepcopy(system)
    perturbed = copy.deepcopy(system)

    # Now I give it a very small perturbation:
    perturbed.perturbation(Target, 0.05)

    ## Now simply let them two evolve:
    print(type(original))
    print(type(perturbed))

    for i in range(time):
        original, energy_original = time_step(original, 0.1, 10)

        perturbed, perturbed_original = time_step(perturbed, 0.1, 10)

        for k in range(system.N):
            local_decorrelator = 1 - np.dot(original.spins[k], perturbed.spins[k])

            if local_decorrelator > 0.01:
                print("The perturbation has spread to:", local_decorrelator, k)

        local_overlap = np.sum(original.spins * perturbed.spins, axis=1)
        global_decorelator = 1 - np.mean(local_overlap)

        print("the total scrabling of the system is:", global_decorelator)
