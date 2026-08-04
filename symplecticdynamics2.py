import numpy as np

from Parallel_Tempering import Rep_exchange_mont

# system = replica[0]


def midpoint_configuration_calculator(new, old):

    midpoints = np.zeros_like(old.spin)

    for i in range(system.spin.N):
        midpoint_temp = new.spin[i] + old.spin[i]

        midpoint_temp /= np.linalg.norm(midpoint_temp)

        midpoints[i] = midpoint_temp

    return midpoints


def time_step(system, dt, total_time):

    new = system.copy()
    old = system.copy()

    num_steps = int(total_time / dt)

    for step in range(num_steps):
        # Initial guess for the implicit solve
        new = old.copy()

        for iteration in range(1000):
            previous = new.copy()

            # Compute midpoint configuration
            midpoints = midpoint_configuration_calculator(new, old)

            # Update every spin
            for i in range(new.spin.N):
                midpoint_field = system.Local_field(i, midpoints)

                new.spin[i] = old.spin[i] + dt * np.cross(midpoints[i], midpoint_field)

            # Convergence test
            error = np.max(np.linalg.norm(new.spin - previous.spin, axis=1))

            if error < 1e-10:
                break

        # Advance to the next timestep
        old = new.copy()

    return new
