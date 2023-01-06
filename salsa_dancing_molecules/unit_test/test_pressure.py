"""Unittest for pressure.py."""

import pytest
from ase import units
from unittest.mock import Mock
from ..pressure import get_pressure


def test_pressure():
    """Function for testing pressure.py."""
    # set up a mock atoms-object, values in the mock objcet are chosen so
    # that get_pressure will return 2 and each term the return summation is
    # equal to 1
    e = units._e
    a = Mock()
    a.get_kinetic_energy.return_value = 4.5*units.kB/units._k
    a.get_positions.return_value = [[1, 1, 1], [1, 1, 1],
                                    [1, 1, 1]]
    a.get_forces.return_value = [[1/e, 1/e, 1/e], [1/e, 1/e, 1/e],
                                 [1/e, 1/e, 1/e]]
    a.get_volume.return_value = 3*1*1e30
    a.__len__ = Mock(return_value=3)

    X = get_pressure(a)
    Y = 2  # This is the value the calculation should give
    assert X == Y
