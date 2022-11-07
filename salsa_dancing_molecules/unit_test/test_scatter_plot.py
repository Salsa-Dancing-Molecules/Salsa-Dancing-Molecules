"""Unit test for scatter_plot.py."""
from ..scatter_plot import draw_scatter_plot
import unittest
import pathlib as pl


class PlotTests(unittest.TestCase):
    """Class for testing creation of scatter plot file."""

    def test_scatter_plot(self):
        """Creates simple scatter plot and checks if it is saved in a file."""
        x_axis = [1, 2, 3, 4]
        y_axis = [1, 4, 9, 16]
        filename = 'test_plot.png'

        draw_scatter_plot(x_axis, y_axis, filename)
        path = pl.Path(filename)
        self.assertTrue(path.is_file())


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(PlotTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
