"""Calculate ensemble energy and ensemble square energy."""
import numpy as np
from .average import average
import ase


def get_mean_square_of_kin(config, t0):
    """Calculate enesemble average of square of kinetic energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of mean square of the kinetic energy.
              time average over equalibrium.
    """
    mean_square_of_kin = [
        ((a.get_kinetic_energy())**2) for a in config
        ]
    return average(t0, mean_square_of_kin)


def get_square_of_mean_kin(config, t0):
    """Calculate square of enesemble average of kinetic energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of the square of mean kinetic energy.
              time average over equalibrium.
    """
    square_of_mean_kin = [
        a.get_kinetic_energy() for a in config
        ]
    return np.power(average(t0, square_of_mean_kin), 2)


def get_square_of_mean_tote(config, t0):
    """Calculate square of enesemble average of total energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of the square of mean total energy.
              time average over equalibrium.
    """
    square_of_mean_tote = [
        (a.get_total_energy()) for a in config
        ]
    return np.power(average(t0, square_of_mean_tote), 2)


def get_mean_square_of_tote(config, t0):
    """Calculate enesemble average of square of total energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of mean square of the total energy.
              time average over equalibrium.
    """
    mean_square_of_tote = [
        (a.get_total_energy()**2) for a in config
        ]
    return average(t0, mean_square_of_tote)
