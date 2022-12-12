"""Module for determining which simulation program to be used."""
from ..simulations.simulation import run
from asap3 import AsapError


def start_simulation(sim_info, atoms):
    """Take data on the simulation and send it to the correct module.

    Args:
        simulation_info: Dictionary with information on the simulation.
        atoms_object: Material to be used for the simulation.
    """
    repeat = int(sim_info["repeat"])
    symbols = atoms.symbols

    """pbc will start as True and will only change if "False" is given """
    if "pbc" in sim_info:
        not_pbc = (sim_info["pbc"] == "False")
        if not_pbc:
            atoms.set_pbc(False)

    if repeat > 0:
        atoms = atoms.repeat(repeat)

    while True:
        try:
            print(f'Simulating for {symbols}')
            run(sim_info, atoms)
        except ValueError as e:
            print(f'Size error for {symbols}: {e}')
            # failsafe against automatic increase of cells becomes too
            # large
            if repeat > 5:
                print('Stopping automatic increase of amount of cells due to '
                      'too large amount of cells, changing potential to ASAP '
                      'Lennard-Jones')
                print('Use repeat = X to manually change to larger amount'
                      'of cells')
                sim_info["use-asap"] = "True"
                sim_info["potential"] = "lennard-jones"
                run(sim_info, atoms)
            else:
                repeat = repeat + 1
                print('Increasing amount of cells, repeat = '+str(repeat))
                atoms = atoms.repeat(repeat)
        except AsapError as e:
            print(f'ASAP3 error for {symbols}: {e}')
            print('Trying without ASAP3...')
            sim_info["potential"] = "lennard-jones"
            sim_info["use-asap"] = "False"
            run(sim_info, atoms)
            break
        # else will only be executed if there is no error
        else:
            break
