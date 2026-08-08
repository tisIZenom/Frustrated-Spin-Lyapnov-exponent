import numpy as np
import matplotlib.pyplot as plt

from SpinSystem import SpinSystem
from Parallel_Tempering import Rep_exchange_mont
from Decorrelator_corrected import decorrelator_measure

from Lattice.create_kogame import find_nn_pairs, build_nn_list

# ==========================================================
# Build the lattice
# ==========================================================

positions, cell_index, nn_pairs = find_nn_pairs(4, 4)

positions = np.asarray(positions)

neighbours = build_nn_list(len(positions), nn_pairs)

system = SpinSystem(positions, neighbours)

system, energy_matrix = Rep_exchange_mont(system, SpinSystem)

# ==========================================================
# Measure decorrelator
# ==========================================================

data = decorrelator_measure(system)

# ==========================================================
# Time axis
# ==========================================================

time = np.arange(data.positional.shape[0]) * data.dt

# ==========================================================
# GLOBAL DECORRELATOR
# ==========================================================

global_D = np.mean(data.positional, axis=1)

plt.figure(figsize=(7, 5))

plt.plot(time, global_D, lw=2)

plt.xlabel("Time")
plt.ylabel(r"$\langle D(t)\rangle$")

plt.title("Global Decorrelator")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.show()

# ==========================================================
# HEAT MAP
#
# Sort lattice sites by their physical distance from
# the perturbed spin.
# ==========================================================

target = system.N // 2

distances = np.linalg.norm(positions - positions[target], axis=1)

order = np.argsort(distances)

sorted_D = data.positional[:, order]

sorted_distances = distances[order]

plt.figure(figsize=(8, 6))

plt.imshow(
    sorted_D,
    origin="lower",
    aspect="auto",
    extent=[sorted_distances[0], sorted_distances[-1], 0, time[-1]],
)

plt.xlabel("Distance from perturbation")

plt.ylabel("Time")

plt.title("Decorrelator Heat Map")

plt.colorbar(label=r"$1-\mathbf S_i\cdot\mathbf S_i'$")

plt.tight_layout()

plt.show()

# ==========================================================
# BUTTERFLY FRONT
# ==========================================================

threshold = 1e-3

front_distance = []
front_time = []

for i in range(data.positional.shape[0]):
    indices = np.where(data.positional[i] > threshold)[0]

    if len(indices) == 0:
        continue

    d = np.max(distances[indices])

    front_distance.append(d)

    front_time.append(time[i])

plt.figure(figsize=(6, 5))

plt.scatter(front_time, front_distance, s=20)

plt.xlabel("Time")

plt.ylabel("Distance from perturbation")

plt.title("Butterfly Front")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.show()
