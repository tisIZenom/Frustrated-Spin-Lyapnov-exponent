## This is where I will try to test whatever I have written

import numpy as np
import matplotlib.pyplot as plt
from Lattice.Chain import create_chain
from SpinSystem import SpinSystem
from montecarlo import metropolis
from Parallel_Tempering import Rep_exchange_mont
from Symplectic_Dynamics_Calculator import time_step, midpoint_configuration_calculator
from Decorrelator_corrected import decorrelator, decorrelator_measure

from Lattice.create_kogame import find_nn_pairs, build_nn_list


# Create the system layout

positions, cell_index, nn_pairs = find_nn_pairs(4, 4)

neighbours = build_nn_list(len(positions), nn_pairs)

print(neighbours)


# Assign the spins
system = SpinSystem(positions, neighbours)

# Temper the configuration using Parallel_Tempering
system, energy_matrix = Rep_exchange_mont(system, SpinSystem)


# Use the decorrelator
data = decorrelator_measure(system)


# this is for plotting and stuff. 1. global decorrelator
time = np.arange(data.positional.shape[0]) * data.dt

global_D = np.mean(data.positional, axis=1)

plt.figure(figsize=(7, 5))

plt.plot(time, global_D, linewidth=2)

plt.xlabel("Time")
plt.ylabel(r"$D(t)$")

plt.title("Global Decorrelator")

plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# This is now for the heatmap
plt.figure(figsize=(8, 6))

plt.imshow(
    data.positional,
    origin="lower",
    aspect="auto",
    extent=[0, system.N, 0, data.positional.shape[0] * data.dt],
)

plt.xlabel("Lattice site")

plt.ylabel("Time")

plt.title("Local Decorrelator")

plt.colorbar(label=r"$1-\mathbf S_i\cdot\mathbf S_i'$")

plt.tight_layout()

plt.show()

# now the butterflu plt
#
threshold = 1e-3

front_position = []
front_time = []

for i in range(data.positional.shape[0]):
    indices = np.where(data.positional[i] > threshold)[0]

    if len(indices) > 0:
        front_position.append(indices.max())

        front_time.append(i * data.dt)

# now comes the plot
#

plt.figure(figsize=(6, 5))

plt.scatter(front_time, front_position, s=25)

plt.xlabel("Time")

plt.ylabel("Front position")

plt.title("Butterfly Front")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.show()
