"""Unit test for scatter_plot.py."""
from ..scatter_plot import draw_scatter_plot
import pathlib as pl


def test_scatter_plot():
    """Creates simple scatter plot and checks if it is saved in a file."""
    x_axis = [1, 2, 3, 4]
    y_axis = [1, 4, 9, 16]
    filename = 'test_plot.png'

    draw_scatter_plot(x_axis, y_axis, filename)
    path = pl.Path(filename)
    assert path.is_file()
