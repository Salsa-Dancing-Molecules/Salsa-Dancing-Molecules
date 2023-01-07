"""Unittest for energy_calc.py."""

import pytest
from ..force import get_force
from .mock_atoms import atoms


def test_force():
    """Function for testing force_calc.py."""
    a = atoms()
    X = get_force(a)

    # Mock atoms object gives a 3x3 vector with value 5 in the middle
    assert len(X) == 3 and X[1][1] == 5
