"""Module for calculating the Debye temperature time average."""
from ase import units


def get_debye_temperature(traj_file, temperature, specific_heat_capacity)
    """
    Calculate the debye temperature.

    arguments:
        traj_file               - trajectory file
        temperature             - float
        specific_heat_capacity  - float

    return:
        debye_temperature - float

    This function assumes that the temperature is low. If temperature is high
    the results might not be accurate.
    """
    configs = read(traj_file + "@0")
    N = len(configs[0])  # Number of atoms

    #This is the simple function (maybe change this later)
    debye_temperature = (temperature*((12*pi**4*N*units.kb)/(5*
                        specific_heat_capacity))**(1/3))

    return debye_temperature
