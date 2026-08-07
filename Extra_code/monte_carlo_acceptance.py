## This is where I will try to make the metropolis algorithm and change the spin config

import random
import matplotlib.pyplot as plt
import numpy as np

from SpinSystem import SpinSystem
from Lattice.Chain import create_chain

# ============================================================
# Build the lattice
# ============================================================

positions, neighbours = create_chain(int(input("What is the number of nodes: ")))

system = SpinSystem(positions, neighbours)

# ============================================================
# Simulation Parameters
# ============================================================

T = float(input("Temperature: "))
SWEEPS = int(input("Number of Monte Carlo sweeps: "))

# ============================================================
# Metropolis Algorithm
# ============================================================


def metropolis(system, temp, sweeps):

    energy = []
    counter = []

    acceptance = 0
    total_attempts = sweeps * system.N

    for sweep in range(sweeps):
        for attempt in range(system.N):
            target = np.random.randint(system.N)

            old_energy = system.local_energy(target)

            old_spin = system.trial_move(target)

            new_energy = system.local_energy(target)

            delta_energy = new_energy - old_energy

            if delta_energy <= 0:
                acceptance += 1

            else:
                probability = np.exp(-delta_energy / temp)

                if random.random() < probability:
                    acceptance += 1

                else:
                    system.spins[target] = old_spin

        energy.append(system.total_energy())
        counter.append(sweep)

    acceptance_ratio = acceptance / total_attempts

    return np.asarray(energy), np.asarray(counter), acceptance_ratio


# ============================================================
# Run Simulation
# ============================================================

energy, counter, acceptance_ratio = metropolis(system, T, SWEEPS)

# ============================================================
# Compute Statistics
# ============================================================

mean_energy = np.mean(energy)
std_energy = np.std(energy)

minimum_energy = np.min(energy)
maximum_energy = np.max(energy)

final_energy = energy[-1]

# Running average (optional but useful)

running_average = np.cumsum(energy) / np.arange(1, len(energy) + 1)


burn_in = SWEEPS // 5

equilibrium_energy = energy[burn_in:]

mean_energy_equi = np.mean(equilibrium_energy)
std_energy_equi = np.std(equilibrium_energy)
minimum_energy = np.min(equilibrium_energy)
maximum_energy = np.max(equilibrium_energy)


# ============================================================
# Print Statistics
# ============================================================

print("\n==============================")
print("Monte Carlo Statistics")
print("==============================")
print(f"Temperature        : {T}")
print(f"Number of Spins    : {system.N}")
print(f"Monte Carlo Sweeps : {SWEEPS}")
print()
print(f"Final Energy       : {final_energy:.6f}")
print(f"Mean Energy        : {mean_energy:.6f}")
print(f"Std Deviation      : {std_energy:.6f}")
print(f"Minimum Energy     : {minimum_energy:.6f}")
print(f"Maximum Energy     : {maximum_energy:.6f}")
print(f"Acceptance Ratio   : {100 * acceptance_ratio:.2f}%")
print(f"equilibrium_energy mean : {mean_energy_equi}")
print(f"standard deviation energy_equillibruim: {std_energy_equi}")
print("==============================")

# ============================================================
# Plot
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(counter, energy, label="Energy")
plt.plot(counter, running_average, linewidth=2, label="Running Mean")

plt.xlabel("Monte Carlo Sweep")
plt.ylabel("Total Energy")
plt.title("Metropolis Monte Carlo")

statistics = (
    f"Mean Energy : {mean_energy:.4f}\n"
    f"Std Dev     : {std_energy:.4f}\n"
    f"Final Energy: {final_energy:.4f}\n"
    f"Acceptance  : {100 * acceptance_ratio:.2f}%"
)

plt.text(
    0.02,
    0.98,
    statistics,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(facecolor="white", edgecolor="black", alpha=0.85),
)

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
