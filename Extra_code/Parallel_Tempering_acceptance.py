# ============================================================
# Driver
# ============================================================

positions, neighbours = create_chain(int(input("Number of lattice sites : ")))

system = SpinSystem(positions, neighbours)

replica0, energy_matrix = Rep_exchange_mont(system, SpinSystem)

# ============================================================
# Analyse Replica 0
# ============================================================

replica0_energy = energy_matrix[:, 0]

exchange_steps = np.arange(len(replica0_energy))

running_mean = np.cumsum(replica0_energy) / np.arange(1, len(replica0_energy) + 1)

mean_energy = np.mean(replica0_energy)
std_energy = np.std(replica0_energy)

minimum_energy = np.min(replica0_energy)
maximum_energy = np.max(replica0_energy)

final_energy = replica0_energy[-1]

print("\n===================================")
print("Replica 0 Statistics")
print("===================================")
print(f"Final Energy   : {final_energy:.6f}")
print(f"Mean Energy    : {mean_energy:.6f}")
print(f"Std Deviation  : {std_energy:.6f}")
print(f"Minimum Energy : {minimum_energy:.6f}")
print(f"Maximum Energy : {maximum_energy:.6f}")
print("===================================")

# ============================================================
# Plot Replica 0
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(exchange_steps, replica0_energy, lw=1.5, label="Replica 0 Energy")

plt.plot(exchange_steps, running_mean, lw=2.5, label="Running Mean")

statistics = (
    f"Final = {final_energy:.4f}\nMean = {mean_energy:.4f}\nStd = {std_energy:.4f}"
)

plt.text(
    0.02,
    0.98,
    statistics,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    bbox=dict(facecolor="white", edgecolor="black", alpha=0.85),
)

plt.xlabel("Replica Exchange Step")
plt.ylabel("Energy")
plt.title("Parallel Tempering : Replica 0")

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
