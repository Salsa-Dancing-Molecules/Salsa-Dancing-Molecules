"""Program for loading atoms object from a file."""

import json
from pickle import load


def handle_files(file_path):
    """
    Read a specified .json file and extracts atoms object.

    Args:
        file_path - The file path to the .json file containing
                    information about the atoms object.
    """
    f = open(file_path)
    simulation_info = json.load(f)
    material_path = simulation_info["material"]
    f = open(material_path, "rb")
    atoms_object = load(f)
    return simulation_info, atoms_object
