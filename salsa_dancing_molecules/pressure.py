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

    return ((len(atoms)*units.kB*get_temperature(atoms))/atoms.get_volume() +
            (1/(3*atoms.get_volume()))*dot_product)
