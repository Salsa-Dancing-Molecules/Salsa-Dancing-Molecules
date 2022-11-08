"""File to create scatter plots from two vectors."""
import matplotlib.pyplot as plt


def draw_scatter_plot(x_axis, y_axis, filename):
    """
    Draw a scatter plot from two given vectors.

    File is saved as filename (which should include .png).
    """
    plt.scatter(x_axis, y_axis)
    plt.savefig(filename)