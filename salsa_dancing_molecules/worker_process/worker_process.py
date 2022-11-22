import os
from infiles_handler import handle_files
from simulation_starter import start_simulation

def start(path):
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
                simulation_info, atoms_object = handle_files(path+"/started_simulations/"+current_file)
                start_simulation(simulation_info, atoms_object)
            except Exception as e:
                filename = os.path.splitext(path+"/started_simulations/"+current_file)[0]+"_error.txt"
                f = open(filename, 'w')
                f.write(e)
                f.close()
            else:
                os.rename(path+"/started_simulations/"+current_file,
                          path+"/done_simulations/"+current_file)