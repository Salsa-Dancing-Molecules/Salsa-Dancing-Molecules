"""Program for managing simulations.

This program takes in a list of jobs, picks one, then moves the file and
runs the simulation according to the data.
"""

import os
from .infiles_handler import handle_files
from .simulation_starter import start_simulation


def start(path):
    """
    Take a catalog containing files and folders to work on.

    Args:
        path: The path to the working directory.
    """
    path = path.rstrip("/")
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
