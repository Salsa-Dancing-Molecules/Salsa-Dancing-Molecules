"""Implements molecular dynamics with constant energy."""

from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory, AsapError
from ..variables import Variables
from ..materialsproject import MatClient


def run_for_materials(formula, api_key, steps, output_path, repeat=0):
    """Run an MD simulation for Materials Project materials.

    Arguments:
        formula: str     - the formula of the materials to simulate. Ex: C-O
        api_key: str     - materialsproject.org API key for downloading
                           materials
        steps: int       - the number of 1 fs steps to run the simulation for
        output_path: str - path to which to save the generated trajectory
                           data and csv data. They get saved to
                           $output_path-$formula.traj and -.csv.
        repeat: int      - number of times to repeat the cell in each
                           dimension. (Default: 0, no repetition)
    """
    with MatClient(api_key) as client:
        atoms_list = client.get_atoms(formula)

    for (i, atoms) in enumerate(atoms_list):
        print(f'Simulating material {i + 1} of {len(atoms_list)}')

        symbols = atoms.symbols
        output_name = f'{output_path}-{symbols}'

        if repeat > 0:
            atoms = atoms.repeat(repeat)

        try:
            print(f'Simulating for {symbols}')
            run(atoms, steps, output_name)
        except AsapError as e:
            print(f'ASAP3 error for {symbols}: {e}')
            print('Trying without ASAP3...')
            run(atoms, steps, output_name, False)


def run(atoms, steps, output_path, use_asap=True):
    """Run an MD simulation for atoms.

    Arguments:
        atoms: Atoms     - ASE Atoms object for which to run the simulation.
        steps: int       - the number of steps in the simulation, one step is
                           equal to 1 fs.
        output_path:str  - path to which to save the generated trajectory
                           data. They get saved to $output_path-$formula.traj.
        use_asap: bool   - Whether to use ASAP3 to calculate the potential.
    """
    # Describe the interatomic interactions with the L-J
    # FIXME: This Lennard-Jones potential is currently hard coded for Argon.
    if use_asap:
        from asap3 import LennardJones
        atoms.calc = LennardJones(18, 0.010323, 3.40, rCut=6.625,
                                  modified=True)
    else:
        from ase.calculators.lj import LennardJones
        atoms.calc = LennardJones(epsilon=0.010323, sigma=3.40, rc=6.625)

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=40)

    # We want to run MD with constant energy using the VelocityVerlet
    # algorithm.
    output_path_traj = output_path + '.traj'
    output_path_csv = output_path + '.csv'
    dyn = VelocityVerlet(atoms, 1 * units.fs)  # 5 fs time step.
    traj = Trajectory(output_path_traj, "w", atoms)
    dyn.attach(traj.write, interval=100)

    # Generate different quantatives to save
    Var = Variables()

    def dynamics(a=atoms):
        # Saves snapshots of the state of system
        Var.Snapshot(a)

    # Now run the dynamics
    dyn.attach(dynamics, interval=10)
    dynamics()
    dyn.run(steps)

    # Convert the list to an array with given data types
    Var.list_to_array()
    # Upload the data to file
    Var.generate_file(output_path_csv)
    # Simulation is done.
    print('Molecular dynamics simulation is completed.')
