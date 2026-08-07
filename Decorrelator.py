# This is for the decorrelator and the butterfly velocity
#

import numpy as np
from Symplectic_Dynamics_Calculator import time_step
import copy
from SpinSystem import SpinSystem


class decorrelator:
    def __init__(self, dt, positional):
        self.dt = dt
        self.positional = positional


def decorrelator_measure(system):
    threshold = 0.0001
    target = system.N // 2
    time = 100

    dt = 0.0001

    original = copy.deepcopy(system)
    perturbed = copy.deepcopy(system)

    # This is the setup
    #

    perturbed.perturbation(target, 0.00000001)

    time_step_1 = int(time // dt)

    De = np.zeros((time_step_1, system.N))

    for i in range(time_step_1):
        original, energy_original = time_step(original, dt, time)
        perturbed, perturbed_original = time_step(perturbed, dt, time)

        # check if they are correct:
        # energies should match check later
        #
        for k in range(system.N):
            De[i, k] = 1 - np.dot(original.spins[k], perturbed.spins[k])

    return decorrelator(dt, De)
