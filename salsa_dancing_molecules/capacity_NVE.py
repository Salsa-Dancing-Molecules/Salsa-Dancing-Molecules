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
    # equilibrium time average
    T = average(t0, temperatures)[-1]
    square_of_mean = get_square_of_mean_kin(config, t0)[-1]
    mean_square = get_mean_square_of_kin(config, t0)[-1]
    # return is in eV/(K * kg) so we need a unit conversion to change it to
    # J/(K * kg)
    variance = mean_square - square_of_mean
    conversion = units._e * 1.5 * units.kB * N
    C_v_J = conversion * ((1 - (variance / (1.5 * N * (units.kB*T)**2)))**(-1))

    return C_v_J/mass
