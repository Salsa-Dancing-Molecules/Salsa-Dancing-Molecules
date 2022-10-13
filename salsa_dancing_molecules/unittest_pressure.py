"""Unittest for pressure.py."""

import sys
import unittest
from pressure import get_pressure
from mock_atoms import atoms


class PressureTest(unittest.TestCase):
    """Class for unittesting pressure.py."""

    def test_pressure(self):
        """Function for testing pressure.py."""
        # set up a mock atoms-object
        a = atoms()

        X = get_pressure(a)
        Y = 9.50705759354618  # This is the value the calculation should give
        self.assertTrue(X == Y)


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(PressureTest)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
