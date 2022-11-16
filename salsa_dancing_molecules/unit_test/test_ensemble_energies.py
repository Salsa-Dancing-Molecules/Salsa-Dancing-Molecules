"""Unittest for ensamble_eneries.py."""

import pytest
from ..calculator import ensemble_energies
from .mock_atoms import atoms
from unittest.mock import Mock


# Mock-atom object
atoms = Mock()


def init_mock():
    """Init mock object for use in the tests."""
    # Mock atom attribute and funtion
    atoms.__len__ = Mock(return_value=3)
    atoms.get_kinetic_energy.return_value = 1
    atoms.get_total_energy.return_value = 1
    atoms.get_potential_energies.return_value = [1, 1, 1]
    atoms.get_velocities.return_value = [[1, 1, 1], [2, 2, 2], [1, 1, 1]]
    atoms.arrays.get.return_value = [[1, 1, 1], [2, 2, 2], [1, 1, 1]]


def test_kinetic_energies():
    """Function for testing pressure.py."""
    init_mock()
    result = ensemble_energies.get_kinetic_energies(atoms)
    # Calculated expected calue
    expected = [0.8660254037844386, 3.4641016151377544, 0.8660254037844386]
    assert all(expected == result)


def test_kin_ensemble_sqr():
    """Function for testing pressure.py."""
    init_mock()
    result = ensemble_energies.get_kine_ensemble_sqr(atoms)
    expected = 0.1111111111111111
    assert expected == result


def test_kin_sqr_ensemble():
    """Function for testing pressure.py."""
    init_mock()
    result = ensemble_energies.get_kine_sqr_ensemble(atoms)
    expected = 4.499999999999999  # Calculated expected value
    assert expected == result


def test_etot_ensemble_sqr():
    """Function for testing pressure.py."""
    init_mock()
    result = ensemble_energies.get_tot_e_ensemble_sqr(atoms)
    expected = 0.1111111111111111
    assert expected == result


def test_etot_sqr_ensemble():
    """Function for testing pressure.py."""
    init_mock()
    result = ensemble_energies.get_tot_e_sqr_ensemble(atoms)
    expected = 8.964101615137755  # Calculated expected value
    assert expected == result
