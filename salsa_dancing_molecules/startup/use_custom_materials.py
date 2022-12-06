"""Module for handling custom materials.

Example material can be found in:
example_simulation/materials/example_material.py
"""
from pickle import dump
import os
import importlib
import sys


def materials_to_pickles(python_modules_path, work_path, material_names):
    """Import atoms object from python file and save as pickle.

    Args:
        python_modules_path - path to file with atoms objects.
        work_path - path to workspace directory.
        material_names - list of names of the materials used.
    """
    module_name = os.path.basename(python_modules_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name,
                                                  python_modules_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    for material_name in material_names:
        # Materials prefixed with mp_ are from Materialsproject and
        # should be skipped.
        if material_name.startswith('mp_'):
            continue
        atoms_obj = getattr(module, material_name)
        pickle_file = open(work_path+"/materials/" +
                           material_name+".pickle", 'wb')
        dump(atoms_obj, pickle_file)
        pickle_file.close()
