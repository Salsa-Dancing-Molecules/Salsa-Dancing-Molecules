"""Unit tests for the optimade module."""
from ..optimade import adapters

from ase import Atoms


def test_anonymous_formula():
    """Test anonymous formula generation."""
    a = Atoms('C2H5OH')
    assert adapters.get_anonymous_formula(a) == 'A6B2C'


def test_get_unique_elements():
    """Test getting unique elements."""
    a = Atoms('Fe2O3COH')
    # The elements need to be in alphabetical order.
    assert adapters.get_unique_elements(a) == ['C', 'Fe', 'H', 'O']


def test_get_element_ratios():
    """Test getting the element ratios."""
    a = Atoms('CH4')
    # The ratios should be sorted in the alphabetical order of the
    # elements, i.e. 0.2 for C should come first followed by 0.8 for H.
    assert adapters.get_element_ratios(a) == [0.2, 0.8]

    a = Atoms('H4C')
    assert adapters.get_element_ratios(a) == [0.2, 0.8]
