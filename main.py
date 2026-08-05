## This is where I will try to test whatever I have written

import matplotlib.pyplot as plt
import numpy as np
from Lattice.Chain import create_chain
from SpinSystem import SpinSystem
from montecarlo import metropolis
from Parallel_Tempering import Rep_exchange_mont
from Symplectic_Dynamics_Calculator import time_step, midpoint_configuration_calculator


positions, neighbours = create_chain(10)


system = SpinSystem(positions, neighbours)

print(system.total_energy())

system_base, energy_evolution = Rep_exchange_mont(system, SpinSystem)

print(energy_evolution)


print(system_base.total_energy())

print("This is how the energy evolved over time ")
system_evolved, energy_list = time_step(system_base, 0.1, 10)


print(energy_list)

print(system_evolved.total_energy())
