# ============================================================
# Pilot Script for Monte Carlo Parameter Sweep
#
# Parallel Version
#
# Each Monte Carlo run is executed in a separate process.
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

from concurrent.futures import ProcessPoolExecutor

from SpinSystem import SpinSystem
from Lattice.create_kogame import find_nn_pairs, build_nn_list
from montecarlo_graph import metropolis


# ============================================================
# Parameters
# ============================================================

SWEEPS = 1000
RUNS = 20

# Number of simulations running simultaneously
MAX_WORKERS = 10

TEMPERATURES = np.logspace(-1, 2, 25)

SIZES = [
    (3, 3),
    (4, 3),
    (4, 4),
    (5, 4),
    (5, 5),
    (6, 5),
    (6, 6),
    (8, 6),
    (8, 8),
    (10, 8),
    (10, 10),
    (12, 10),
    (12, 12),
    (14, 12),
    (14, 14),
]

OUTPUT_FOLDER = "MonteCarloRuns"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# Worker Function
# ============================================================


def run_single_simulation(args):

    run, positions, neighbours, temperature_folder, Lx, Ly, T = args

    system = SpinSystem(positions, neighbours)

    energy, counter = metropolis(system, T, SWEEPS)

    energy = np.asarray(energy)
    counter = np.asarray(counter)

    # ---------------- Raw Data ----------------

    np.savetxt(
        os.path.join(temperature_folder, f"run_{run:03d}.csv"),
        np.column_stack((counter, energy)),
        delimiter=",",
        header="Sweep,Energy",
        comments="",
    )

    # ---------------- Plot ----------------

    plt.figure(figsize=(8, 5))

    plt.plot(counter, energy)

    plt.xlabel("Monte Carlo Sweep")
    plt.ylabel("Energy")

    plt.title(f"Lx={Lx}  Ly={Ly}  T={T:.4f}  Run={run}")

    plt.tight_layout()

    plt.savefig(
        os.path.join(temperature_folder, f"run_{run:03d}.png"),
        dpi=150,
    )

    plt.close()

    return [
        run,
        energy[-1],
        np.mean(energy),
        np.std(energy),
        np.min(energy),
        np.max(energy),
    ]


# ============================================================
# Main Program
# ============================================================

if __name__ == "__main__":
    for Lx, Ly in SIZES:
        print("=" * 60)
        print(f"Lattice Size : {Lx} x {Ly}")

        positions, cell_index, nn_pairs = find_nn_pairs(Lx, Ly)

        neighbours = build_nn_list(len(positions), nn_pairs)

        N = len(positions)

        lattice_folder = os.path.join(OUTPUT_FOLDER, f"Lx{Lx}_Ly{Ly}_N{N}")

        os.makedirs(lattice_folder, exist_ok=True)

        for T in TEMPERATURES:
            print(f"Temperature = {T:.4f}")

            temperature_folder = os.path.join(lattice_folder, f"T_{T:.4f}")

            os.makedirs(temperature_folder, exist_ok=True)

            jobs = []

            for run in range(RUNS):
                jobs.append(
                    (
                        run,
                        positions,
                        neighbours,
                        temperature_folder,
                        Lx,
                        Ly,
                        T,
                    )
                )

            with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
                summary = list(
                    executor.map(
                        run_single_simulation,
                        jobs,
                    )
                )

            summary = np.asarray(summary)

            np.savetxt(
                os.path.join(
                    temperature_folder,
                    "summary.csv",
                ),
                summary,
                delimiter=",",
                header="Run,FinalEnergy,MeanEnergy,StdEnergy,MinimumEnergy,MaximumEnergy",
                comments="",
            )

    print("\nAll simulations completed successfully.")
