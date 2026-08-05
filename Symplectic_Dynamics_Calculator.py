from calendar import c
import sys

import numpy as np
import copy

from Parallel_Tempering import Rep_exchange_mont

# system = replica[0]


def midpoint_configuration_calculator(new, old):

    midpoints = []

    for i in range(new.N):
        midpoint_temp = new.spins[i] + old.spins[i]

        midpoint_temp /= np.linalg.norm(midpoint_temp)

        midpoints.append(midpoint_temp)

    return midpoints


def time_step(system, dt, total_time):

    new = copy.deepcopy(system)
    old = copy.deepcopy(system)

    energy = []

    num_steps = int(total_time / dt)

    for step in range(num_steps):
        # Initial guess for the implicit solve

        for iteration in range(1000):
            previous = copy.deepcopy(new)

            # Compute midpoint configuration
            midpoints = midpoint_configuration_calculator(new, old)

            # Update every spin
            for i in range(new.N):
                midpoint_field = system.Local_field(i, midpoints)

                new.spins[i] = old.spins[i] + dt * np.cross(
                    midpoints[i], midpoint_field
                )

            # Convergence test
            error = np.max(np.linalg.norm(new.spins - previous.spins, axis=1))

            if error < 1e-10:
                break

        # Advance to the next timestep
        old = copy.deepcopy(new)
        # need to give out an energy graph

        energy_temp = new.total_energy()
        energy.append(energy_temp)

    return new, energy
