"""Unittest for lennardjonesparse.py."""

import pytest
from ..lennardjonesparse import parse_lj_params


def test_lj():
    """Function for lennardjonesparse.py."""
    r_c, epsilon, sigma = parse_lj_params('H')

    assert r_c == 2.20943 and epsilon == 4.47789 and sigma == 0.552357
