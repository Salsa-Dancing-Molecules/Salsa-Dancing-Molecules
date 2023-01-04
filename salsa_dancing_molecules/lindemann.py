"""Calculates the Lindemann parameter and check the Lindemann criterium."""

from .mean_square_displacement import calculate_msd
import numpy as np

try:
    from asap3 import Trajectory
except ImportError:
    print("asap3 import failed. This should only happen when building docs.")


def get_lindemann_parameter(traj, a, t0):
    """Read trajectory file.

    Input:
        traj: str      -trajectory file
        t0: int        -timestep when equilibrium starts
        a: float       -lattice constant

    Output:
        lidemann_parameters: array - array of time evolution averages of
                                     Lindeman parameter
        criterion: boolean - if lindemann criterion is violated;
                             if the time average lindemann parameter > 0.1
    """
    configs = Trajectory(traj)
    atom = configs[-1]
    unit_cell = atom.get_cell_lengths_and_angles()
    cell = atom.get_cell()
    cell = cell.fromcellpar(unit_cell)
    lattice = cell.get_bravais_lattice()
    MSD, MSD_avr = calculate_msd(configs, t0, "initial")
    return calculate_lindemann_parameter(a, MSD, MSD_avr[-1], lattice)


def calculate_lindemann_parameter(a, msd, msd_avr, lattice):
    """Calculate the Lindeman parameter and validate the lindemann criterion.

    Inputs:
        a: float        -lattice constant
        msd: list       -List of MSD for all timesteps

    Outputs:
        lidemann_parameters: array - array of time evolution averages of
                                     Lindeman parameter
        criterion: boolean - if lindemann criterion is violated:
                             if the time average lindemann parameter > 0.1

    Calculation depending on the lattice structure the object has.
    """
    # Calculates nearest neighbor depending on lattice structure
    if "BCC" in str(lattice):
        d = np.sqrt(3) * a / 2
    elif "CUB" in str(lattice):
        d = a / 2
    elif 'FCC' in str(lattice):
        d = a * (2 ** (-1/2))
    else:
        d = a
        criterion = ('Lattice structure was not recogniced. Lattice ' +
                     'constant is used as nearest neighbor distans, which ' +
                     'might give wrong vales. ')
    lind_parameters = np.divide(np.sqrt(msd), d)

    if np.sqrt(msd_avr) / d > 0.1:
        criterion = ('According to the Lindemann criterion the material ' +
                     'have melted.')
    else:
        criterion = ''

    return lind_parameters, criterion
