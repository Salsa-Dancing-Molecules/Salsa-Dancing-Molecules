"""Calculates the specific heat capacity for an NVT ensamble."""

import numpy as np
from ase import units
from ase.io.trajectory import Trajectory
from .ensemble_energies import (get_square_of_mean_tote,
                                get_mean_square_of_tote)
from .average import average


def get_NVT_heat_capacity(traj, t0):
    """Calculat Heat Capacity for a NVT ensamble.

    Input:
        traj: str    - trajectory-file
        t0: int      - timestep when equilibrium starts

    Output:
        int - time average heat capacity, time average over equalibrium
    """
    config = Trajectory(traj)
    return calculate_NVT_heat_capacity(config, t0)


def calculate_NVT_heat_capacity(config, t0):
    """Calculat Heat Capacity for a NVT ensamble.

    Input:
        traj: ase.io.trajectory.Trajectory  - traj file containing atom objects
        t0: int                             - timestep when equilibrium starts

    Output:
        int - time average heat capacity, time average over equalibrium
    """
    a = config[-1]
    mass = sum(a.get_masses())*units._amu  # change mass from u to kg

    temperatures = [atom.get_temperature() for atom in config]
    # equilibrium time average of resp.
    T = average(t0, temperatures)[-1]
    squar_of_mean = get_square_of_mean_tote(config, t0)[-1]
    mean_squar = get_mean_square_of_tote(config, t0)[-1]
    # return is in eV/(K * kg) so we need a unit conversion to change it to
    # J/(K * kg)
    eV_to_J = units._e

    print(eV_to_J/(mass*units.kB*(T)**2))
    return eV_to_J*((mean_squar - squar_of_mean) / (units.kB*(T**2)))/mass
