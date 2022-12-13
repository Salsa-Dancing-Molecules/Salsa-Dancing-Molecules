"""
Program to manage volume processing for calculation of bulk properties.

A number of simulations with different volumes are neede for
calculation of lattice constant and bulk modulus.

"""

import json
import os
import csv
from ..bulk_properties import get_bulk_properties
from datetime import datetime


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
    done_path = path.rstrip("/")+"/done_simulations"
    sim_info_list = []
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

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
        results_list.append(get_bulk_properties(group, ensembles[0]))

    if not os.path.exists(path.rstrip("/")+"/volume_process_output"):
        os.mkdir(path.rstrip("/")+"/volume_process_output")

    # Write to csv-file
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%y_%H_%M_%S")
    results_file_name = "volume_process_"+dt_string+".csv"
    results_file_name = (path.rstrip('/') + "/volume_process_output/" +
                         results_file_name)
    f = open(results_file_name, "w+")
    fieldnames = results_list[0].keys()
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    for result_dict in results_list:
        writer.writerow(result_dict)
        traj_list.append(result_dict['Trajectory file'])
        csv_file = result_dict['Trajectory file'].rstrip('.traj') + '.csv'
        csv_list.append(csv_file)
    f.close()

    # One processor core deletes all files except those corresponding
    # to the optimal volume.
    if rank == 0:
        for file in os.listdir(path+"output/traj/"):
            remove_file = True
            for file_name in traj_list:
                if str(file) in file_name:
                    remove_file = False
                    break
            if remove_file:
                os.remove(path+"output/traj/"+file)
                os.remove(path+"output/csv/"+file.rstrip('.traj') + '.csv')
                os.remove(path+"done_simulations/"+file.rstrip('.traj') +
                          '.json')
