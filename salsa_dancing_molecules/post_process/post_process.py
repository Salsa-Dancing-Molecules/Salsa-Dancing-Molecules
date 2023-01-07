"""Module for managing post process calculations of multiple simulations."""
import os
import csv
from .post_simulation_calculation import post_simulation_calculation
from datetime import datetime
import json


def run_post_calculations(work_path):
    """Run post processing.

    Go through folder of configs from finished simulations and perform
    post simulation calculations.

    Args:
        work_path: string - path to working directory.
    """
    done_path = work_path.rstrip("/")+"/done_simulations"
    done_list = os.listdir(done_path)
    simulation_results = []
    if not os.path.exists(work_path.rstrip("/")+"/post_process_output"):
        os.mkdir(work_path.rstrip("/")+"/post_process_output")
    for done_sim in done_list:
        f = open(os.path.join(done_path, done_sim))
        sim_info = json.load(f)
        f.close()
        sim_results = post_simulation_calculation(sim_info)
        sim_file_name = os.path.splitext(done_sim)[0]
        sim_results["file_name"] = sim_file_name
        simulation_results.append(sim_results)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%y_%H_%M_%S")
    results_file_name = "post_process_"+dt_string+".csv"
    results_file_name = (work_path.rstrip('/') + "/post_process_output/" +
                         results_file_name)
    f = open(results_file_name, "w+")
    fieldnames = simulation_results[0].keys()
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    for result_dict in simulation_results:
        writer.writerow(result_dict)
    f.close()
