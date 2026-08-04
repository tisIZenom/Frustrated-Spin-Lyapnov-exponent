## Here I try to verify whether the results in the paper Temperature denpendence on butterfly effect in a classical many body system
# accurate for a bigger range. Also whether the lattice structure contributes to the denpendence.
#
#
#
# Steps to look out for
# 1. Generate the graph
# 2. Choose a temperature
# 3. Using monte carlo methods sample the specific temperature and find equillibrium
# 4. Evolve spins using the hamiltonian or the equation of motion
# 5. After given time compute the decorrelator, butterfly and extract lambda and thermal denpendence
#
# 6. Convert the value array into a graphical diagram
# 7. Analyse
#
# Here is how I will structure the project.
"""spin_dynamics/

│
├── lattice.py
│      Creates kagome/chain/square lattices
│
├── montecarlo.py
│      Thermal equilibrium sampling
│
├── dynamics.py
│      Time integration of spin equations
│
├── butterfly.py
│      Creates perturbed copy
│      Computes decorrelator D(x,t)
│
├── observables.py
│      Energy
│      Magnetization
│      Lyapunov exponent
│      Butterfly velocity
│
├── plotting.py
│      Figures
│
└── main.py

"""
