"""Program for handling startup tasks."""
from .prepare_workspace import do_preparations
from .use_custom_materials import materials_to_pickle
from .config_module import read_configuration
import os


def start(args):
    """Run the different modules of the startup program.

    Args:
        args - argument object from argparse.
    """
    do_preparations(args.work_path)
    read_configuration(args.conf_path)
    material_names = read_configuration["material_names"]
    custom_materials = args.mat_path
    if custom_materials.endswith('.py'):
        materials_to_pickle(custom_materials, args.work_path, material_names)
    elif not '.' in custom_materials:
        for file in os.listdir(custom_materials):
            if file.endswith('.py'):
                materials_to_pickle(file, args.work_path, material_names)
