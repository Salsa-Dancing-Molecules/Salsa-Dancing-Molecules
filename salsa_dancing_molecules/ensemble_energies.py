"""Calculate ensemble energy and ensemble square energy."""
import numpy as np
from .average import average


def get_kinetic_energies(a):
    """Get the kinetic energy.

    Input:
        a: atom-object

    Output:
        array - array of kinetic energies of each atom.
    """
    kinetic_energies = []
    momenta = a.get_momenta()
    xyz_kin = 0.5 * np.multiply(momenta, a.get_velocities())
    for k in xyz_kin:
        kinetic_energies.append(np.sqrt(np.dot(k, k)))
    return np.asarray(kinetic_energies)


def get_mean_square_of_kin(config, t0):
    """Calculate enesemble average of square of kinetic energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of mean square of the kinetic energy for an atom.
              time average over equalibrium.
    """
    mean_square_of_kin = []
    for a in config:
        kinetic = get_kinetic_energies(a)
        kin_avrs = np.dot(kinetic, kinetic) / len(a)
        mean_square_of_kin.append(kin_avrs)
    return average(t0, mean_square_of_kin)


def get_square_of_mean_kin(config, t0):
    """Calculate square of enesemble average of kinetic energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of the square of mean kinetic energy of one atom.
              time average over equalibrium.
    """
    square_of_mean_kin = [
        ((a.get_kinetic_energy() / len(a))**2) for a in config
        ]
    return average(t0, square_of_mean_kin)


def get_square_of_mean_tote(config, t0):
    """Calculate square of enesemble average of total energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of the square of mean total energy of one atom.
              time average over equalibrium.
    """
    square_of_mean_tote = [
        ((a.get_total_energy() / len(a))**2) for a in config
        ]
    return average(t0, square_of_mean_tote)


def get_mean_square_of_tote(config, t0):
    """Calculate enesemble average of square of total energy.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average of mean square of the total energy for an atom.
              time average over equalibrium.
    """
    mean_square_of_tote = []
    for a in config:
        etot = get_kinetic_energies(a) + a.get_potential_energies()
        mean_square_of_tote.append(np.dot(etot, etot) / len(a))
    return average(t0, mean_square_of_tote)
