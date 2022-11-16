"""Module containing the main function of the simulation software."""
import argparse
import sys
from ..simulations import argon, nve


def main():
    """Run the simulation software."""
    parser = argparse.ArgumentParser(
        description="Molecular dynamics simulation program")
    command_parser = parser.add_subparsers(help='Simulation commands')

    run_parser = command_parser.add_parser('run', help='Run the argon example')

    run_parser.add_argument('steps',
                            help='Steps: Number of steps to run' +
                            '(1 step = 1 fs)', type=int)
    run_parser.add_argument('cell_size',
                            help='Cellsize: Number of repetitions in all' +
                            'dimensions of the minimal unit cell. Default' +
                            'is a 5*5*5 repetition.',
                            nargs='?', default=5, type=int)

    run_parser.add_argument('output_path',
                            help='path to which to save the generated' +
                            'trajectory data. Default is to save to "ar.traj"',
                            nargs='?', default="ar.traj")

    nve_parser = command_parser.add_parser('nve', help='Run an NVE simulation')
    nve_parser.add_argument('formula',
                            help=('Chemical formula of the material to fetch '
                                  'from materialsproject and simulate.  '
                                  '(Default: Ar)'), default='Ar')
    nve_parser.add_argument('--repeat',
                            help=('Optional number to repeat the '
                                  'material cell in all three dimensions. '
                                  'This is usefull if the downloaded '
                                  'material cell is too small.'),
                            type=int, default=0)
    nve_parser.add_argument('api_key',
                            help=('API key for materialsproject.org '
                                  'needed for fetching material structures to '
                                  'simulate.'))
    nve_parser.add_argument('steps',
                            help=('Steps: Number of steps to run '
                                  '(1 step = 1 fs)'), type=int)
    nve_parser.add_argument('output_file',
                            help=('Output file for trajectory data. '
                                  'The file will be named '
                                  '$output_file-$formula.traj '
                                  'for each material'))

    args = parser.parse_args()

    if 'formula' in args:
        nve.run_for_materials(args.formula, args.api_key, args.steps,
                              args.output_file, args.repeat)
    elif 'steps' in args:
        argon.run(args.steps, args.cell_size, args.output_path)


if __name__ == '__main__':
    main()
