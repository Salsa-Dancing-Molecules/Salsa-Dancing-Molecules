"""Module for calculating the mean square displacement of a trajectory file."""

from ase.io import read
import numpy as np


def get_msd(traj_file, reference="final"):
    """
    Read trajectory file and call calculation function.

    arguments:
        traj_file - trajectory file
        reference - string or None

    return:
        mean square displacement - list

    Example of a function call:
        get_msd(traj_file = "cu.traj@0:-1")
    or
        get_msd(traj_file = "cu.traj@0:-1", reference = "initial")

    "@0:-1" after the trajectory file name means that all the atoms objects
    will be read.
    If " reference = "initial" " is included the first atom positions will be
    used as reference. Otherwise refernce is set to the last atom positions.
    """
    configs = read(traj_file)

    return calculate_msd(configs, reference)


def calculate_msd(configs, reference="final"):
    """
    Calculate the mean square dispalcement for a trajectory file as a list.

    arguments:
        configs - list
        reference - string or None

    return:
        mean square displacement - list
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
    return MSD
