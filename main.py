## This is where I will try to test whatever I have written


import numpy as np
from Lattice.Chain import create_chain
from SpinSystem import SpinSystem
from montecarlo import metropolis
from Parallel_Tempering import Rep_exchange_mont
from symplecticdynamics2 import time_step, midpoint_configuration_calculator


positions, neighbours = create_chain(10)


system = SpinSystem(positions, neighbours)

print(system.total_energy())

temperature_gradient = np.linspace(0.01, 0.5, 10)


system_base = Rep_exchange_mont(system, 10, temperature_gradient, SpinSystem)


print(system_base.total_energy())

system_evolved = time_step(system_base, 0.1, 10)

print(system_evolved.total_energy)
