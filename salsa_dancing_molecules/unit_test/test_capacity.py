"""Unittest for capacity_NVT.py and capacity_NVE.py."""
from .. import capacity_NVE
from .. import capacity_NVT
from ase import units
from unittest.mock import Mock
import pytest

# Mock-atom object
atoms = Mock()


def init_mock():
    """Init mock object for use in the tests."""
    # Mock atom attribute and funtion
    atoms.__len__ = Mock(return_value=1)
    atoms.get_temperature.return_value = 1
    atoms.get_kinetic_energy.side_effect = [1, 1, 1, 1, 1, 1, 1,
                                            2, 2, 2, 2, 2, 2, 2, 2]
    atoms.get_total_energy.side_effect = [1, 1, 1, 1, 1, 1, 1,
                                          2, 2, 2, 2, 2, 2, 2, 2]
    atoms.get_masses.return_value = [1, 1, 1]


def test_capacity_NVE():
    """Test case for NVT capacity."""
    init_mock()
    configs = [atoms, atoms, atoms, atoms, atoms, atoms, atoms]
    t0 = 2
    # Mock funtions
    mock_mass = 3 * units._amu
    #  caluculated test value was derived with units eV/K, unit_conversion
    # changes it to J/(K*kg)
    unit_conversion = units._e*units.kB / mock_mass
    V = 2 / ((units.kB**2)*3)
    expected = 1.5 * unit_conversion / (1 - 3*V)
    result = capacity_NVE.calculate_NVE_heat_capacity(configs, t0)
    assert result == pytest.approx(expected, 0.0001)


def test_capacity_NVT():
    """Test case for NVT capacity."""
    init_mock()
    configs = [atoms, atoms, atoms, atoms, atoms, atoms, atoms]
    t0 = 2
    # Mock funtions
    mock_mass = 3 * units._amu
    # calculated test value was derived with units eV/K, unit_conversion
    #  changes it to J/(K*kg)
    unit_conversion = units._e/(mock_mass*units.kB)
    expected = 3 * unit_conversion
    result = capacity_NVT.calculate_NVT_heat_capacity(configs, t0)

    assert result == pytest.approx(expected, 0.0001)
