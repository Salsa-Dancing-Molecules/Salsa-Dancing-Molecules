"""Module containing the main function of the simulation software."""
import argparse
import sys
from ..simulations import argon, nve
from ..command_plot import data_plot
from ..startup import startup_script


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
                            help='Output_path: filename which saves ' +
                            'trajectory data and simulation data. Default ' +
                            'is "X"',
                            nargs='?', default="X")

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
                            help=('Output file for trajectory data and '
                                  'simulation data. The file will be named '
                                  '$output_file-$formula.traj and -.csv '
                                  'for each material'))
    plot_parser = command_parser.add_parser(
        'plot', help='Plot the simulation data with four plots or '
        'specify a variable to get a single plot.')

    plot_parser.add_argument('--show',
                             help=('Open up a window to show plot/plots,'
                                   ' default: do not show'),
                             default=False, action='store_true')

    plot_parser.add_argument('filename',
                             help=('The name of the file containing datafile,'
                                   ' default: X.csv'), nargs='?',
                             default='X.csv')

    plot_parser.add_argument('image_file',
                             help=('The name of the file of the saved plot,'
                                   ' default: Image.png'), nargs='?',
                             default='Image.png')

    plot_parser.add_argument('variable',
                             help=('Possible single plots of variables:'
                                   ' Ekin, Epot, Temp, Pres, cnve '
                                   ), nargs='?', default='-')

    startup_parser = command_parser.add_parser(
        'startup', help='Script for generating the necessary files to '
        'run the program')

    startup_parser.add_argument('config_path',
                                help=('Path to simulation config'))

    args = parser.parse_args()

    if 'formula' in args:
        nve.run_for_materials(args.formula, args.api_key, args.steps,
                              args.output_file, args.repeat)
    elif 'filename' in args:
        data_plot(args.variable, args.filename, args.image_file, args.show)

    elif 'steps' in args:
        argon.run(args.steps, args.cell_size, args.output_path)

    elif 'config_path' in args:
        startup_script.start(args.config_path)


if __name__ == '__main__':
    main()
