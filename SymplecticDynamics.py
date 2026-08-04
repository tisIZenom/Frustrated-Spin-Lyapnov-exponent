import numpy as np 
from Parallel_Tempering import Rep_exchange_mont

replica =  Rep_exchange_mont(spin)
system = replica[0]

def midpoint_configuration_calculator(new, old): 

    midpoints = np.zeros_like(old.spin)

    for i in range(system.spin.N):
        midpoint_temp_1 = new.spin[i]+old.spin[i]
 
        midpoint_temp_2 = midpoint_temp_1 / np.linalg.norm(midpoint_temp_1)

        midpoints.append(midpoint_temp_2)


    return midpoints


def time_step(system, time_step_resolution, total_time): 

    new = system.copy()
    old = system.copy()

    for i in range(time_step_resolution * total_time)
        

        # now comes the time step ;
        # this is for 1 spin only 


        #iterate to get a better approximation 
        
        
        for j in range(1000): 
            midpoints = midpoint_configuration_calculator(new,old)

            for i in range(new.spin.N):
                midpoint_field = system.Local_field(i,midpoints)
                

                new.spin[i] = old.spin[i] + time_step_resolution * (np.cross(midpoints.[i], midpoint_field)) 

                temp_spin = new.copy()
                if np.max(np.linalg.norm(new.spin[i] - temp_spin.spin[i])) < 1e -10:
                     break 


        old = new.copy()


    system = new 

    return system 







