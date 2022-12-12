"""Module for running a simulation."""
from ..lennardjonesparse import parse_lj_params
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.md.andersen import Andersen
from ase import units
from asap3 import Trajectory
from ..variables import Variables


def choose_potential(potential, sim_info, use_asap, atoms):
    """Set the atoms object's calc attribute.

    The atoms object's .calc value specifies the calculator used
    in the simulation. If openkim does not work, Lennard Jones will be
    used instead. Openkim and Lennard Jones are the only ones implemented
    right now. use_asap is not relevant for openkim, only Lennard Jones.

    Args:
        potential: string - name of potential to be used.
        kim_model: string - with ID for ensemble to be chosen from openkim.
        use_asap: bool - True if asap3 is to be used instead of ASE
        atoms: atoms object to be edited.
    """
    potential = potential.lower().strip()
    if potential == "openkim":  # use openkim
        try:
            from ase.calculators.kim import KIM
            atoms.calc = KIM(sim_info['kim-model'])
        except RuntimeError:
            print(f'{sim_info["kim-model"]} is not a valid OpenKIM potential, '
                  'will use standard Lennard-Jones potential')
            potential = 'lennard-jones'
        else:
            if use_asap:
                print("OpenKIM potential used, use-asap "
                      "= True will be ignored.")
    if potential == "lennard-jones":
        element_symbols = atoms.get_chemical_symbols()
        if len(element_symbols) > 1:
            print('More than one element was inputted, will use '
                  f'LJ-parameters for {element_symbols[0]}')
        element, rc, epsilon, sigma = parse_lj_params(element_symbols[0])

        if use_asap:
            from asap3 import LennardJones
            atoms.calc = LennardJones(element, epsilon, sigma, rCut=rc,
                                      modified=True)
        else:
            from ase.calculators.lj import LennardJones
            atoms.calc = LennardJones(epsilon=epsilon, sigma=sigma, rc=rc)


def choose_ensemble(ensemble, target_temperature, atoms):
    """Create an ASE dynamics object depending on what ensemble to be used.

    Args:
        ensemble - String with the name of the ensemble.
        target_temperature - Target temperature for NVT simulation.
        atoms - Atoms object to be used.
    Returns:
        dyn - dynamics object.

    """
    ensemble = ensemble.lower()
    if ensemble == "nve":
        dyn = VelocityVerlet(atoms, 5 * units.fs)
    elif ensemble == "nvt":
        dyn = Andersen(atoms,
                       5 * units.fs,
                       temperature_K=int(target_temperature),
                       andersen_prob=0.01)  # andersen_prob maybe configurable?
    else:
        raise Exception("Invalid ensemble.")
    return dyn


def run(sim_info, atoms):
    """Run the simulation.

    Args:
        sim_info - dictionary with information on the simulation.
        atoms - atoms object to be used.
    """
    if "volume-scale" in sim_info:
        scaling = float(sim_info["volume-scale"])
        atoms.set_cell(atoms.get_cell() * scaling, scale_atoms=True)
    if type(sim_info["use-asap"]) is str:
        sim_info["use-asap"] = (sim_info["use-asap"].lower() == "true")
    choose_potential(sim_info["potential"],
                     sim_info,
                     sim_info["use-asap"],
                     atoms)
    # Initialize the momenta from the chosen initial temperature.
    init_temp = int(sim_info["initial-temperature"])
    MaxwellBoltzmannDistribution(atoms,
                                 temperature_K=init_temp)

    output_path_traj = sim_info["traj_output_path"]
    output_path_csv = sim_info["csv_output_path"]
    # Create dynamics object for simulation.
    if "target-temperature" in sim_info:
        target_temperature = sim_info["target-temperature"]
    else:
        target_temperature = None
    dyn = choose_ensemble(sim_info["ensemble"],
                          target_temperature,
                          atoms)

    traj = Trajectory(output_path_traj, "w", atoms)
    dyn.attach(traj.write, interval=100)
    # Generate different quantatives to save
    Var = Variables()
    Var.set_timestep(10)

    def dynamics(a=atoms):
        # Saves snapshots of the state of system
        Var.Snapshot(a)
        Var.increment_time()

    # Now run the dynamics
    dyn.attach(dynamics, interval=10)
    dynamics()
    dyn.run(int(sim_info["steps"]))
    # Convert the list to an array with given data types
    Var.list_to_array()
    # Upload the data to file
    Var.generate_file(output_path_csv)
    # Simulation is done.
    print('Molecular dynamics simulation is completed.')
