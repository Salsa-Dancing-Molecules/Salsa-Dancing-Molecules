"""Functionfile for energy.

Functions to get average energy, potential energy and
kinetic energy of each atom in an atoms object.
"""


def get_energy(atoms):
    """Get average total energy of each atom."""
    return get_potential_energy(atoms) + get_kinetic_energy(atoms)


def get_potential_energy(atoms):
    """Get average potential energy of each atom."""
    return atoms.get_potential_energy() / len(atoms)


def get_kinetic_energy(atoms):
    """Get average kinetic energy of each atom."""
    return atoms.get_kinetic_energy() / len(atoms)
