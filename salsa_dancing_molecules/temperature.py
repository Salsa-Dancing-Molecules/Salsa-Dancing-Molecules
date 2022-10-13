"""Module for calculating temperature of atoms object."""
from ase import units
from .energy import get_kinetic_energy


def get_temperature(atoms):
    """Calculate average temperature of atoms object.

    Arguments:
        atoms - ASE atoms object

    Returns:
        temperature - float
    """
    return get_kinetic_energy(atoms)/(1.5*units.kB)
