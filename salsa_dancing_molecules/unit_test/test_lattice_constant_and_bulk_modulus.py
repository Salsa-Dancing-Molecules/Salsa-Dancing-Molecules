"""
Unit test for lattice_constant.py.

Expected result values were calculated manually using the EquationOfState
function imported from ase.eos.
"""

import pytest
from ..lattice_constant_and_bulk_modulus import (
        calculate_lattice_constant_and_bulk_modulus
)
from unittest.mock import Mock

"""
Make the mock objects, the function calculate_lattice_constant_and_bulk_modulus
takes a list of five elements (this could be subject to change)
"""
atoms = Mock()
atoms.__len__ = Mock(return_value=1)
configs = [atoms, atoms, atoms, atoms, atoms]


# We don't care about numerical stability in our test.
@pytest.mark.filterwarnings("ignore: Polyfit may be poorly conditioned")
def test_lattice_constant_and_bulk_modulus():
    """Function for testing latt. const. and bulk mod. calculation."""
    cell = Mock()
    cell.get_bravais_lattice.return_value = 'FCC'
    configs[0].get_cell.return_value = cell

    atoms.get_volume.side_effect = [3, 2, 1, 2, 3]
    atoms.get_potential_energy.side_effect = [3, 2, 1, 2, 3]

    """Runs a test with set values for the atoms objects."""
    result = calculate_lattice_constant_and_bulk_modulus(configs)
    test_success = (1.5662216452033666, 893.9303749757568)
    assert result == pytest.approx(test_success, 0.0001)
