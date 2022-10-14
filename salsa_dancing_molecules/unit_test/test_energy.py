"""Unittest for energy_calc.py."""

import pytest
from ..energy import get_energy, get_potential_energy, get_kinetic_energy
from .mock_atoms import atoms


def test_total_energy():
    """Test the total energy of a created atoms object."""
    a = atoms()

    assert get_energy(a) == get_kinetic_energy(a) \
           + get_potential_energy(a)


def test_kinetic_energy():
    """Test the kinetic energy of a created atoms object."""
    a = atoms()

    assert get_kinetic_energy(a) == 15/3


def test_potential_energy():
    """Test the potential energy of a created atoms object."""
    a = atoms()

    assert get_potential_energy(a) == 20/3
