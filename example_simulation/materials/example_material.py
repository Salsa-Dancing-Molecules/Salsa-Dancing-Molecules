"""Materials used in simulation.

Create ASE Atoms objects to use in simulations.
Then, specify the objects/materials to be used in the simulation config.
Use the same name in the config file as the name of the variable in this file.
"""
from ase import Atoms


a = 4.05  # Gold lattice constant
b = a / 2
gold_fcc = Atoms('Au',
                 cell=[(0, b, b), (b, 0, b), (b, b, 0)],
                 pbc=True)
