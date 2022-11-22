def start_simulation(simulation_info, atoms_object):
    if (simulation_info["ensemble"] == "nve" &
        simulation_info["potential"] == "lennard_jones"):
        from ..simulations import nve
        nve.run(atoms_object,
                simulation_info["steps"],
                simulation_info["output_path"],
                simulation_info["use_asap"])