"""Module for calculating the Debye temperature time average."""
from ase import units
from ase.io import read


def get_debye_temperature(traj_file, temperature, specific_heat_capacity):
    """
    Read trajectory file and call calculation function.

    arguments:
        traj_file:str                 - trajectory file
        temperature:float             - Temperature average of the system
        specific_heat_capacity:float  - specifict heat capacity of the system

    return:
        debye_temperature - float
    """
    configs = read(traj_file + "@0:1")  # Only one timestep is needed
    debye_temperature = (calculate_debye_temperature(configs, temperature,
                         specific_heat_capacity))

    return debye_temperature


def calculate_debye_temperature(configs, temperature, specific_heat_capacity):
    """
    Calculate the debye temperature.

    arguments:
        configs: ase.io.trajectory.Trajectory - traj file containg atom-obj.
        temperature:float             - Temperature average of the system
        specific_heat_capacity:float  - specifict heat capacity of the system

    return:
        debye_temperature - float

    This function assumes that the temperature is low. If temperature is high
    the results might not be accurate.
    """
    N = len(configs[0])  # Number of atoms
    debye_temperature = (temperature*((12*units.pi**4*N*units.kB)/(5 *
                         specific_heat_capacity))**(1/3))

    return debye_temperature
