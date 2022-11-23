"""Function that decides to plot single-plot or four-plots."""
from .variables import Variables
from .scatter_plot import (draw_scatter_plot,
                           draw_four_scatter_plots)
import csv
import numpy as np
import matplotlib.pyplot as plt


def data_plot(Q='-', filename='simulation_data.csv',
              newfile='fourplots.png', show=False):
    """
    Generate one or four plots depeding on inarguments.

    Q : Quanitity, like {Ekin, Epot, cnve, Pres, Temp}

    Filename: The filename containg the data

    Newfile: The name of the file the image will be saved to
    """
    time_step = []
    kinetic = []
    potential = []
    pressure = []
    temperature = []
    heat_capacity = []

    with open(filename, 'r') as csv_file:
        data = csv.DictReader(csv_file)
        next(data)
        for row in data:
            potential.append(float(row['Potential Energy (eV)']))
            kinetic.append(float(row['Kinetic Energy (eV)']))
            pressure.append(float(row['Pressure (Pa)']))
            temperature.append(float(row['Temperature (K)']))
            heat_capacity.append(float(
                row['Specific Heat Capacity NVE (J/[K kg])']))
            time_step.append(float(row['Time (fs)']))

    if Q != '-':
        if Q == 'Ekin':
            draw_scatter_plot(time_step, kinetic,
                              '(fs)', '(eV)', newfile, show)
        elif Q == 'Epot':
            draw_scatter_plot(time_step, potential,
                              '(fs))', '(eV)', newfile, show)
        elif Q == 'Pres':
            draw_scatter_plot(time_step, pressure,
                              '(fs)', '(Pa)', newfile, show)
        elif Q == 'Temp':
            draw_scatter_plot(time_step, temperature,
                              '(fs)', '(K)', newfile, show)
        elif Q == 'cnve':
            draw_scatter_plot(time_step, heat_capacity,
                              '(fs)', '( J/[K kg] )', newfile, show)
        else:
            print('Unknown command, try agian. For help use -h or --help ')
    else:
        # converting column data to list
        draw_four_scatter_plots(time_step, [
            potential,
            kinetic,
            pressure,
            temperature,
            heat_capacity,
        ], newfile, show)
