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
    MSD, _ = calculate_msd(configs, 0)
    test_success = (7.5, 0)
    assert MSD == pytest.approx(test_success, 0.0001)


def test_mean_square_displacement_time_average():
    """Function for testing the mean square displacement calculation."""
    _, MSD_avr = calculate_msd(configs, 0)
    test_success = (7.5, 7.5 / 2)
    assert MSD_avr == pytest.approx(test_success, 0.0001)
