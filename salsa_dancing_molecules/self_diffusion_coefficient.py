"""Module for calculating the self diffusion coefficient."""

from .mean_square_displacement import get_msd
from .mean_square_displacement import calculate_msd


def get_self_diffusion_coefficient(traj_file):
    """
    Take a trajectory file and returns the self diffusion coefficient.

    arguments:
        traj_file - trajectory file

    returns:
        self_diffusion_coefficient - float
    """
    MSD = get_msd(traj_file, reference="initial")
    self_diffusion_coefficient = calculate_self_diffusion_coefficient(MSD)

    return self_diffusion_coefficient


def calculate_self_diffusion_coefficient(MSD):
    """
    Take a list of mean square displacement for each timestep.

    arguments:
        MSD - list

    returns:
        self_diffusion_coefficient - float
    """
    t = len(MSD)
    self_diffusion_coefficient = MSD[-1]/(6*t)

    return self_diffusion_coefficient
