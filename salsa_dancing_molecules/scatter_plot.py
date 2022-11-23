"""File to create scatter plots from two vectors."""
import matplotlib
import matplotlib.pyplot as plt


def draw_scatter_plot(x_axis, y_axis, xlabel, ylabel, filename, show):
    """
    Draw a scatter plot from two given vectors.

    Arguments in are: x-axis, y-axis, x-label, y-label, file name.

    File is saved as filename (which should include .png).
    """
    # Agg -> use non-interactive backend to save plot to file
    if not show:
        matplotlib.use('Agg')
    plt.scatter(x_axis, y_axis, s=1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    if show:
        plt.show()


def draw_four_scatter_plots(time_step, y_list, filename, show):
    """
    Draw a scatter plot from a list of variables.

    Arguments in are: time-steps, y-list,file name.

    File is saved as filename (which should include .png).
    """
    if not show:
        matplotlib.use('Agg')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 10))
    fig.suptitle('Simulation of molecular dynamics')
    ax1.scatter(time_step, y_list[0],
                s=1, label='Ep', c='orange')
    ax1.scatter(time_step, y_list[1],
                s=1, label='Ek', c='black')
    ax1.set_title('Potential Energy and Kinetic Energy')
    ax1.set_xlabel('Timestep N (fs)')
    ax1.set_ylabel('(eV)')
    ax1.legend()

    ax2.scatter(time_step, y_list[4], s=1)
    ax2.set_title('Specific Heat Capacity NVE')
    ax2.set_xlabel('Timestep N (fs)')
    ax2.set_ylabel('( J/[K kg] )')

    ax3.scatter(time_step, y_list[2], s=1)
    ax3.set_title('Pressure')
    ax3.set_xlabel('Timestep N (fs)')
    ax3.set_ylabel('(Pa)')

    ax4.scatter(time_step, y_list[3], s=1)
    ax4.set_title('Temperature')
    ax4.set_xlabel('Timestep N (fs)')
    ax4.set_ylabel('(K)')

    plt.savefig(filename)

    if show:
        plt.show()
