"""Module for finding the "steady state" of a system"""

from pymbar.timeseries import detect_equilibration
import numpy as np



def get_eqiulibrium(temperatures):
    """
    Function for finding the eqiulibrium of a NVE-system.

    arguments:
        temperatures - array, containing temperatures for each timestep 

    returns:
        eqiulibrium - integer
    """
    [eqiulibrium, g, Neff_max] = detect_equilibration(temperatures)
    
    return eqiulibrium

if __name__ == "__main__":
    temperatures=np.array([])
    print(get_eqiulibrium(temperatures))
