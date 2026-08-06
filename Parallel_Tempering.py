## This is the parallel tempering model over the montecarlo methods


from SpinSystem import SpinSystem
from montecarlo import metropolis
import numpy as np
from Lattice.Chain import create_chain


# First create a set of replicas of the same system
# the first copy:

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
    delta = []
    replica_list = []
    energies = []
    energy_evolution = []

    for T in temperature_gradient:
        new_spin = system

        print(new_spin.total_energy())
        replica = Replica(new_spin, T)

        replica_list.append(replica)

    # Now assign a temperature for each gradient
    # and also just metropolis it

    sweeps = 100
    swap = 100

    for i in range(swap):
        for replica in replica_list:
            metropolis(replica.spin, replica.temperature, sweeps)

        energies = [replica.spin.total_energy() for replica in replica_list]

        for i in range(Num_replicas - 1):
            delta_value = (
                (1 / replica_list[i].temperature)
                - (1 / replica_list[i + 1].temperature)
            ) * (energies[i] - energies[i + 1])

            delta.append(delta_value)

            P = min(1, np.exp(delta[i]))
            if np.random.rand() < P:
                replica_list[i].spin, replica_list[i + 1].spin = (
                    replica_list[i + 1].spin,
                    replica_list[i].spin,
                )
        energy_evolution1 = replica_list[0].spin.total_energy()
        energy_evolution.append(energy_evolution1)

    return replica_list[0].spin, energy_evolution
