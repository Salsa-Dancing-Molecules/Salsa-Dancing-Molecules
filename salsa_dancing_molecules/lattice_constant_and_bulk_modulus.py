"""
Function for calculating lattice constant and bulk modulus.

Takes a trajectory file and outputs lattice constant (in Angstrom)
and bulk modulus (in GPa) as float values.
"""

from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState
import math

traj_file = 'Ag.traj@0:5'


def get_lattice_constant_and_bulk_modulus(traj_file):
    """
    Read traj file, place atoms objects in list and call calculation function.

    Takes a filepath to traj file as a string and returns lattice constant and
    bulk modulus.
    """
    configs = read(traj_file)
    return calculate_lattice_constant_and_bulk_modulus(configs)


def calculate_lattice_constant_and_bulk_modulus(configs):
    """
    Calculate lattice constant as done in ASE documentation.

    Takes a list of atoms objects at different time steps and returns
    a - lattice constant, and B - bulk modulus.
    """
    # This code assumes crystal structure does not
    # change from first time step.
    cell = configs[0].get_cell()
    lattice = cell.get_bravais_lattice()
    volumes = [atom.get_volume() for atom in configs]
    energies = [atom.get_potential_energy() for atom in configs]
    eos = EquationOfState(volumes, energies)
    v0, e0, B0 = eos.fit()
    B = B0 / kJ * 1.0e24

    if 'FCC' in str(lattice):
        a = (4 * v0) ** (1/3)

    elif 'BCC' in str(lattice):
        a = (2 * v0) ** (1/3)

    elif 'SC' in str(lattice):
        a = v0 ** (1/3)

    # Add more crystal lattices in if statements here?

    return a, B


print(get_lattice_constant_and_bulk_modulus(traj_file))

# Call of function should look like this:
# get_lattice_constant_and_bulk_modulus(traj_file="Ag.traj@0:5"))
# where the 0:5 means that the read function reads the first 5 atoms objects
# in the traj file
