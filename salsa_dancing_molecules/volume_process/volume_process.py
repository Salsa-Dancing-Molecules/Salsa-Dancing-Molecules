"""
Program to manage volume processing for calculation of bulk properties.

A number of simulations with different volumes are neede for
calculation of lattice constant and bulk modulus.

"""

import json
import os
import csv
import numpy as np
from ..bulk_properties import get_bulk_properties
from ..lindemann import get_lindemann_parameter
from ..equilibrium import get_equilibrium
from datetime import datetime
from asap3 import Trajectory


def group_by_volume(sim_info_list):
    """Group volume-simulations.

    Input:
        sim_info_list: list  -list containing simulation information from all
                              json-files

    Output:
        sim_info_group_list: list  -list containg lists. All simulations
                                    from the same volume-simulation will be
                                    grouped together in one sub-list.
        csv_list: list             -list containging csv-file names from
                                    simulations that have not been simulated
                                    for varying volume.
        traj_list: list            -list containing traj-file names of
                                    files that have not been simulated for
                                    varying volume.

    """
    sim_info_groups_list = []
    traj_list = []
    csv_list = []
    for sim_info in sim_info_list:
        if 'volume-scale' in sim_info:
            if len(sim_info_groups_list) == 0:
                sim_info_groups_list.append([sim_info])
            else:
                found_no_match = True
                for group_list in sim_info_groups_list:
                    found_group_match = True
                    for old_sim_info in group_list:
                        for key in old_sim_info.keys():
                            if key not in ["volume-scale",
                                           "traj_output_path",
                                           "csv_output_path"]:
                                if old_sim_info[key] != sim_info[key]:
                                    found_group_match = False
                                    break
                    if found_group_match:
                        group_list.append(sim_info)
                        found_no_match = False
                if found_no_match:
                    sim_info_groups_list.append([sim_info])
        else:
            traj_list.append(sim_info['traj_output_path'])
            csv_list.append(sim_info['csv_output_path'])
    return sim_info_groups_list, traj_list, csv_list


def start(path):
    """
    Take a catalog containing files and folders to work on.

    Args:
        path: The path to the working directory.

    """
    path = path.rstrip("/")
    done_path = path+"/done_simulations"
    sim_info_list = []

    for file in os.listdir(done_path):
        f = open(os.path.join(done_path, file))
        sim_info = json.load(f)
        f.close()
        sim_info_list.append(sim_info)

    sim_info_groups_list, traj_list, csv_list = group_by_volume(sim_info_list)

    results_list = []
    for group_list in sim_info_groups_list:
        group = [sim_info['traj_output_path'] for sim_info in group_list]
        ensembles = [sim_info['ensemble'] for sim_info in group_list]
        result_dict = get_bulk_properties(group, ensembles[0])
        if not result_dict['Lattice constant'] is None or float('NaN'):
            configs = Trajectory(result_dict['Trajectory file'])
            # Calculate the equilibrium time of the system
            t0, equilibrium_warning = get_equilibrium(configs, ensembles[0])
            if type(result_dict['Lattice constant']) == np.ndarray:
                a = result_dict['Lattice constant'][0]  # shortest vector
            else:
                a = result_dict['Lattice constant']
            parameter_list, criterion = get_lindemann_parameter(
                                            result_dict['Trajectory file'],
                                            a,
                                            t0)
        else:
            parameter_list = None
            criterion = None
        result_dict['Lindeman parameter over time'] = parameter_list
        result_dict['Lindeman criterion'] = criterion
        results_list.append(result_dict)

    post_process_dir = f'{path}/post_process_output'

    # Iterate over all result files in the post process directory and read them
    # into memory.
    post_calc_info = []
    for file in os.listdir(post_process_dir):
        if file.startswith("temp_"):
            with open(f'{post_process_dir}/{file}') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    post_calc_info.append(row)

    # Write to csv-file
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%y_%H_%M_%S")
    results_file_name = "post_process_"+dt_string+".csv"
    results_file_name = (path + "/post_process_output/" +
                         results_file_name)
    f = open(results_file_name, "w+")
    fieldnames = list(results_list[0].keys())+list(post_calc_info[0].keys())
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    for post_calc_dict in post_calc_info:
        writer.writerow(post_calc_dict)
    for result_dict in results_list:
        writer.writerow(result_dict)
    f.close()

    # Clean all temporary files.
    for file in os.listdir(post_process_dir):
        if file.startswith("temp_"):
            os.remove(f'{post_process_dir}/{file}')
