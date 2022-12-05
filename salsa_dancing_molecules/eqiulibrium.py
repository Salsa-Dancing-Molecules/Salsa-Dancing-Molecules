"""Module for finding the "steady state" of a system."""

from pymbar.timeseries import detect_equilibration
import numpy as np
from asap3 import Trajectory


def get_eqiulibrium(traj, ensemble='NVE'):
    """
    Find the eqiulibrium of a system.

    Input:
        traj: str  - trajectory file

    Output:
        eqiulibrium: int   - timestep when equilibrium starts.
    """
    configs = Trajectory(traj)
    if ensemble == 'NVE':
        list = [atoms.get_temperature() for atoms in configs]
    elif ensemble == 'NVT':
        list = [atoms.get_potential_energy() for atoms in configs]
    else:
        list = [atoms.get_temperature() for atoms in configs]
    list = np.array(list, dtype=np.float64)
    [equilibrium, _, _] = detect_equilibration(list)

    return equilibrium