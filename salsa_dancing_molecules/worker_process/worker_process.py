"""Program for managing simulations.

This program takes in a list of jobs, picks one, then moves the file and
runs the simulation according to the data.
"""
import os
import csv
import json
import uuid
from datetime import datetime
from .infiles_handler import handle_files
from .simulation_starter import start_simulation
from ..post_process.post_simulation_calculation import (
                                                post_simulation_calculation)


def log_simulation_exception(started_path, exception):
    """Log an exception for a simulation.

    Log an exception for a simulation to standard output as well as to a file
    where the file extension of started_path has been replaced with
    "_error.txt".

    arguments:
        started_path: str    - path to simulation configuration
        excetpion: Exception - exception to log
    """
    print(exception)
    filename = os.path.splitext(started_path)[0]+"_error.txt"
    with open(filename, 'w') as f:
        f.write(str(exception))


def run_simulation_job(started_path, done_path):
    """Run a single simulation job.

    Run a single simulation job described by the configuration pointed to by
    started_path. The simulation configuration is moved to done_path on
    successful completion.

    arguments:
        started_path: str - path to simulation job configuration
        done_path: str    - path to store the job configuration when simulation
                            has successfully completed

    returns:
        simulation_result: list(dict()) | None - list of simulation results or
                                                 None on error
    """
    try:
        sim_info, atoms_obj = handle_files(started_path)
        start_simulation(sim_info, atoms_obj)

        # Mark the simulation as completed by moving the simulation job
        # description to the done directory.
        os.rename(started_path, done_path)

        with open(done_path) as f:
            sim_info = json.load(f)

        sim_results = post_simulation_calculation(sim_info)

        # Add the name of the simulation configuration to the simulation
        # result.
        sim_file_name = os.path.splitext(os.path.basename(started_path))[0]
        sim_results["file_name"] = sim_file_name

        return sim_results
    except Exception as e:
        log_simulation_exception(started_path, e)
        return None


def post_process_write_temporary(work_dir, rank, sim_calc_list):
    """Write a temporary post process data file.

    Write a temporary post process output file. These files will be combined to
    a single result file by the worker with rank 0.

    arguments:
        work_dir: str               - path to simulation workspace
        rank: int                   - MPI process rank used for file naming
        sim_calc_list: list(dict()) - list with simulation results for
                                      simulations run by this worker
    """
    post_process_dir = f'{work_dir}/post_process_output'
    results_file_name = f'{post_process_dir}/temp_{str(rank)}.csv'

    with open(results_file_name, "w+") as f:
        fieldnames = sim_calc_list[0].keys()
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for result_dict in sim_calc_list:
            writer.writerow(result_dict)


def post_process_all_files(work_dir):
    """Post process all temporary files in work_dir/post_process_output.

    Goes through all temporary post processing results and combines them to a
    single output file containing all data.

    arguments:
        work_dir: str - path to simulation workspace
    """
    all_post_calc_info = []
    post_process_dir = f'{work_dir}/post_process_output'

    # Iterate over all result files in the post process directory and read them
    # into memory.
    for file in os.listdir(post_process_dir):
        if file.startswith("temp_"):
            with open(f'{post_process_dir}/{file}') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_post_calc_info.append(row)

    # If we find no files to process, we're done.
    if len(all_post_calc_info) == 0:
        return

    # Create the name of the final results file.
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%y_%H_%M_%S")
    results_file_name = f'{post_process_dir}/post_process_{dt_string}.csv'

    # Write all results to the final results file.
    with open(results_file_name, "w+") as f:
        fieldnames = all_post_calc_info[0].keys()
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for result_dict in all_post_calc_info:
            writer.writerow(result_dict)

    # Clean all temporary files.
    for file in os.listdir(post_process_dir):
        if file.startswith("temp_"):
            os.remove(f'{post_process_dir}/{file}')


def start(path):
    """
    Take a catalog containing files and folders to work on.

    Args:
        path: The path to the working directory.
    """
    path = path.rstrip("/")
    rank = str(uuid.uuid1())

    # List for storing post simulation calculation results.
    sim_calc_list = []

    while len(os.listdir(path+"/unbegun_simulations")) != 0:
        list_of_files = os.listdir(path+"/unbegun_simulations")
        current_file = list_of_files[0]

        unbegun_path = f'{path}/unbegun_simulations/{current_file}'
        started_path = f'{path}/started_simulations/{current_file}'
        done_path = f'{path}/done_simulations/{current_file}'

        try:
            # Reserve a simulation job by moving the simulation specification
            # from unbegun_simulations to started_simulations. This is repeated
            # until the simulation directory is empty.
            #
            # If another competing worker process steals the file, an exception
            # will be raised and we try again with another file.
            os.rename(unbegun_path, started_path)
        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)
        else:
            # If we managed to reserve a file, we run the simulation.
            if res := run_simulation_job(started_path, done_path):
                sim_calc_list.append(res)

    if len(sim_calc_list) > 0:
        post_process_write_temporary(path, rank, sim_calc_list)
