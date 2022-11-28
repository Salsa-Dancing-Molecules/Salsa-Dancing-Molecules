"""Unittest for ensamble_eneries.py."""

import pytest
from .. import ensemble_energies
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
    atoms.get_momenta.return_value = [[1, 1, 1], [2, 2, 2], [1, 1, 1]]


def test_kinetic_energies():
    """Function for testing pressure.py."""
    init_mock()
    result = ensemble_energies.get_kinetic_energies(atoms)
    # Calculated expected calue
    expected = [0.8660254037844386, 3.4641016151377544, 0.8660254037844386]
    assert result == pytest.approx(expected, 0.0001)


def test_square_of_mean_kin():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_square_of_mean_kin(config, t0)
    expected = [0.1111111111111111, 0.1111111111111111, 0.1111111111111111]
    assert result == pytest.approx(expected, 0.0001)


def test_mean_square_of_kin():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_mean_square_of_kin(config, t0)
    # Calculated expected value
    expected = [4.499999999999999, 4.499999999999999, 4.499999999999999]
    assert result == pytest.approx(expected, 0.0001)


def test_square_of_mean_tote():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_square_of_mean_tote(config, t0)
    expected = [0.1111111111111111, 0.1111111111111111, 0.1111111111111111]
    assert result == pytest.approx(expected, 0.0001)


def test_mean_square_of_tote():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_mean_square_of_tote(config, t0)
    # Calculated expected value
    expected = [8.964101615137755, 8.964101615137755, 8.964101615137755]
    assert result == pytest.approx(expected, 0.0001)
