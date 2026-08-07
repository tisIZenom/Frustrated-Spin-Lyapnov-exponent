import matplotlib.pyplot as plt
import numpy as np
import copy

from SpinSystem import SpinSystem
from montecarlo import metropolis
from Lattice.Chain import create_chain

# ============================================================
# Build System
# ============================================================

positions, neighbours = create_chain(10)
system = SpinSystem(positions, neighbours)

print("Initial Energy:", system.total_energy())

# ============================================================
# Replica Class
# ============================================================


class Replica:
    def __init__(self, spin, temperature):
        self.spin = spin
        self.temperature = temperature


# ============================================================
# Parallel Tempering
# ============================================================


def Rep_exchange_mont(system):

    Num_replicas = 10

    # Same logarithmic temperature range as the Metropolis study
    temperature_gradient = np.logspace(-1, 2, Num_replicas)

    replica_list = []
    energy_matrix = []

    # Create replicas
    for T in temperature_gradient:
        new_spin = copy.deepcopy(system)

        replica = Replica(new_spin, T)

        replica_list.append(replica)

    sweeps = 100
    swaps = 200

    # ========================================================
    # Parallel Tempering Loop
    # ========================================================

    for step in range(swaps):
        # Monte Carlo evolution
        for replica in replica_list:
            metropolis(replica.spin, replica.temperature, sweeps)

        # Measure energies before attempting exchanges
        energies = [replica.spin.total_energy() for replica in replica_list]
        energy_matrix.append(energies)

        # Replica exchange
        for j in range(Num_replicas - 1):
            delta = (
                (1 / replica_list[j].temperature)
                - (1 / replica_list[j + 1].temperature)
            ) * (energies[j] - energies[j + 1])

            probability = min(1.0, np.exp(delta))

            if np.random.rand() < probability:
                replica_list[j].spin, replica_list[j + 1].spin = (
                    replica_list[j + 1].spin,
                    replica_list[j].spin,
                )

    return replica_list, np.array(energy_matrix), temperature_gradient


# ============================================================
# Run Simulation
# ============================================================

replicas, energy_matrix, temperature_gradient = Rep_exchange_mont(system)

print("Final Energy:", replicas[0].spin.total_energy())

# ============================================================
# Plot Energy History
# ============================================================

plt.figure(figsize=(9, 6))

for j in range(len(temperature_gradient)):
    plt.plot(energy_matrix[:, j], label=f"T={temperature_gradient[j]:.2f}")

plt.xlabel("Replica Exchange Step")
plt.ylabel("Total Energy")
plt.title("Energy History of Each Temperature")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ============================================================
# Thermodynamic Averages
# ============================================================

burn_in = len(energy_matrix) // 5

equilibrium = energy_matrix[burn_in:]

mean_energy = np.mean(equilibrium, axis=0)
std_energy = np.std(equilibrium, axis=0)

# ============================================================
# Mean Energy vs Temperature
# ============================================================

plt.figure(figsize=(8, 6))

plt.errorbar(
    temperature_gradient,
    mean_energy,
    yerr=std_energy,
    fmt="o-",
    linewidth=2,
    capsize=4,
    label="Mean Energy",
)

plt.xscale("log")

plt.xlabel("Temperature")
plt.ylabel("Mean Energy")
plt.title("Parallel Tempering: Mean Energy vs Temperature")

plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# ============================================================
# Print Statistics
# ============================================================

print("\n==============================================")
print("Temperature    Mean Energy      Std Deviation")
print("==============================================")

for T, E, S in zip(temperature_gradient, mean_energy, std_energy):
    print(f"{T:10.4f} {E:14.6f} {S:14.6f}")

print("==============================================")
