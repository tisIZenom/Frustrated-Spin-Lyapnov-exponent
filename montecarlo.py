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

    acceptance = 0
    for i in range(sweeps):
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
                    system.spins[target] = old_spin
                    acceptance = acceptance + 1


#    print(
#       "the accpetance against the total attempts were:", acceptance, sweeps * system.N
#   )
