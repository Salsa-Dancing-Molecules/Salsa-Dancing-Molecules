"""Module for handling custom materials."""
from pickle import dump
import os, importlib, sys


def get_default_value(material, key):
    """Get default value instead of keyerror."""
    return None if not key in material else material[key]


def materials_to_pickles(python_modules_path, materials_path, material_names):
    """Import atoms object from python file and save as pickle."""
    module_name = os.path.basename(python_modules_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, python_modules_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    for material_name in material_names:
        atoms_obj = getattr(module, material_name)
        pickle_file = open(materials_path+material_name+".pickle", 'wb')
        dump(atoms_obj, pickle_file)
        pickle_file.close()
