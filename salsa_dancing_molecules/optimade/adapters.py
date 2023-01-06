"""Module containing adapters for conversions to OPTIMADE formats."""

from .models import (
    SingleSimulationResultAttributes,
    AggregateSimulationResultAttributes
)

from optimade.models import (
    Species,
    StructureResource,
    StructureResourceAttributes,
    Link,
)
from ase import Atoms

import csv
import functools
import json
import numpy
import os
import pickle
import uuid
from collections import Counter
from time import time as now


def fix_length_anon_gen(length, accumulator=''):
    """Enumerate anonymous formulas with fix length.

    Enumerate anonymous formulas with a fix length.

    length == 0 ->
       A, B, C, D, ..., Z
    length == 1 ->
       Aa, Ab, ..., Az, Ba, Bb, ..., Bz, Za, ... Zz

    There is no upper limit for length other than platform memory
    limits.

    argumens:
        length: int - length of the resulting string
        accumulator: str - internal help argument; leave unset

    yields:
        permutation: str - a permutation in the sequence
    """
    upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_case = 'abcdefghijklmnopqrstuvwxyz'
    alphabet = upper_case if accumulator == '' else lower_case

    if length > 0:
        for letter in alphabet:
            yield from fix_length_anon_gen(length - 1, accumulator + letter)
    else:
        for letter in alphabet:
            yield accumulator + letter


def variable_length_anon_gen():
    """Enumerate anonymous formulas with variable length.

    Generator that yields permutations for anonymous formulas of a
    variable length.

    Example output:
      A, B, C, ..., Z, Aa, Ab, ..., Zz, Aaa, Aab, ..., Aaz, Aba, ..., Abz, ...,
      Zzz

    yields:
      variable length anonymous formula: str
    """
    length = 0
    while True:
        yield from fix_length_anon_gen(length)
        length += 1


def get_unique_elements(atoms):
    """Return a list of unique elements in an atoms object.

    arguments:
        atoms: ase.Atoms - ASE atoms object

    returns:
        element_list: list(str) - list of unique elements in the
                                  object
    """
    # The OPTIMADE specification requires that the list of elements is
    # alphabetically sorted, hence the sorted() call.
    return sorted(list(set(atoms.get_chemical_symbols())))


def get_element_ratios(atoms):
    """Return the ratios of different chemical elements in an atoms object.

    Returns a list of the ratios of unique elements in the atoms
    object. Methane, CH4, would return [0.2, 0.8].

    NOTE: The order of ratios is the same as the elements returned by
          get_unique_elements().

    arguments:
        atoms: ase.Atoms - ASE atoms object

    returns:
        element_ratios: list(float) - a list of floats containing the
                                      ratios of different elements in
                                      the atoms object
    """
    elements = atoms.get_chemical_symbols()

    total_element_count = len(elements)

    # Count the different elements in the material.
    counts = dict(Counter(elements))

    # Get unique elements since the ratio list must have the same
    # sorting as the element list according to the OPTIMADE
    # specfication.
    unique_elements = get_unique_elements(atoms)

    return [counts[element] / total_element_count for
            element in unique_elements]


def get_anonymous_formula(atoms):
    """Generate anonymous formula for an atoms object.

    The OPTIMADE specification for elements has a field called
    chemical_formula_anonymous. This field needs a formula where the
    elements are sorted left to right by proportion and then have
    their elements replaced by letters A, B, ..., Z, Aa, Ab, ..., Zz.

    As an example, ethanol, C2H5OH, has the anonymous formula A6B2C.

    arguments:
        atoms: ase.Atoms - ASE atoms ojbect

    returns:
        anonymous_formula: str - anonymous chemical formula
    """
    elements = atoms.get_chemical_symbols()

    # Count the different elements in the object for later sorting.
    count_dict = dict(Counter(elements))

    gcd = numpy.gcd.reduce([count_dict[val] for val in count_dict])

    # Extract all the element counts and sort them largest to
    # smallest.
    count_list = sorted([int(count_dict[element]/gcd)
                         for element in count_dict.keys()])
    count_list.reverse()

    # Build the anonymous formula by iterating over all the counts and
    # concatenating them with symbols from the anonymous formula
    # generator.
    anon_formula = ''
    symbol = variable_length_anon_gen()
    for count in count_list:
        anon_formula = (f'{anon_formula}{next(symbol)}'
                        f'{count if count > 1 else ""}')

    return anon_formula


def get_reduced_formula(atoms):
    """Get a reduced chemical formula.

    Returns a reduced chemical formula where all the constituents have
    a GCD of one for their element counts.

    arguments:
        atoms: ase.Atoms - atoms object for which to return a reduced
                           formula

    returns:
        reduced_formula: str - a reduced chemical formula
    """
    elements = atoms.get_chemical_symbols()

    # Count the different elements in the object for later sorting.
    count_dict = dict(Counter(elements))

    gcd = numpy.gcd.reduce([count_dict[val] for val in count_dict])

    formula_list = sorted([(key, int(count_dict[key]/gcd))
                           for key in count_dict])

    return ''.join([f'{symbol}{count if count > 1 else ""}'
                    for (symbol, count) in formula_list])


def get_optimade_structure(attributes):
    """Construct an OPTIMADE structure from attributes.

    Takes a finished SimulationResultAttributes object and turns it
    into an OPTIMADE structure record.

    arguments:
        attributes: SimulationResultAttributes - attributes to encapsulate

    returns:
        optimade_structure: optimade.models.StructureResource
                            - OPTIMADE materials entry
    """
    return StructureResource(id=str(uuid.uuid1()), attributes=attributes)


def get_species_list(atoms):
    """Get a list of elements present in the atoms object.

    This function returns a list if OPTIMADE species objects to be
    used in an OPTIMADE structure entry.

    arguments:
        atoms: ase.Atoms - ASE atoms object

    returns:
        species_list: list(optimade.models.Species()) - list of
            OPTIMADE speciec objects
    """
    species_list = []
    for symbol in get_unique_elements(atoms):
        species_list.append(Species(
            name=symbol,
            chemical_symbols=[symbol],
            concentration=[1.0]))
    return species_list


def fill_standard_fields(sim_result, atoms):
    """Fill in required standard OPTIMADE values in SimulationResultAttributes.

    Performs a partial application of the constructor of a
    SimulationResultAttributes object where standard mandatory values
    are filled in. The partially applied class is then returned for
    further initialisation.

    arguments:
        sim_result: OPTIMADE attribute - an OPTIMADE attribute object
                                         to partially fill-in
        atoms: ase.Atoms - atoms used during the simulation

    returns:
        attributes: SimulationResultAttributes - a partially
            constructed SimulationResultAttributes with standard
            OPTIMADE values filled in
    """
    unique_elements = get_unique_elements(atoms)
    dimension_types = [int(pbc) for pbc in atoms.get_pbc()]
    species_list = get_species_list(atoms)
    return functools.partial(
            sim_result,
            last_modified=int(now()),
            elements=unique_elements,
            nelements=len(unique_elements),
            elements_ratios=get_element_ratios(atoms),
            chemical_formula_descriptive=atoms.get_chemical_formula(),
            chemical_formula_reduced=get_reduced_formula(atoms),
            chemical_formula_anonymous=get_anonymous_formula(atoms),
            lattice_vectors=atoms.get_cell().tolist(),
            dimension_types=dimension_types,
            nperiodic_dimensions=sum(dimension_types),
            cartesian_site_positions=atoms.get_positions().tolist(),
            nsites=atoms.get_global_number_of_atoms(),
            species=species_list,
            species_at_sites=atoms.get_chemical_symbols(),
            structure_features=[])


def fill_simulation_config(sim_result, atoms, config):
    """Fill an OPTIMADE structure with simulation configuration info.

    Performs a partial application on sim_result with fields that
    contain the simulation configuration.

    arguments:
        sim_result: OPTIMADE attribute - an OPTIMADE attribute object
                                         to partially fill-in
        atoms: ase.Atoms - atoms used during the simulation

    returns:
        partial application of sim_result
    """
    potential = config['potential']
    kim_model = config['kim-model'] if potential == 'openkim' else None
    target_temperature = None
    if config['ensemble'] == 'NVT':
        target_temperature = int(config['target-temperature'])
    volume_scale = 1
    if 'volume-scale' in config:
        volume_scale = float(config['volume-scale'])

    return functools.partial(
            sim_result,
            ensemble=config['ensemble'],
            potential=potential,
            kim_model=kim_model,
            initial_temperature=int(config['initial-temperature']),
            target_temperature=target_temperature,
            volume_scale=volume_scale,
    )


def get_optimade_calculation_single(entry, atoms, config):
    """Return an OPTIMADE compliant simulation attribute entry.

    Convert CSV calculation data for a single simulation into an
    OPTIMADE compliant attribute record.

    arguments:
        entry: dict()      - dict containing CSV calculation entries
        atoms: ase.Atoms() - atoms object used during the simulation
        config: dict()     - dict containing the simulation
                             configuration

    returns:
        simulation_result: .models.SingleSimulationResultAttributes -
            OPTIMADE attribute record
    """
    diff_coeff = entry['self_diffusion_coefficient']
    attr = fill_standard_fields(SingleSimulationResultAttributes, atoms)
    attr = fill_simulation_config(attr, atoms, config)

    # The json export does not like if the debye temperature is nan.
    # Relpace it with None since it is translated to null, which is
    # okay in the json.
    debye_temperature = entry['debye_temperature']
    if debye_temperature == 'nan':
        debye_temperature = None

    return attr(
        msd_average=entry['MSD_avr'],
        self_diffusion_coefficient=diff_coeff,
        heat_capacity=entry['heat_capacity'],
        debye_temperature=debye_temperature,
        cohesive_energy=entry['cohesive_energy'],
        equilibrium_warning=entry['equilibrium_warning'],
        debye_warning=entry['debye_warning'],
    )


def get_optimade_calculation_aggregate(entry, atoms, config):
    """Return an OPTIMADE compliant simulation attribute entry.

    Convert CSV calculation data for an aggregate simulation into an
    OPTIMADE compliant attribute record.

    arguments:
        entry: dict()      - dict containing CSV calculation entries
        atoms: ase.Atoms() - atoms object used during the simulation
        config: dict()     - dict containing the simulation
                             configuration

    returns:
        simulation_result: .models.AggregateSimulationResultAttributes
            OPTIMADE attribute record
    """
    attr = fill_standard_fields(AggregateSimulationResultAttributes, atoms)
    attr = fill_simulation_config(attr, atoms, config)

    lattice_constant = None
    try:
        lattice_constant = float(entry['Lattice constant'])
    except ValueError:
        # We might not have a lattice constant. If the material is not
        # cubic, we output vectors and angles. Skip the value if that
        # is the case.
        pass

    if entry['Lindeman criterion'] == '':
        lindeman_criterion = "False"
    else:
        lindeman_criterion = "True"

    return attr(
        # Salsa specific values below.
        lattice_constant=lattice_constant,
        bulk_modulus=entry['Bulk modulus'],
        lindeman_criterion=lindeman_criterion,
    )


def load_config(conf_path):
    """Get material and potential from the simulation configuration.

    arguments:
        conf_path: str - path to the simulation job json configuration

    returns:
        material: ase.Atoms, conf: dict() - returns the Atoms object
            used during the simulation as well as a dictionary
            containing the simulation configuration
    """
    with open(conf_path, 'r') as conf_file:
        conf = json.load(conf_file)
    with open(conf['material'], 'rb') as material_file:
        material = pickle.load(material_file)

    return material, conf


def get_optimade_calculation(workspace_path, entry):
    """Get an OPTIMADE calculation entry from simulation output.

    Returns an OPTIMADE compliant structure entry for a post
    processed simulation result.

    arguments:
        workspace_path: str - path to a simulation workspace
        entry: dict()       - dict containing simulation post process data

    returns:
        material: ase.Atoms, .models.SimulationResult -
            return the Atoms object used in the simulation
            as well as an OPTIMADE compliant structure entry
    """
    conf_path = (f'{workspace_path}/done_simulations/'
                 f'{entry["file_name"]}.json')
    if 'Lattice constant' in entry:
        if entry['Lattice constant'] == '':
            material, config = load_config(conf_path)
            return material, get_optimade_calculation_single(entry,
                                                             material,
                                                             config)
        else:
            traj_name = os.path.basename(entry['Trajectory file'])
            conf_name = f'{os.path.splitext(traj_name)[0]}.json'
            conf_path = f'{workspace_path}/done_simulations/{conf_name}'

            material, config = load_config(conf_path)
            return material, get_optimade_calculation_aggregate(entry,
                                                                material,
                                                                config)
    else:
        material, config = load_config(conf_path)
        return material, get_optimade_calculation_single(entry,
                                                         material,
                                                         config)


def get_optimade_data(result_path, workspace_path):
    """Get a generator for converting simulation results to OPTIMADE format.

    Get a generator that generates OPTIMADE compliant entries from
    simulation output

    arguments:
        result_path: str    - path to a post process results CSV file
        workspace_path: str - path to a simulation workspace

    returns:
        optimade_itr: generator of StructureResource -
                      generates OPTIMADE structure entries
    """
    with open(result_path, 'r') as f:
        reader = csv.DictReader(f)
        for entry in reader:
            material, attributes = get_optimade_calculation(workspace_path,
                                                            entry)
            struct = get_optimade_structure(attributes)

            yield struct
