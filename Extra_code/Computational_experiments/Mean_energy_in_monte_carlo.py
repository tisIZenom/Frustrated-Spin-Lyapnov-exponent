from turtle import pos

import numpy as np
import matplotlib.pyplot as plt

from SpinSystem import SpinSystem
from Lattice.create_kogame import (
    build_nn_list,
    find_nn_pairs,
)  # or whatever your square lattice is called
from montecarlo_graph import metropolis
from Thermalization.Frustrated_Spins.main import neighbours  # import your function

# ============================================================
# Simulation Parameters
# ============================================================

Lx = 4
Ly = 4

SWEEPS = 100000

temperatures = np.logspace(-1, 2, 25)

mean_energies = []
std_energies = []
acceptance_ratios = []

# ============================================================
# Temperature Loop
# ============================================================

for T in temperatures:
    print(f"Running T = {T:.3f}")

    positions, cell_index, nn_pairs = find_nn_pairs(Lx, Ly)

    neighbours = build_nn_list(len(positions), nn_pairs)

    system = SpinSystem(positions, neighbours)

    energy, counter, acceptance = metropolis(system, T, SWEEPS)

    burn_in = SWEEPS // 5

    equilibrium = energy[burn_in:]

    mean_energies.append(np.mean(equilibrium))
    std_energies.append(np.std(equilibrium))
    acceptance_ratios.append(acceptance)

mean_energies = np.array(mean_energies)
std_energies = np.array(std_energies)
acceptance_ratios = np.array(acceptance_ratios)

# ============================================================
# Plot
# ============================================================

plt.figure(figsize=(8, 6))

plt.errorbar(temperatures, mean_energies, yerr=std_energies, marker="o", capsize=3)

plt.xscale("log")

plt.xlabel("Temperature")
plt.ylabel("Mean Energy")
plt.title("Mean Energy vs Temperature")

plt.grid(True, which="both", alpha=0.3)

plt.tight_layout()
plt.show()
