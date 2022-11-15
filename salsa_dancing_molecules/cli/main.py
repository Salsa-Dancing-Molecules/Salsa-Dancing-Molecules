"""Module containing the main function of the simulation software."""
import argparse
import sys
from ..simulations import argon


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

    args = parser.parse_args()

    if 'steps' in args:
        argon.run(args.steps, args.cell_size, args.output_path)


if __name__ == '__main__':
    main()
