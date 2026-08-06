# This version is for generating the graphs.
#


## This is the parallel tempering model over the montecarlo methods

import matplotlib.pyplot as plt
from SpinSystem import SpinSystem
from montecarlo import metropolis
import numpy as np
from Lattice.Chain import create_chain
import copy

# First create a set of replicas of the same system
# the first copy:

positions, neighbours = create_chain(10)


system = SpinSystem(positions, neighbours)

print(system.total_energy())

# nnow I just make the temp gradient from 0.1
# rather have a class replica
#


class Replica:
    def __init__(self, spin, temperature) -> None:
        self.spin = spin
        self.temperature = temperature
        pass


def Rep_exchange_mont(system, SpinSystem):

    Num_replicas = 10

    temperature_gradient = np.linspace(0.01, 0.5, Num_replicas)

    replica_list = []

    energies = []

    energy_matrix = []

    for T in temperature_gradient:
        new_spin = system

        replica = copy.deepcopy(Replica(new_spin, T))

        replica_list.append(replica)

    # Now assign a temperature for each gradient
    # and also just metropolis it

    sweeps = 100
    swap = 100

    for i in range(swap):
        for replica in replica_list:
            metropolis(replica.spin, replica.temperature, sweeps)

        energies = [replica.spin.total_energy() for replica in replica_list]

        energy_matrix.append(energies)

        for j in range(Num_replicas - 1):
            delta_value = (
                (1 / replica_list[j].temperature)
                - (1 / replica_list[j + 1].temperature)
            ) * (energies[j] - energies[j + 1])

            P = min(1, np.exp(delta_value))

            if np.random.rand() < P:
                replica_list[j].spin, replica_list[j + 1].spin = (
                    replica_list[j + 1].spin,
                    replica_list[j].spin,
                )

    return replica_list[0].spin, energy_matrix


system, energy_matrix = Rep_exchange_mont(system, SpinSystem)

energy_matrix = np.array(energy_matrix)
Num_replicas = 10
for j in range(Num_replicas):
    plt.plot(energy_matrix[:, j])

print(system.total_energy())

plt.xlabel("After montecarlo of the replica in a given system before a swap")
plt.ylabel("The energy of the temperature associated spin configuration")
plt.show()
