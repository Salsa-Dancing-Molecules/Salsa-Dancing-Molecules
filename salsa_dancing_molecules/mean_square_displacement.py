"""Module for calculating the mean square displacement of a trajectory file."""

from ase.io.trajectory import Trajectory
import numpy as np
from .average import average


def get_msd(traj_file, t0, reference="final"):
    """
    Read trajectory file and call calculation function.

    arguments:
        traj_file: str         - trajectory file
        t0: int                - timestep when equilibrium starts
        reference: str or None - which atom to be used as reference,can be
                                 'initial' or 'final', default is 'final'.

    return:
        mean square displacement - list

    If " reference = "initial" " is included the first atom positions will be
    used as reference. Otherwise refernce is set to the last atom positions.
    """
    configs = Trajectory(traj_file)

    return calculate_msd(configs, t0, reference)


def calculate_msd(configs, t0, reference="final"):
    """
    Calculate the mean square dispalcement for a trajectory file as a list.

    arguments:
        configs: ase.io.trajectory.Trajectory - traj file containg atom-obj.
        reference: str or None - which atom to be used as reference,can be
                                 'initial' or 'final', default is 'final'.

    return:
        MSD: list     - means square displacement
        MSD_avr: list - time evolution average of mean square displacement
    """
    N = len(configs[0])  # Number of atoms
    atom = configs[0]
    cell_lengths_and_angles = atom.get_cell_lengths_and_angles()
    x_size = cell_lengths_and_angles[0]
    y_size = cell_lengths_and_angles[1]
    z_size = cell_lengths_and_angles[2]
    atom_positions = [atom.get_positions() for atom in configs]
    atom_positions = np.array(atom_positions)

    if reference == "initial":
        reference_position = atom_positions[0]
    elif reference == "final":
        reference_position = atom_positions[-1]

    # Changes atom positions according to boundary conditions
    for time_step in range(len(atom_positions)):
        if time_step == 0:
            pass
        else:
            dr = (atom_positions[time_step] - atom_positions[time_step-1])
            for atom in dr:
                dx = atom[0]
                if (dx > x_size*0.5):
                    dx = dx - x_size
                if (dx <= -x_size*0.5):
                    dx = dx + x_size
                atom[0] = dx
                dy = atom[1]
                if (dy > y_size*0.5):
                    dy = dy - y_size
                if (dy <= -y_size*0.5):
                    dy = dy + y_size
                atom[1] = dy
                dz = atom[2]
                if (dz > z_size*0.5):
                    dz = dz - z_size
                if (dz <= -z_size*0.5):
                    dz = dz + z_size
                atom[2] = dz

            atom_positions[time_step] = atom_positions[time_step-1] + dr

    MSD = []
    # Calculates the mean square displacement using correct atom positions
    for pos in atom_positions:
        X = np.subtract(pos, reference_position)
        MSD.append(1/N*sum([(np.linalg.norm(i))**2 for i in X]))
    MSD_avr = average(t0, MSD)
    return MSD, MSD_avr
