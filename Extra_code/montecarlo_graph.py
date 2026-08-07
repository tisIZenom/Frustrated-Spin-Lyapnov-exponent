# This is where I will try to make the metropolis algorithm and change the spin config

from platform import system_alias
import random
import matplotlib.pyplot as plt
import numpy as np
from SpinSystem import SpinSystem
from Lattice.Chain import create_chain

positions, neighbours = create_chain(int(input("What is the number of nodes: ")))

system = SpinSystem(positions, neighbours)


## The important variables:

print(system.total_energy())


def metropolis(system, temp, sweeps):

    energy = []
    counter = []

    acceptance = 0

    for i in range(sweeps):
        # this goes through the entire system
        #

        for attempt in range(system.N):
            target = np.random.randint(system.N)

            old_energy = system.local_energy(target)

            old_spin = system.trial_move(target)

            new_energy = system.local_energy(target)

            delta_energy = new_energy - old_energy

            if delta_energy <= 0:
                pass

            else:
                probability = np.exp((-1 * delta_energy) / temp)

                if random.random() < probability:
                    pass

                else:
                    system.spins[target] = old_spin

        # This is for the energy graph remove once done buddy
        energy_per_monte_carlo = system.total_energy()
        energy.append(energy_per_monte_carlo)
        counter.append(i)
    return energy, counter


energy, counter = metropolis(system, 0.01, 1000)

plt.plot(counter, energy)

plt.xlabel("number of sweeps that occured")
plt.ylabel("Respective energy for the configuration of the sweep")
plt.show()

print(system.total_energy())

#    print(
#       "the accpetance against the total attempts were:", acceptance, sweeps * system.N
#   )
