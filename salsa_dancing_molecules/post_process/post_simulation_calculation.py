"""Module for calling calculations of the post simulation values."""

from ase.io.trajectory import Trajectory
from ..equilibrium import get_equilibrium
from ..average import average
from ..mean_square_displacement import calculate_msd
from ..self_diffusion_coefficient import calculate_self_diffusion_coefficient
from ..capacity_NVE import calculate_NVE_heat_capacity
from ..capacity_NVT import calculate_NVT_heat_capacity
from ..debye_temperature import calculate_debye
from ..cohesive_energy import calculate_cohesive_energy

import csv
import numpy as np


def get_column_from_csv(csv_path, col_name):
    """Extract column from csv file.

    Args:
        csv_path: string - path to csv file to be read.
        col_name: string - name of column to be extracted.

    return:
        return_list: list - list of values in specified columns
    """
    f = open(csv_path, "r")
    file_data = csv.DictReader(f)
    return_list = []
    for row in file_data:
        return_list.append(row[col_name])
    f.close()
    return return_list


def post_simulation_calculation(sim_info):
    """Perform post simulation calculations for specific simulation.

    Args:
        sim_info: dict - Dictionary with info on simulation.

    return:
        result_dict                 - dictionary containing:
            MSD_avr                     - list
            self_diffusion_coefficient  - float
            heat_capacity               - float
            debye_temperature           - float
            cohesive_energy             - float

    To get the average mean square displacement from equilibrium-time to the
    last time-step take the last element of MSD_avr.
    """
    traj_path = sim_info["traj_output_path"]
    csv_path = sim_info["csv_output_path"]
    temperature = get_column_from_csv(csv_path, "Temperature (K)")
    temperature = [float(x) for x in temperature]
    ensemble = sim_info["ensemble"]
    ensemble = ensemble.upper()
    # Read the Trajectory file
    configs = Trajectory(traj_path)

    # Calculate the equilibrium time of the system
    t0, equilibrium_warning = get_equilibrium(configs, ensemble)

    if equilibrium_warning:
        equilibrium_warning = ("Warning: Equilibrium detected close to the "
                               "end of the simulation (last 10%). True "
                               "equilibrium might not have been reached.")
    else:
        equilibrium_warning = ""

    # Calculate the temperature average of the system
    temperature = np.array(temperature)
    temperature_avr = average(t0, temperature)[-1]

    # Calculate values
    MSD, MSD_avr = calculate_msd(configs, t0)
    self_diffusion_coefficient = calculate_self_diffusion_coefficient(MSD, t0)

    if ensemble == 'NVE':
        heat_capacity = calculate_NVE_heat_capacity(configs, t0)
    elif ensemble == 'NVT':
        heat_capacity = calculate_NVT_heat_capacity(configs, t0)

    debye_temperature, debye_warning = calculate_debye(configs,
                                                       temperature_avr,
                                                       heat_capacity)

    if debye_warning:
        debye_warning = ("Warning: Debye temperature is low compared to the "
                         "temperature. The calculated value for debye "
                         "temperature might not be accurate.")
    else:
        debye_warning = ""

    cohesive_energy = calculate_cohesive_energy(configs, t0)

    result_dict = {}
    result_dict["MSD_avr"] = MSD_avr
    result_dict["self_diffusion_coefficient"] = self_diffusion_coefficient
    result_dict["heat_capacity"] = heat_capacity
    result_dict["debye_temperature"] = debye_temperature
    result_dict["cohesive_energy"] = cohesive_energy
    result_dict["equilibrium_warning"] = equilibrium_warning
    result_dict["debye_warning"] = debye_warning

    return result_dict
