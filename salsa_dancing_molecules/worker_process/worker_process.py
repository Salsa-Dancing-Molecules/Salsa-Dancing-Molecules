"""Program for managing simulations.

This program takes in a list of jobs, picks one, then moves the file and
runs the simulation according to the data.
"""
import os
import csv
import json
from datetime import datetime
from .infiles_handler import handle_files
from .simulation_starter import start_simulation
from ..post_process.post_simulation_calculation import (
                                                post_simulation_calculation)


def start(path):
    """
    Take a catalog containing files and folders to work on.

    Args:
        path: The path to the working directory.
    """
    path = path.rstrip("/")
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    sim_calc_list = []
    while len(os.listdir(path+"/unbegun_simulations")) != 0:
        list_of_files = os.listdir(path+"/unbegun_simulations")
        current_file = list_of_files[0]
        try:
            os.rename(path+"/unbegun_simulations/"+current_file,
                      path+"/started_simulations/"+current_file)
        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)
        else:
            try:
                sim_info, atoms_obj = handle_files(path +
                                                   "/started_simulations/" +
                                                   current_file)
                start_simulation(sim_info, atoms_obj)
            except Exception as e:
                print(e)
                filename = os.path.splitext(path+"/started_simulations/" +
                                            current_file)[0]+"_error.txt"
                f = open(filename, 'w')
                f.write(str(e))
                f.close()
            else:
                os.rename(path+"/started_simulations/"+current_file,
                          path+"/done_simulations/"+current_file)
                f = open(path+"/done_simulations/"+current_file)
                sim_info = json.load(f)
                f.close()
                sim_calc_list.append(post_simulation_calculation(sim_info))
    if not os.path.exists(path+"/post_process_output"):
        os.mkdir(path+"/post_process_output")
    results_file_name = "temp_"+str(rank)+".csv"
    results_file_name = (path.rstrip('/') + "/post_process_output/" +
                         results_file_name)
    f = open(results_file_name, "w+")
    fieldnames = sim_calc_list[0].keys()
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    for result_dict in sim_calc_list:
        writer.writerow(result_dict)
    f.close()
    all_post_calc_info = []
    if rank == 0:
        for file in os.listdir(path+"/post_process_output"):
            if file.startswith("temp_"):
                f = open(path+"/post_process_output/"+file)
                reader = csv.DictReader(f)
                for row in reader:
                    all_post_calc_info.append(row)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%y_%H_%M_%S")
        results_file_name = "post_process_"+dt_string+".csv"
        results_file_name = (path + "/post_process_output/" +
                             results_file_name)
        f = open(results_file_name, "w+")
        fieldnames = all_post_calc_info[0].keys()
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for result_dict in all_post_calc_info:
            writer.writerow(result_dict)
        f.close()
        for file in os.listdir(path+"/post_process_output"):
            if file.startswith("temp_"):
                os.remove(path+"/post_process_output/"+file)
