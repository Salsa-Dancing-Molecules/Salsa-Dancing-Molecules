"""Calculates the specific heat capacity for an NVE ensamble."""

import numpy as np
from ase import units
from ase.io.trajectory import Trajectory
from .ensemble_energies import (get_mean_square_of_kin,
                                get_square_of_mean_kin)
from .average import average


def get_NVE_heat_capacity(traj, t0):
    """Calculat Heat Capacity for a NVE ensamble.

    Input:
        traj: str    - trajectory-file
        t0: int      - timestep when equilibrium starts

    Output:
        int - time average heat capacity, time average over equalibrium
    """
    config = Trajectory(traj)
    return calculate_NVE_heat_capacity(config, t0)


def calculate_NVE_heat_capacity(config, t0):
    """Calculate Heat Capacity for NVE snemble.

    Imput:
        config: ase.io.trajectory.Trajectory -traj-file containing atom objects
        t0: int                              -timestep when equilibrium starts

    Output:
        int - time average heat capacity, time average over equalibrium
    """
    a = config[-1]
    N = len(a)
    mass = sum(a.get_masses())*units._amu  # change mass from u to kg
    temperatures = [atom.get_temperature() for atom in config]
    # equilibrium time average of resp.
    T = average(t0, temperatures)[-1]
    mean_square = get_mean_square_of_kin(config, t0)[-1]
    square_of_mean = get_square_of_mean_kin(config, t0)[-1]
    return (N*units._k*1.5/(1 - (mean_square - square_of_mean)
                            / (1.5*(T**2)*units.kB**2)))/mass
