import json
from pickle import load

def handle_files(file_path):
    """Reads a specified .json file and extracts atoms object"""
    f = open(file_path)
    simulation_info = json.load(f)
    material_path = simulation_info["material"]
    f = open(material_path, "rb")
    atoms_object = load(f)
    return simulation_info, atoms_object