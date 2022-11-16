"""
Function for calculating lattice constant and bulk modulus.

Takes a trajectory file and outputs lattice constant (in Angstrom),
bulk modulus (in GPa) as float values and
cohesive energy (in eV/atom)
"""

from ase.units import kJ
from ase.eos import EquationOfState
from asap3 import Trajectory
import numpy as np
import os
from .equilibrium import get_equilibrium


def get_bulk_properties(work_path, ensemble):
    """Get bulk properties.

    Calculate lattice constant, bulk modulus and get the trajectory file with
    the optimal volume.

    args:
        work_path:str     - name of work path
        ensemble:str      - the ensemble for the system, ei 'NVT' or 'NVE'

    returns:
        a: float          - lattice constant (in Angstrom).
        B: float          - bulk modulus (in GPa).
        optimal_traj: str - path / file name of the optimal trajectory file.

    """
    avg_energies = []
    avg_volumes = []
    # for each trajectory file, calculate average potential energy and volume
    # after the equilibrium time and save these to lists.
    traj_dir = work_path.rstrip('/') + '/output/traj'
    traj_list = [os.path.join(traj_dir, file) for file in os.listdir(traj_dir)]
    if len(traj_list) > 3:
        for traj_file in traj_list:
            configs = Trajectory(traj_file)
            t0 = get_equilibrium(traj_file, ensemble)
            pot_energies = [atom.get_potential_energy() for atom in configs]
            avg_energies.append(sum(pot_energies[t0:]) /
                                len(pot_energies[t0:]))
            volumes = [atom.get_volume() for atom in configs]
            avg_volumes.append(sum(volumes[t0:]) / len(volumes[t0:]))

        return calculate_bulk_properties(traj_list, avg_energies, avg_volumes)
    else:
        print('Amount of trajectory files must be 4 or more.')


def calculate_bulk_properties(traj_list, avg_energies, avg_volumes):
    """Calculate bulk properties.

    args:
        traj_list: list     - list of paths to trajectory files
        avg_energies: list  - list of average energies
        avg_volumes:        - list of average volumes

    returns:
        a: float          - lattice constant (in Angstrom).
        B: float          - bulk modulus (in GPa).
        optimal_traj: str - file name of the optimal trajectory file.

    """
    eos = EquationOfState(avg_volumes, avg_energies)
    try:
        v0, _, B0 = eos.fit()
    except ValueError as e:
        print(e)
        print('Please try another guess of lattice constant.')
        print('Bulk modulus and lattice constant could not be ' +
              'calculated. No optimal volume found.')
        return None

    # unit conversion to get bulk modulus in GPa.
    B = B0 / kJ * 1.0e24

    # get the trajectory files that is the closest to the optimal volume.
    diff_array = np.absolute(avg_volumes - v0)
    index = diff_array.argmin()
    optimal_traj = traj_list[index]

    # get the structure of the lattice
    atom = Trajectory(optimal_traj)[-1]
    unit_cell = atom.get_cell_lengths_and_angles()
    cell = atom.get_cell()
    cell = cell.fromcellpar(unit_cell)
    lattice = cell.get_bravais_lattice()
    N = atom.get_global_number_of_atoms()

    # do appropritate calculation depending on lattice structure
    if 'FCC' in str(lattice):
        a = (4 * v0 / float(N)) ** (1/3)

    elif 'BCC' in str(lattice):
        a = (2 * v0 / float(N)) ** (1/3)

    elif 'CUB' in str(lattice):
        a = (v0 / float(N)) ** (1/3)

    return a, B, optimal_traj
