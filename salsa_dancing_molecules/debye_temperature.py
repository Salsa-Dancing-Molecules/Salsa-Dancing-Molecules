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
    debye_temperature = (calculate_debye(configs, temperature,
                         specific_heat_capacity))

    return debye_temperature


def calculate_debye(configs, temperature, specific_heat_capacity):
    """
    Calculate the debye temperature.

    arguments:
        configs: ase.io.trajectory.Trajectory - traj file containg atom-obj.
        temperature:float             - Temperature average of the system
        specific_heat_capacity:float  - specifict heat capacity of the system

    return:
        debye_temperature - float
        warning: bool     - False if under the low-temperature limit.

    This function assumes that the temperature is low. If temperature is high
    the results might not be accurate.
    """
    a = configs[0]
    N = len(a)  # Number of atoms
    mass = sum(a.get_masses())*units._amu  # change mass from u to kg
    heat_capacity = specific_heat_capacity*mass
    debye_temperature = (temperature*((12*units.pi**4*N*units._k)/(5 *
                         heat_capacity))**(1/3))
    warning = 0.3 < temperature/debye_temperature

    return debye_temperature, warning
