"""Program for handling startup tasks."""
from .prepare_workspace import do_preparations
from .use_custom_materials import materials_to_pickles
from .config_module import read_configuration
from .generate_json import convert_to_json
import os


def start(conf_path):
    """Run the different modules of the startup program.

    The results from running this module is:
        - A unbegun directory will be created, if it does not exist.
        - A finshed directory will be created, if it does not exist.
        - Materials section in configuration file creates pickle files of
          those atoms.
        - Json files are created for each configuration set.

    Args:
        args - argument object from argparse.
    """
    config = read_configuration(conf_path)
    for simulation_conf in config.values():
        work_path = simulation_conf["workspace_path"]
        custom_materials = simulation_conf["materials_path"]
        material_names = simulation_conf["material"]
        do_preparations(work_path)
        if custom_materials.endswith('.py'):
            materials_to_pickles(custom_materials, work_path, material_names)
        elif '.' not in custom_materials:  # check if path is directory
            for file in os.listdir(custom_materials):
                if file.endswith('.py'):
                    materials_to_pickles(custom_materials +
                                         '/'+file, work_path, material_names)
        convert_to_json(simulation_conf)
