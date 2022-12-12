"""Unit test for debye_temperature.py."""

import pytest
from ..debye_temperature import calculate_debye
from unittest.mock import Mock

atoms = Mock()
atoms.__len__ = Mock(return_value=2)
configs = [atoms]
temperature = 20
specific_heat_capacity = 3


def test_debye_temperature():
    """Function for testing the debye temperature calculation."""
    result = (calculate_debye(configs, temperature,
              specific_heat_capacity))
    test_success = 2.582047321497842e-06, True
    assert result == pytest.approx(test_success, 0.0001)
