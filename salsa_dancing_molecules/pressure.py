"""Module for calculating the internal pressure of an atoms-object."""

from numpy import sum, multiply
from ase import units
from .temperature import get_temperature


def get_pressure(atoms):
    """Calculate the pressure for an atoms object.

    arguments:
        atoms - ASE atom object

    return:
        pressure - float
    """
    # sum of position vector and forces vector:
    dot_product = sum(multiply(atoms.get_positions(), atoms.get_forces()))

    # a conversion from ångström to meter is needed to get the answer in Pa
    a_to_m = 1e-10

    return ((len(atoms)*units._k*get_temperature(atoms) /
            ((a_to_m**3)*atoms.get_volume()) +
            (1/(3*(a_to_m**2)*atoms.get_volume()))*dot_product))
