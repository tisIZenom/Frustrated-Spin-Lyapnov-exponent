## This is where I will try to test whatever I have written


import matplotlib.pyplot as plt
from Lattice.Chain import create_chain
from SpinSystem import SpinSystem
from montecarlo import metropolis
from Parallel_Tempering_Corrected import Rep_exchange_mont
from Symplectic_Dynamics_Calculator import time_step, midpoint_configuration_calculator
from Decorrelator import decorrelator

from Lattice.create_kogame import find_nn_pairs, build_nn_list


# Create the system layout

positions, cell_index, nn_pairs = find_nn_pairs(3, 3)

neighbours = build_nn_list(len(positions), nn_pairs)

print(neighbours)


# Assign the spins
system = SpinSystem(positions, neighbours)

# Temper the configuration using Parallel_Tempering
system, energy_matrix = Rep_exchange_mont(system, SpinSystem)

for j in range(10):
    plt.plot(energy_matrix[:, j])


# Use the decorrelator
decorrelator(system)
