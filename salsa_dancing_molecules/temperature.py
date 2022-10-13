"""
Function for calculating temperature of atoms object.
The function takes in an atoms object and returns the temperature.
"""
from ase import units

def get_temperature(atoms):
    return atoms.get_kinetic_energy()/(1.5*units.kB)

if __name__ == "__main__":
    get_temperature(atoms)	
