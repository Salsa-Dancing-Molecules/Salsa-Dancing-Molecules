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
    print(f"t0 = {t0}")
    print(f"t_max = {len(config)}")
    T = average(t0, temperatures)[-1]
    square_of_mean = get_square_of_mean_kin(config, t0)[-1]
    mean_square = get_mean_square_of_kin(config, t0)[-1]
    # return is in eV/(K * kg) so we need a unit conversion to change it to
    # J/(K * kg)
    print(f"kinetic = {a.get_kinetic_energy()}")
    print(f"N = {N}")
    print('mean square',mean_square, 'sqr of mean', square_of_mean, 'Diff: ', mean_square-square_of_mean)
    eV_to_J = units._e
    variance = mean_square - square_of_mean
    C_v = ((3 * units.kB)/2) * N * ((1 - (2 * variance / (3 * N * units.kB**2 * T**2)))**(-1))
    C_v_J = C_v * eV_to_J
    print(f"C_v = {C_v}, mass = {mass}, C_v to J = {C_v_J}, C_v_J/mass = {C_v_J/mass}")

    return C_v_J/mass
