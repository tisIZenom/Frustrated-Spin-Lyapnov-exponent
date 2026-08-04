# This is where I will try to make the metropolis algorithm and change the spin config

import random

import numpy as np
from SpinSystem import SpinSystem
from Lattice.Chain import create_chain

positions, neighbours = create_chain(int(input("What is the number of nodes: ")))

spin = SpinSystem(positions, neighbours)


## The important variables:
temp = float(input("what is the desired temperature for the system: "))
sweeps = int(input("how many sweeps would you like?: "))

print(spin.total_energy())


def metropolis(spin, temp, sweeps):

    acceptance = 0

    for i in range(sweeps):
        for attempt in range(spin.N):
            target = np.random.randint(spin.N)

            old_energy = spin.local_energy(target)

            old_spin = spin.trial_move(target)

            new_energy = spin.local_energy(target)

            delta_energy = new_energy - old_energy

            if delta_energy <= 0:
                acceptance = acceptance + 1
                pass

            else:
                probability = np.exp((-1 * delta_energy) / temp)

                if random.random() > probability:
                    spin.spins[target] = old_spin
                    acceptance = acceptance + 1

    print(
        "the accpetance against the total attempts were:", acceptance, sweeps * spin.N
    )


metropolis(spin, temp, sweeps)

print(spin.total_energy())
