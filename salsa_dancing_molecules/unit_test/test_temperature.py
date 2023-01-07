"""Unittest for temperature.py."""
import pytest
from ..temperature import get_temperature
from .mock_atoms import atoms


def test_temperature():
    """Test if the correct value is calculated when using mock atoms object.

    The expected value is given by using the formula in physics handbook.
    """
    a = atoms()
    assert get_temperature(a) == pytest.approx(38681.74)
