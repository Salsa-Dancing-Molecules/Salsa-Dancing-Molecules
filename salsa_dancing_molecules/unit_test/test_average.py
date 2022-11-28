"""Unittest for average.py."""

import pytest
from ..average import average
import numpy as np


def test_average():
    """Test for time avarege of array."""
    t0 = 4
    array = [1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
    np.array(array)
    result = average(t0, array)
    expected = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
                5.142857142857143, 5.25, 5.333333333333333,
                5.4, 5.454545454545454]
    assert result == pytest.approx(expected, 0.0001)
