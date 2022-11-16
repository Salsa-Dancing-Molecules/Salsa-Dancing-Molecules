"""Helpers to run an example simulation on Argon."""

from ase.lattice.cubic import FaceCenteredCubic
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
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              symbol="Ar",
                              size=(cell_size, cell_size, cell_size),
                              latticeconstant=5.256,
                              pbc=True)
    nve_run(atoms, steps, output_path)
