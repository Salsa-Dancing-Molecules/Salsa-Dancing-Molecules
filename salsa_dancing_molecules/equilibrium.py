"""Module for finding the "steady state" of a system."""

from pymbar.timeseries import detect_equilibration
import numpy as np
from asap3 import Trajectory


def get_equilibrium(configs, ensemble='NVE'):
    """
    Find the eqiulibrium of a system.

    Input:
        configs: ase.io.trajectory.Trajectory - traj file containg atom-obj.

    Output:
        eqiulibrium: int   - timestep when equilibrium starts.
        warning: bool      - True if equilibrium is reached in the last 10%
    """
    if ensemble == 'NVE':
        list = [atoms.get_temperature() for atoms in configs]
    elif ensemble == 'NVT':
        list = [atoms.get_potential_energy() for atoms in configs]
    else:
        list = [atoms.get_temperature() for atoms in configs]
    list = np.array(list, dtype=np.float64)
    [equilibrium, _, _] = detect_equilibration(list)

    # Check if equilibrium is reached in the last 10% of the timesteps
    warning = 0.9 < equilibrium/len(list)

    return equilibrium, warning
