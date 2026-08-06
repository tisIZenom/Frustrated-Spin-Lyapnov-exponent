# kagome 6site unit cell

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 0) geometric definitions
# ---------------------------
sqrt3 = np.sqrt(3.0)

# Bravais vectors (doubled unit cell compared to 3-site version)
a1 = np.array([2.0, 0.0])
a2 = np.array([0.5, sqrt3 / 2.0])

# 6-site basis inside one unit cell (see your picture)
basis = [
    np.array([0.0, 0.0]),  # site 0
    np.array([0.5, 0.0]),  # site 1
    np.array([0.25, sqrt3 / 4.0]),  # site 2
    np.array([1.0, 0.0]),  # site 3
    np.array([1.5, 0.0]),  # site 4
    np.array([1.25, sqrt3 / 4.0]),  # site 5
]

# pairwise distances (sanity check)
_pairwise_dists = []
for i in range(6):
    for j in range(i + 1, 6):
        _pairwise_dists.append(np.linalg.norm(basis[i] - basis[j]))
_pairwise_dists = np.array(_pairwise_dists)


# ---------------------------
# 1) indexing helpers (x fastest)
# ---------------------------
def global_index(ix, iy, sub, Lx, Ly):
    return (iy * Lx + ix) * 6 + sub


def inv_index(index, Lx, Ly):
    cell = index // 6
    sub = index % 6
    ix = cell % Lx
    iy = cell // Lx
    return ix, iy, sub


def print_index_map(Lx, Ly):
    N = 6 * Lx * Ly
    print(f"Lx={Lx}, Ly={Ly} -> N_sites = {N}")
    print(" (ix,iy,sub) -> index")
    for iy in range(Ly):
        for ix in range(Lx):
            base = (iy * Lx + ix) * 6
            print(
                f" cell (ix={ix}, iy={iy}): indices {base}, {base + 1}, {base + 2}, {base + 3}, {base + 4}, {base + 5}"
            )
    print("\nExample inverse checks (first 12 indices):")
    for idx in range(min(N, 12)):
        print(f" index {idx:2d} -> (ix,iy,sub) = {inv_index(idx, Lx, Ly)}")


# ---------------------------
# 2) build sites (positions + metadata)
# ---------------------------
def build_sites(Lx, Ly):
    positions = []
    cell_index = []
    for iy in range(Ly):
        for ix in range(Lx):
            R = ix * a1 + iy * a2
            for sub, d in enumerate(basis):
                pos = R + d
                positions.append(pos)
                cell_index.append((ix, iy, sub))
    positions = np.array(positions)
    return positions, cell_index


# ---------------------------
# 3) find nearest-neighbor pairs
# ---------------------------
def find_nn_pairs(Lx, Ly, r_cut=0.6, pbc=True):
    positions, cell_index = build_sites(Lx, Ly)
    N = positions.shape[0]
    nn_pairs = []

    for i, (ix, iy, sub_i) in enumerate(cell_index):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for sub_j in range(6):
                    jix = ix + dx
                    jiy = iy + dy

                    # boundary handling
                    if pbc:
                        jix_mod = jix % Lx
                        jiy_mod = jiy % Ly
                    else:
                        if (jix < 0) or (jix >= Lx) or (jiy < 0) or (jiy >= Ly):
                            continue
                        jix_mod = jix
                        jiy_mod = jiy

                    j_index = global_index(jix_mod, jiy_mod, sub_j, Lx, Ly)

                    # avoid self and double counting
                    if j_index <= i:
                        continue

                    # displacement using dx,dy (not wrapped)
                    disp = dx * a1 + dy * a2 + basis[sub_j] - basis[sub_i]
                    dist = np.linalg.norm(disp)

                    if (dist > 1e-8) and (dist < r_cut):
                        nn_pairs.append((i, j_index))

    return positions, cell_index, nn_pairs


# ---------------------------
# 4) build Hamiltonian
# ---------------------------
def build_kagome6_hamiltonian(Lx, Ly, t=1.0, mu=0.0, pbc=True):
    positions, cell_index, nn_pairs = find_nn_pairs(Lx, Ly, pbc=pbc)
    N = len(positions)
    H = np.zeros((N, N), dtype=float)

    # hoppings
    for i, j in nn_pairs:
        H[i, j] = -t
        H[j, i] = -t

    # onsite
    for i in range(N):
        H[i, i] += mu

    return H, positions, cell_index, nn_pairs


# ---------------------------
# 5) demonstration / run
# ---------------------------
if __name__ == "__main__":
    # parameters
    Lx = 2
    Ly = 2
    t = 1.0
    mu = 0.0
    pbc = True

    print_index_map(Lx, Ly)
    print("Pairwise distances inside basis (sanity):", _pairwise_dists)

    # build Hamiltonian
    H, positions, cell_index, nn_pairs = build_kagome6_hamiltonian(
        Lx, Ly, t=t, mu=mu, pbc=pbc
    )

    # quick summaries
    N = len(positions)
    print("\nTotal sites N =", N)
    print("NN bonds (undirected) count:", len(nn_pairs))
    print("First 24 bonds (i, j):", nn_pairs[:24])

    print("\nHamiltonian (dense) shape:", H.shape)
    np.set_printoptions(precision=3, suppress=True)
    print(H)

    # eigenvalues
    eigvals = np.linalg.eigvalsh(H)
    print("\nEigenvalues:", np.round(eigvals, 6))

    # plot lattice and labels
    plt.figure(figsize=(6, 6))
    plt.scatter(positions[:, 0], positions[:, 1], s=80)
    for i, pos in enumerate(positions):
        plt.text(pos[0] + 0.02, pos[1] + 0.02, str(i), fontsize=10)
    for i, j in nn_pairs:
        p1, p2 = positions[i], positions[j]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], lw=1)
    plt.gca().set_aspect("equal", "box")
    plt.title(f"Kagome (6-site unit cell) patch Lx={Lx}, Ly={Ly}, N={N}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
