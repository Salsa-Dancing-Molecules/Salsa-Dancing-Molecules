"""Module for calculating the self diffusion coefficient."""

from .mean_square_displacement import get_msd


def get_self_diffusion_coefficient(traj_file, t0):
    """
    Take a trajectory file and returns the self diffusion coefficient.

    arguments:
        traj_file: str - trajectory file
        t0: int        - timestep when equilibrium starts

    returns:
        self_diffusion_coefficient - float

    """
    MSD, _ = get_msd(traj_file, reference="initial")
    self_diffusion_coefficient = calculate_self_diffusion_coefficient(MSD, t0)

    return self_diffusion_coefficient


def calculate_self_diffusion_coefficient(MSD, t0):
    """
    Take a list of mean square displacement for each timestep.

    arguments:
        MSD: list - list of mean square displacement for eachtimestep in
                    the simulation
        t0: int   - timestep when equilibrium starts


    returns:
        self_diffusion_coefficient - float

    self_diffusion_coefficient is calculated by taking the last value of the
    mean square displacement. Since MSD is calculated with the initial value as
    reference the last value will give us the slope of MSD. This presupposes
    that the material being simulated is a liquid, which will give a linear
    slope.

    """
    t = len(MSD)-t0
    self_diffusion_coefficient = (MSD[-1] - MSD[t0])/(6*t)

    return self_diffusion_coefficient
