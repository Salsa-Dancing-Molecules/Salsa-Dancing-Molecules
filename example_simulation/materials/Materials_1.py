"""Materials used in simulation."""
from ase import Atoms


a = 4.05  # Gold lattice constant
b = a / 2
gold_fcc = Atoms('Au',
                 cell=[(0, b, b), (b, 0, b), (b, b, 0)],
                 pbc=True)
