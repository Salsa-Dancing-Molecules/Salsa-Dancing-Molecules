"""Unittest for pressure.py."""

import pytest
from ..pressure import get_pressure
from .mock_atoms import atoms


def test_pressure():
    """Function for testing pressure.py."""
    # set up a mock atoms-object
    a = atoms()

    X = get_pressure(a)
    Y = 9.50705759354618  # This is the value the calculation should give
    assert X == pytest.approx(Y, 0.00001)
