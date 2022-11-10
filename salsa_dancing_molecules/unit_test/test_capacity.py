"""Unittest for capacity_NVT.py and capacity_NVE.py."""

from ..calculator import capacity_NVE, capacity_NVT
from unittest.mock import Mock
from ase import units

# Mock-atom object
atoms = Mock()


def init_mock():
    """Init mock object for use in the tests."""
    # Mock atom attribute and funtion
    atoms.__len__ = Mock(return_value=1)
    atoms.get_temperature.return_value = 1
    atoms.get_kinetic_energy.return_value = 1
    atoms.get_total_energy.return_value = 1
    atoms.get_potential_energies.return_value = [1, 1, 1]
    atoms.get_velocities.return_value = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    atoms.arrays.get.return_value = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


def test_capacity_NVE():
    """Test case for NVT capacity."""
    init_mock()

    # Mock funtions
    expected = -1.1518362268490951e-12  # Calculated expected value
    result = capacity_NVE.get_NVE_heat_capacity(atoms)

    assert expected == result


def test_capacity_NVT():
    """Test case for NVT capacity."""
    init_mock()

    # Mock funtions
    expected = 109618.08417520954  # Calculated expected value
    result = capacity_NVT.get_NVT_heat_capacity(atoms)

    assert expected == result
