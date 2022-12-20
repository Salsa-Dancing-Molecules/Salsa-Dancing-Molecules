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
    atoms.get_kinetic_energy.return_value = 2
    atoms.get_total_energy.return_value = 2


def test_square_of_mean_kin():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_square_of_mean_kin(config, t0)
    expected = [4, 4, 4]
    assert result == pytest.approx(expected, 0.0001)


def test_mean_square_of_kin():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_mean_square_of_kin(config, t0)
    # Calculated expected value
    expected = [4, 4, 4]
    assert result == pytest.approx(expected, 0.0001)


def test_square_of_mean_tote():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_square_of_mean_tote(config, t0)
    expected = [4, 4, 4]
    assert result == pytest.approx(expected, 0.0001)


def test_mean_square_of_tote():
    """Function for testing pressure.py."""
    init_mock()
    t0 = 1
    config = [atoms, atoms, atoms, atoms]
    result = ensemble_energies.get_mean_square_of_tote(config, t0)
    # Calculated expected value
    expected = [4, 4, 4]
    assert result == pytest.approx(expected, 0.0001)
