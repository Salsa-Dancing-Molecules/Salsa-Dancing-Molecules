"""
Unit test for lattice_constant.py.

Expected result values were calculated manually using the EquationOfState
function imported from ase.eos.
"""

import sys
import unittest
from lattice_constant import calculate_lattice_constant_and_bulk_modulus
from unittest.mock import Mock
"""
Make the mock objects, the function calculate_lattice_constant_and_bulk_modulus
takes a list of five elements (this could be subject to change)
"""
atoms = Mock()
atoms.__len__ = Mock(return_value=1)
configs = [atoms, atoms, atoms, atoms, atoms]


class LatticeTests(unittest.TestCase):
    """Class for testing latt. const. and bulk mod. calculation."""

    atoms.get_volume.side_effect = [3, 2, 1, 2, 3]
    atoms.get_potential_energy.side_effect = [3, 2, 1, 2, 3]

    def test_lattice_constant_and_bulk_modulus(self):
        """Runs a test with set values for the atoms objects."""
        result = calculate_lattice_constant_and_bulk_modulus(configs)
        test_success = (1.5662216452033666, 893.9303749757568)
        self.assertTrue(result == test_success)


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(LatticeTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
