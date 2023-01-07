"""Helpers to run an example simulation on Argon."""

from ase.calculators.emt import EMT
from ase import Atoms
from .nve import run as nve_run


def run(steps, cell_size=5, output_path='ar.traj'):
    """Run an MD simulation for argon in a FCC configuration.

    Arguments:
        steps - the number of steps in the simulation, one step is
                equal to 1 fs.
        cell_size - the number of repetitions in all dimensions of the
                    minimal unit cell. Default is a 5*5*5 repetition.
        output_path - path to which to save the generated trajectory
                      data. Default is to save to "ar.traj".
    """
    # Set up an example Argon crystal
    a = 5.0  # approximate lattice constant
    b = a / 2
    atoms = Atoms('Ar',
                  cell=[(0, b, b), (b, 0, b), (b, b, 0)],
                  pbc=1,
                  calculator=EMT())  # use EMT potential
    atoms = atoms * (cell_size, cell_size, cell_size)
    nve_run(atoms, steps, output_path)
