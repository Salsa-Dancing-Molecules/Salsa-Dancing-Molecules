"""Calculate cohesive energy."""

from asap3 import Trajectory


def get_cohesive_energy(traj_file, t0):
    """Calculate cohesive energy.

    Input:
        traj_file: str  - filename of trajectory file
        t0: int         - timestep when equilibrium starts

    Output:
        cohesive energy for the system (in eV/atom): float

    """
    configs = Trajectory(traj_file)
    pot_energies = [atom.get_potential_energy() for atom in configs]
    avg_pot_e = (sum(pot_energies[t0:]) / len(pot_energies[t0:]))

    return calculate_cohesive_energy(configs, avg_pot_e)


def calculate_cohesive_energy(configs, avg_pot_e):
    """Calculate cohsive energy from time average potential energy.

    Input:
        configs:ase.io.trajectory.Trajectory -traj file containing atom objects
        avg_pot_e: float               -average potential energy at equilibrium

    Output:
        cohesive energy for the system: float

    """
    return -(avg_pot_e / configs[-1].get_global_number_of_atoms())
