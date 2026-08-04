## This is the parallel tempering model over the montecarlo methods


from SpinSystem import SpinSystem
from montecarlo import metropolis
import numpy as np
from Lattice.Chain import create_chain


# First create a set of replicas of the same system
# the first copy:

position, neighbours = create_chain(int(input("what is the number of nodes?: ")))
# This created the system
#
# nnow I just make the temp gradient from 0.1
spin = SpinSystem(position, neighbours)

# rather have a class replica
#


class Replica:
    def __init__(self, spin, temperature) -> None:
        self.spin = spin
        self.temperature = temperature
        pass


temperature = float(
    input("What is the range of temperatures to sample (upto  0.1)?:  ")
)


Replica_resolution = int(input("How many parallel replicas would you like?: "))


temperature_gradient = np.linspace(0.01, 0.5, Replica_resolution)


def Rep_exchange_mont(spin, Replica_resolution, temperature_gradient, SpinSystem):

    delta = []
    replicas = []
    energies = []

    for T in temperature_gradient:
        new_spin = SpinSystem(position, neighbours)

        print(new_spin.total_energy())
        replica = Replica(new_spin, T)

        replicas.append(replica)

    # Now assign a temperature for each gradient
    # and also just metropolis it

    sweeps = 200
    swap = 200

    for i in range(swap):
        for replica in replicas:
            metropolis(replica.spin, replica.temperature, sweeps)

        energies = [replica.spin.total_energy() for replica in replicas]

        for i in range(Replica_resolution - 1):
            delta_value = (
                (1 / replicas[i].temperature) - (1 / replicas[i + 1].temperature)
            ) * (energies[i] - energies[i + 1])

            delta.append(delta_value)

            P = min(1, np.exp(delta[i]))
            if np.random.rand() < P:
                replicas[i].spin, replicas[i + 1].spin = (
                    replicas[i + 1].spin,
                    replicas[i].spin,
                )

    return replicas[0]


total = Rep_exchange_mont(spin, Replica_resolution, temperature_gradient, SpinSystem)

print(total.spin.total_energy())
