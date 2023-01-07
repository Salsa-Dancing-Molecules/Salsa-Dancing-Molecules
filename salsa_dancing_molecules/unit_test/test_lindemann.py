"""Unit test for lindemann.py."""

import pytest
from ..lindemann import calculate_lindemann_parameter


def test_lindemann_parameter():
    """Test calculation of lindemann parameter."""
    a = 5
    msd = [0.2, 0.2, 0.1, 0.1]
    msd_avr = 0.15
    result, _ = calculate_lindemann_parameter(a, msd, msd_avr, 'FCC')
    expected = [0.12649, 0.12649, 0.08944, 0.08944]
    assert result == pytest.approx(expected, 0.0001)


def test_true_criterion():
    """Test that lindemann criterion is true."""
    a = 5
    msd = [0.1, 0.1, 0.1, 0.1]
    msd_avr = 0.08944
    _, result = calculate_lindemann_parameter(a, msd, msd_avr, 'FCC')
    assert not result


def test_false_criterion():
    """Test lindemann criterion is violated."""
    a = (2 ** (1/2))
    msd = [2, 3, 3, 3, 3]
    msd_avr = 14 / 5
    _, result = calculate_lindemann_parameter(a, msd, msd_avr, 'BCC')
    assert result
