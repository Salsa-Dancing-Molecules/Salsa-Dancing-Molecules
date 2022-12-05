"""Unittest for capacity_NVT.py and capacity_NVE.py."""
from .. import capacity_NVE
from .. import capacity_NVT
from unittest.mock import Mock
import pytest

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
    atoms.get_momenta.return_value = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


def test_capacity_NVE():
    """Test case for NVT capacity."""
    init_mock()
    configs = [atoms, atoms, atoms, atoms, atoms, atoms, atoms]
    t0 = 2
    # Mock funtions
    expected = -1.1518362268490951e-12  # Calculated expected value
    result = capacity_NVE.calculate_NVE_heat_capacity(configs, t0)

    assert result == pytest.approx(expected, 0.0001)


def test_capacity_NVT():
    """Test case for NVT capacity."""
    init_mock()
    configs = [atoms, atoms, atoms, atoms, atoms, atoms, atoms]
    t0 = 2
    # Mock funtions
    expected = 109618.08417520954  # Calculated expected value
    result = capacity_NVT.calculate_NVT_heat_capacity(configs, t0)

    assert result == pytest.approx(expected, 0.0001)
