# ============================================================
# Pilot Script for Monte Carlo Parameter Sweep
#
# Sweeps:
#   - System Size (Lx, Ly)
#   - Temperature
#   - Random Initial Conditions
#
# Saves:
#   - Energy vs Sweep (csv)
#   - Energy plot (png)
#   - Summary statistics
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

from SpinSystem import SpinSystem
from Lattice.create_kogame import find_nn_pairs, build_nn_list
from montecarlo_graph import metropolis

# ============================================================
# Simulation Parameters
# ============================================================

SWEEPS = 1000
RUNS = 20

# Temperatures from 0.1 to 100
TEMPERATURES = np.logspace(-1, 2, 25)

# Kagome lattice sizes
# N = 3*Lx*Ly

SIZES = [
    (3, 3),  # 27
    (4, 3),  # 36
    (4, 4),  # 48
    (5, 4),  # 60
    (5, 5),  # 75
    (6, 5),  # 90
    (6, 6),  # 108
    (8, 6),  # 144
    (8, 8),  # 192
    (10, 8),  # 240
    (10, 10),  # 300
    (12, 10),  # 360
    (12, 12),  # 432
    (14, 12),  # 504
    (14, 14),  # 588
]

OUTPUT_FOLDER = "MonteCarloRuns"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ============================================================
# Start Sweep
# ============================================================

for Lx, Ly in SIZES:
    print("=" * 60)
    print(f"Lattice Size : {Lx} x {Ly}")

    positions, cell_index, nn_pairs = find_nn_pairs(Lx, Ly)
    neighbours = build_nn_list(len(positions), nn_pairs)

    N = len(positions)

    lattice_folder = os.path.join(OUTPUT_FOLDER, f"Lx{Lx}_Ly{Ly}_N{N}")

    os.makedirs(lattice_folder, exist_ok=True)

    # --------------------------------------------------------

    for T in TEMPERATURES:
        print(f"    Temperature = {T:.4f}")

        temperature_folder = os.path.join(lattice_folder, f"T_{T:.4f}")

        os.makedirs(temperature_folder, exist_ok=True)

        summary = []

        # ----------------------------------------------------

        for run in range(RUNS):
            print(f"        Run {run + 1}/{RUNS}")

            system = SpinSystem(positions, neighbours)

            energy, counter = metropolis(system, T, SWEEPS)

            energy = np.asarray(energy)
            counter = np.asarray(counter)

            # ==============================================
            # Save raw data
            # ==============================================

            filename = os.path.join(temperature_folder, f"run_{run:03d}.csv")

            np.savetxt(
                filename,
                np.column_stack((counter, energy)),
                delimiter=",",
                header="Sweep,Energy",
                comments="",
            )

            # ==============================================
            # Save Plot
            # ==============================================

            plt.figure(figsize=(8, 5))

            plt.plot(counter, energy)

            plt.xlabel("Monte Carlo Sweep")
            plt.ylabel("Energy")
            plt.title(f"Lx={Lx}  Ly={Ly}  T={T:.4f}  Run={run}")

            plt.tight_layout()

            plt.savefig(os.path.join(temperature_folder, f"run_{run:03d}.png"), dpi=150)

            plt.close()

            # ==============================================
            # Statistics
            # ==============================================

            summary.append(
                [
                    run,
                    energy[-1],
                    np.mean(energy),
                    np.std(energy),
                    np.min(energy),
                    np.max(energy),
                ]
            )

        # ----------------------------------------------------
        # Save summary for this temperature
        # ----------------------------------------------------

        summary = np.asarray(summary)

        np.savetxt(
            os.path.join(temperature_folder, "summary.csv"),
            summary,
            delimiter=",",
            header="Run,FinalEnergy,MeanEnergy,StdEnergy,MinimumEnergy,MaximumEnergy",
            comments="",
        )

print("\nAll simulations completed successfully.")
