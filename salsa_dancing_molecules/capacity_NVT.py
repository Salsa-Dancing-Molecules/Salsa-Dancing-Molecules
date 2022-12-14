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
    # equilibrium time average
    T = average(t0, temperatures)[-1]
    square_of_mean = get_square_of_mean_tote(config, t0)[-1]
    mean_square = get_mean_square_of_tote(config, t0)[-1]

    conversion = units._e / mass
    variance = mean_square - square_of_mean

    return conversion * variance / (units.kB*(T**2))
