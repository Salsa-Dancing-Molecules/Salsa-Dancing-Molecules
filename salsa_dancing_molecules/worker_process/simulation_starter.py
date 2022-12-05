"""Module for determining which simulation program to be used."""


def start_simulation(simulation_info, atoms_object):
    """Take data on the simulation and send it to the correct module.

    Args:
        simulation_info: Dictionary with information on the simulation.
        atoms_object: Material to be used for the simulation.
    """
    print(simulation_info["ensemble"])
    print(simulation_info["potential"])
    if (simulation_info["ensemble"] == "nve" and
            simulation_info["potential"] == "lennard_jones"):
        from ..simulations import nve
        print(simulation_info["steps"])
        print(simulation_info["output_path"])
        print(simulation_info["use_asap"])
        nve.run(atoms_object,
                simulation_info["steps"],
                simulation_info["output_path"],
                simulation_info["use_asap"])
