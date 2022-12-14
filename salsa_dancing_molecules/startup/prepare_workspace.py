"""This module creates the necessary folders in the workspace."""
import os


def do_preparations(work_path):
    """Check if folders exists, create if not found.

    Args:
        work_path - string with path to workplace directory.
    """
    if not os.path.exists(work_path):
        os.mkdir(work_path)
    list_of_folders = ["/unbegun_simulations",
                       "/started_simulations",
                       "/done_simulations",
                       "/post_process_output",
                       "/output/traj",
                       "/output/csv",
                       "/materials"]
    for folder in list_of_folders:
        if not os.path.exists(work_path+folder):
            os.makedirs(work_path+folder)
