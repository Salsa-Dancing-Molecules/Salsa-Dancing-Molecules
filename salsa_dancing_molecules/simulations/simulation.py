"""Module for running a simulation."""


def run(sim_info, atoms):
    """Run the simulation.

    Args:
        sim_info - dictionary with information on the simulation.
        atoms - atoms object to be used.
    """
    # TODO: implement real simulation
    f = open(sim_info["traj_output_path"], "w")
    f.write(sim_info["potential"])
    f.close()
    f = open(sim_info["csv_output_path"], "w")
    f.write(sim_info["ensemble"])
    f.close()
