"""Function that decides to plot single-plot or four-plots."""
from .variables import Variables
from .scatter_plot import (draw_scatter_plot,
                           draw_four_scatter_plots)
import numpy as np
import matplotlib.pyplot as plt
from pandas import *


def data_plot(Q='-', filename='simulation_data.csv',
              newfile='fourplots.png', show=False):
    """
    Generate one or four plots depeding on inarguments.

    Q : Quanitity, like {Ekin, Epot, cnve, Pres, Temp}

    Filename: The filename containg the data

    Newfile: The name of the file the image will be saved to
    """
    data = read_csv(filename)
    time_step = data['Time (fs)']

    if Q != '-':
        if Q == 'Ekin':
            draw_scatter_plot(time_step, data['Kinetic Energy (eV)'].tolist(),
                              '(fs)', '(eV)', newfile, show)
        elif Q == 'Epot':
            draw_scatter_plot(time_step,
                              data['Potential Energy (eV)'].tolist(),
                              '(fs))', '(eV)', newfile, show)
        elif Q == 'Pres':
            draw_scatter_plot(time_step, data['Pressure (Pa)'].tolist(),
                              '(fs)', '(Pa)', newfile, show)
        elif Q == 'Temp':
            draw_scatter_plot(time_step, data['Temperature (K)'].tolist(),
                              '(fs)', '(K)', newfile, show)
        elif Q == 'cnve':
            draw_scatter_plot(time_step, data[
                'Specific Heat Capacity NVE (J/[K kg])'].tolist(),
                '(fs)', '( J/[K kg] )', newfile, show)
        else:
            print('Unknown command, try agian. For help use -h or --help ')
    else:
        # converting column data to list
        draw_four_scatter_plots(time_step, [
            data['Potential Energy (eV)'].tolist(),
            data['Kinetic Energy (eV)'].tolist(),
            data['Pressure (Pa)'].tolist(),
            data['Temperature (K)'].tolist(),
            data['Specific Heat Capacity NVE (J/[K kg])'].tolist()
        ], newfile, show)
