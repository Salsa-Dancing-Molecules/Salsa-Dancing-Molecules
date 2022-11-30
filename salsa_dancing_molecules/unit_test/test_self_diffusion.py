"""Unit test for self_diffusion_coefficient.py."""

import pytest
from ..self_diffusion_coefficient import calculate_self_diffusion_coefficient
from unittest.mock import Mock

MSD = [0, 7.5]
t0 = 0


def test_self_diffusion_coefficient():
    """Function for testing the self diffusion coefficient."""
    result = calculate_self_diffusion_coefficient(MSD, t0)
    test_success = 0.625
    assert result == pytest.approx(test_success, 0.0001)
