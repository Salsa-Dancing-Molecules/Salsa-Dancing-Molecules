"""Program for handling startup tasks."""
from .prepare_workspace import do_preparations
from .use_custom_materials import convert_to_pickle


def start(args):
    """Run the different modules of the startup program.

    Args:
        args - argument object from argparse.
    """
    do_preparations(args.work_path)
    custom_materials = [args.mat_path]
    if custom_materials:
        convert_to_pickle(custom_materials)
