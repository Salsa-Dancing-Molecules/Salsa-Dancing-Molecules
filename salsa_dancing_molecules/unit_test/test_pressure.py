"""Unittest for pressure.py."""

import pytest
from ase import units
from unittest.mock import Mock
from ..pressure import get_pressure


def test_pressure():
    """Function for testing pressure.py."""
    # set up a mock atoms-object
    a = Mock()
    a.get_kinetic_energy.return_value = 1229 * units.kB
    a.get_positions.return_value = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    a.get_forces.return_value = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    a.get_volume.return_value = 10
    a.__len__ = Mock(return_value=3)

    X = get_pressure(a)
    Y = 9.50705759354618  # This is the value the calculation should give
    assert X == pytest.approx(Y, 0.00001)
