In this paper ![[PhysRevLett.121.250602.pdf]]

We are trying to establish a clear connection between the lyapnov exponent and the temperature of the frustrated spin system to be a power law one. Furthermore the numerical simulation suggests that it should be:$$ \huge 
\lambda \propto \sqrt{ T }
$$
Which is a rather strong claim. Our objective is to try to probe into whether this holds true in extreme conditions of nonlinearity and temperature(namely lower temperatures). 

___ 
## Analysis

So far the analysis of the problem is that it's a trivial in the hamiltonian construction as long as we do not have a myopic approach to the nonlinearity at hand. 

The bonds influence each other and information cascades as expected. 

Some of the local energies and similar properties of interest can be solved. 

- Here is a list of the formula that is important for our analysis


___ 

## Numerical methods used

As a matter of writing good code I broke down the project into many smaller modular components and tried to build them all together. This helps not only in trying to debug the entire simulation but it also helps in swapping out components to create more diversity and helps in approaching the problem in different perspectives. 

Here is the main code architecture: 
"""spin_dynamics/

│
├── Lattices 
|      |
|      |---chain.py - creates a 1D chain
|      |---Kogame.py 
│     
│
├── Minimizer 
|      montecarlo.py
│      Thermal equilibrium sampling
|      Parallel tempering 
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

___ 

## Montecarlo.py

This is an important point to notice.

[[Monete Carlo simulation]]

Since the sampling of the energy landscape is easier done in the higher temperatures when in the lower temperature we need to be very careful since the system can fall into a steep nonglobal minima which hinders the exploration of the energy landscape and does not provide the optimal configuration for a given temperature(For a low enough temperature). 

Thus we must be cautious to not allow this to occur. and hence we use a different method to explore the global energy landscape more accurately. 


___ 

## Parallel tempering.py 

This is the essential ingredient in trying to explore the global landscape. We use multiple replicas of the same system and assign a different temperature for each of them. We can thus explore a wider range of energy landscape. We finally exchange two configurations with their temperatures so the respective configurations do not fall into a steep non-global minima. 

Thus by the end our replicas would have explored a wide range of energies and we can choose the one with the lowest temperature as our system of interest. 

The exchange occurs through probability. The probability of which is defined as follows: $$ \huge 
P(exchange) = min(1, e^{(\beta_{i}-\beta_{j})\cdot (E_{i}-E_{j})})
$$
This essentially ensures that the swap that does occur only does happen more frequently for two configurations that are close by and it becomes increasingly rare for two configurations that are far in energy and temeperature. 

Overall a cascading effect occurs where each configuration successfully explores a wider range of the energy curve, thereby increasing the chances of finding the global minima. 

One extra step needs to be implemented in this algorithm in my opinion, that being the fact that after choosing the configuration of interest we need to let the system further evolve for a longer time in montecarlo so that it reaches the pit of the global minima. 


[[Parallel Tempering]]


___ 

## Geometric spin symplectic integrator 

This is how we are going to evolve the system with respect to time. 
We essentially let the system evolve making sure that the spin and the energy(total spin and energy) of the system remains conserved at all times. 

The recommended formula to approach this question was found in this paper: 

![[1402.4114v2.pdf]]

I derived the formula for the nth time step for the ith spin to be:$$ \huge 
S_{n_{1}} = S_{n} + \Delta t( S_{mid}\times B(S_{mid}))
$$

Where the S mid is the midpoint of the new and the old configuration. 
$$ \huge 
S_{mid} = \frac{S_{n+1}+{S_{n}}}{|S_{n+1}+S_{n}|}
$$
Where under the mod function the spins return back to the sphere and remain normalized at every step. 

The computation of the midpoint we iterate over (similar to other midpoint convergence algorithms) before moving on to the next time step. To make sure that the system approaches the closest value possible before we change and move onto the next spin. 

___ 
## Problem 

Currently the simulation runs well however as I let it evolve over time the energy changes in the system. Which is very concerning. Since the system should have conserved quantities. 

The problem could be because of the following: 

1. Normalization not occuring at the correct time 
2. montecarlo did not get the lowest energy state. 
3. A genuine problem with the algorithm logically 

There are more but these seem to be most likely. 

___ 

## Generating the lattice structure

This is one of the most important parts of the program and I need to be very careful in determining how the system would behave if I gave it different parameters. In general I would like the program to simply give me the position numerically of the spin and it's associated neighbours. This is enough. 

However this might be harder for complex graphs. 

___ 

## Frustrated spins 

Chaos and statistical mechanics share a deeply intimate relationship that allow for us to link the chaotic dynamics as well as ergodicity and thermalization. 

The ability of the system to be exponentially sensitive to initial conditions gives rise to non-trivial consequences when we cogitate upon the physical system at hand. 

The paper that I have choosen to study tries to approach the chaotic evolution in the light of temperature and thermalization. This basically means that we would like to see how the chaos in the system scales as a function of temperature. 

- One expects that in the lower energy limit we observe that the dynamics of the system is dominated by the emergence of long lived quasi particles. Hence hindering the total effect of chaos. However even without the existence of such particles we observe in this paper that even at the lowest of T, chaos can manifest at the hands of OTOCs(classical). 
- We try to find this in this numerical simulation by trying to come up the butterfly velocity which shows us how fast a perturbation in the system can propagate and relate it to the lyapnov exponent while seeing how temperature affects this value. 

- Why is the system not relaxing even at the lowest of temperature and why do we have reason to belive that the chaotic regime still holds in our system? 
	- this is because we choose a frustrated spin system. They completely supress ordering even at the low temperature limit. 
- We thus try to study a magnetic frustrated spin model on a kagome lattice. With the hamiltonian looking as follows:$$ \huge 
H = J \sum_{x,x'} S_{x}\cdot S_{y}
$$
This leads to a macroscopically degenerate state even at a lower temperature. 
- The system does not freeze or fall outside of equilibrium in the whole temperature range. Z2 spin liquid. 

