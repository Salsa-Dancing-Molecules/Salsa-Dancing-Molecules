"""Unit test for mean_square_displacement.py."""

import pytest
from ..mean_square_displacement import calculate_msd
from unittest.mock import Mock


atoms = Mock()
atoms2 = Mock()
atoms.__len__ = Mock(return_value=2)
atoms.get_cell_lengths_and_angles.return_value = [10, 10, 10]
atoms.get_positions.return_value = [[1, 1, 1], [2, 2, 2]]
atoms2.get_positions.return_value = [[9, 9, 9], [3, 3, 3]]
configs = [atoms, atoms2]


def test_mean_square_displacement():
    """Function for testing the mean square displacement calculation."""
    result = calculate_msd(configs)
    test_success = (7.5, 0)
    assert result == pytest.approx(test_success, 0.0001)
