"""Program for handling startup tasks."""
from .prepare_workspace import do_preparations
from .use_custom_materials import materials_to_pickles
from .config_module import read_configuration
from .generate_json import convert_to_json
from ..materialsproject import prepare_materials as mp_prepare_materials
import os
import sys


def start(args):
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
    config = read_configuration(args.config_path)
    for simulation_conf in config.values():
        work_path = simulation_conf["workspace_path"]
        material_names = simulation_conf["material"]

        if work_path[0] != '/':
            print('Error: workspace_path must be an absolute path!')
            sys.exit(1)

        do_preparations(work_path)

        # If we only have Materialproject materials, materials_path
        # might not exist in the configuration. Only process custom
        # materials if the path exists.
        if "materials_path" in simulation_conf:
            custom_materials = simulation_conf["materials_path"]
            if custom_materials[0] != '/':
                print('Error: materials_path must be an absolute path!')
                sys.exit(1)

            if custom_materials.endswith('.py'):
                materials_to_pickles(custom_materials, work_path,
                                     material_names)
            elif os.path.isdir(custom_materials):  # check if path is directory
                for file in os.listdir(custom_materials):
                    if file.endswith('.py'):
                        materials_to_pickles(custom_materials +
                                             '/'+file, work_path,
                                             material_names)

        # Find all Materialsproject materials. They are prefixed with "mp_".
        mp_materials = list(filter(lambda mat: mat.startswith('mp_'),
                                   material_names))
        if len(mp_materials) > 0:
            if not args.api_key:
                print('Error: An API key must be provided on the '
                      'command line when using a Materialsproject material!')
                sys.exit(1)

            downloaded_materials = mp_prepare_materials(args.api_key,
                                                        work_path +
                                                        '/materials',
                                                        mp_materials)

            # Replace all mp_ prefixed materials with the actual
            # downloaded materials.
            simulation_conf['material'] = list(filter(lambda mat: not
                                                      mat.startswith('mp_'),
                                                      material_names))
            simulation_conf['material'].extend(downloaded_materials)

        convert_to_json(simulation_conf)
