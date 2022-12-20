"""Module containing the main function of the simulation software."""
import argparse
import sys


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

    nve_parser.add_argument('--potential',
                            help=('Potential from taken from OpenKIM '
                                  'database. If no potential is given a '
                                  'standard Lennard-Jones potential '
                                  'will be used'), default='Lennard-Jones')

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

    worker_parser = command_parser.add_parser('worker',
                                              help='Arguments for workers.')
    worker_parser.add_argument('work_path', help='Path to working directory.')

    startup_parser = command_parser.add_parser(
        'startup', help='Script for generating the necessary files to '
        'run the program')

    startup_parser.add_argument('--api-key',
                                help=('API key for materialsproject. '
                                      'Only needed if such a material is '
                                      'included in the configuration.'),
                                type=str)

    startup_parser.add_argument('--job',
                                help=("Name of the job."),
                                default="TFYA99",
                                type=str)

    startup_parser.add_argument('--use_devel',
                                help=("The type of job to be run is 'devel'."),
                                action='store_true')

    startup_parser.add_argument('--time',
                                help=("Max time for the job. "
                                      "Format: hh:mm:ss"),
                                default="00:05:00",
                                type=str)

    startup_parser.add_argument('--nodes',
                                help=("Number of nodes to be used."),
                                default="1",
                                type=str)

    startup_parser.add_argument('--cores',
                                help=("Number of cores to be used."),
                                default="32",
                                type=str)

    startup_parser.add_argument('--exclusive',
                                help=("Set flag to run the job as exclusive"),
                                action='store_true')

    startup_parser.add_argument('config_path',
                                help=('Path to simulation config'))

    post_parser = command_parser.add_parser('post_simulation',
                                            help=('Run post simulation '
                                                  'calculations'))

    post_parser.add_argument('post_work_path',
                             help=('Path to workspace directory'))

    volume_parser = command_parser.add_parser('volume_process',
                                              help=('Run post volume-' +
                                                    'simulation calculations'))

    volume_parser.add_argument('volume_work_path',
                               help=('Path to workspace directory'))

    args = parser.parse_args()

    if 'formula' in args:
        from ..simulations import nve
        nve.run_for_materials(args.formula, args.api_key, args.steps,
                              args.output_file, args.potential, args.repeat)
    elif 'filename' in args:
        from ..command_plot import data_plot
        data_plot(args.variable, args.filename, args.image_file, args.show)

    elif 'steps' in args:
        from ..simulations import argon
        argon.run(args.steps, args.cell_size, args.output_path)

    elif 'work_path' in args:
        from ..worker_process import worker_process
        worker_process.start(args.work_path)

    elif 'config_path' in args:
        from ..startup import startup_script
        startup_script.start(args)

    elif 'post_work_path' in args:
        from ..post_process import post_process
        post_process.run_post_calculations(args.post_work_path)

    elif 'volume_work_path' in args:
        from ..volume_process import volume_process
        volume_process.start(args.volume_work_path)


if __name__ == '__main__':
    main()
