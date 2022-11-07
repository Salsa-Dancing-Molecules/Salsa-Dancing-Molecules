"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory, LennardJones, EMT


def run(steps, cell_size=5, output_path='ar.traj'):
    """Run an MD simulation for argon in a FCC configuration.

    Arguments:
        steps - the number of steps in the simulation, one step is
                equal to 1 fs.
        cell_size - the number of repetitions in all dimensions of the
                    minimal unit cell. Default is a 5*5*5 repetition.
        output_path - path to which to save the generated trajectory
                      data. Default is to save to "ar.traj".
    """
    # Set up a crystal
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              symbol="Ar",
                              size=(cell_size, cell_size, cell_size),
                              latticeconstant=5.256,
                              pbc=True)

    # Describe the interatomic interactions with the L-J
    atoms.calc = LennardJones(18, 0.010323, 3.40, rCut=6.625, modified=True)

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=40)

    # We want to run MD with constant energy using the VelocityVerlet
    # algorithm.
    dyn = VelocityVerlet(atoms, 1 * units.fs)  # 5 fs time step.
    traj = Trajectory(output_path, "w", atoms)
    dyn.attach(traj.write, interval=100)

    def printenergy(a=atoms):
        """Print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB),
                                 epot + ekin))

    # Now run the dynamics
    dyn.attach(printenergy, interval=10)
    printenergy()
    dyn.run(steps)
