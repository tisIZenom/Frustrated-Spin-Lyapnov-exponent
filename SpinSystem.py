## Here I would like to have all the code on how the spin object works and how I can manipulate it as required

from platform import system

import numpy as np
from Lattice.Chain import create_chain


# 3 Dimensional spin
# Create a spin class that contains all the information about the spins
# Then you store in all the attributes that are there globally.


#######################################################################


class SpinSystem:
    def __init__(self, positions, neighbours, J=1):

        self.positions = positions
        self.neighbours = neighbours
        self.N = len(positions)

        # Initializing the spins randomly

        self.spins = np.random.randn(self.N, 3)

        # NOrmalize
        lengths = np.linalg.norm(self.spins, axis=1)

        self.spins /= lengths[:, None]

        # Coupling constant

        self.J = J

        # Randomizing the spins

    def randomize_spins(self):
        self.spins = np.random.randn(self.N, 3)

        lengths = np.linalg.norm(self.spins, axis=1)

        self.spins /= lengths[:, None]

    # Finding the local field:

    def local_field(self, i):
        neighbour_spins = self.spins[self.neighbours[i]]

        return self.J * np.sum(neighbour_spins, axis=0)

    def local_energy(self, i):
        energy = 0.0

        for j in self.neighbours[i]:
            energy += np.dot(self.spins[i], self.spins[j])

        return -self.J * energy

    def total_energy(self):
        energy = 0.0

        for i in range(self.N):
            energy += self.local_energy(i)

        return energy / 2

    # I also need a way to measure the local field for the integrator laterL
    #
    #
    def Local_field(self, i, spins):
        B_local = np.zeros(3)

        for j in self.neighbours[i]:
            B_local = B_local + self.J * self.spins[j]

        return B_local

    # Trying to make a monte carlo system I need a trial move to slightly rotate the spin and check energy.
    def trial_move(self, i, epsilon=0.005):
        target_position = i

        old_config = self.spins[target_position].copy()

        delta = epsilon * np.random.randn(3)

        new_config = old_config + delta

        new_config /= np.linalg.norm(new_config)

        self.spins[target_position] = new_config

        return old_config

    def perturbation(self, target, epsilon):

        delta = epsilon * np.random.randn(3)

        self.spins[target] += delta
        self.spins[target] /= np.linalg.norm(self.spins[target])


#########################################################################


# Checking whether the system works:
