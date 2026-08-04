# this is the dynamics engine to run the simulation with respect to time.
#
#
from SpinSystem import SpinSystem
import numpy as np
from Lattice.Chain import create_chain
from Parallel_Tempering import Rep_exchange_mont


# From the output of the parallel tempering take out the system with the least amount of temeprature 
# Then use the system to take the mipoint of all the spins. Evolve accordingly. 
#
#
targetsystem = replica[0]




def midpoint_calc(spin, SpinSystem,targetsystem ): 
    midpoints =[]
    oldspinconfig = targetsystem.copy()
    newspinconfig = oldspinconfig.copy()

    # Assuming that I have high resolution oldspin = new spin 
    #
    for  i in range(oldspinconfig.spin.N)
        midpoint_temp = oldspinconfig[i].spin + newconfig[i].spin / abs(oldspinconfig[i].spin + newspinconfig[i].spin)

        midpoints.append(midpoint_temp)

    return midpoints 
    


def time_evolution(
    SpinSystem,
    replicas,
    Time,
    targetsystem
):
    

    for i in range(Time):

        for i in range(oldspinconfig.spin.N) : 
            
            midpoints = midpoint_calc(spin, SpinSystem,targetsystem) 

            newspinconfig[i].spin = oldspinconfig + timestep * ( np.cross(midpoints[i], oldspinconfig[i].local_field)) 

            oldspinconfig[i] = newspinconfig[i]


    return newspinconfig 




