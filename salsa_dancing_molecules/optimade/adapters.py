"""Module containing adapters for conversions to OPTIMADE formats."""

from .models import (
    SimulationResult,
    SimulationResultAttributes,
)

from optimade.models import (
    Species,
    StructureResource,
    StructureResourceAttributes,
    Link,
)
from ase import Atoms

import csv
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


def get_optimade_structure(atoms):
    """Convert an ASE atoms object into an OPTIMADE materials entry.

    Takes an ASE atom object and converts it into an OPTIMADE
    materials entry.

    arguments:
        atoms: ase.Atoms - atoms object to convert

    returns:
        optimade_structure: optimade.models.StructureResource
                            - OPTIMADE materials entry
    """
    unique_elements = get_unique_elements(atoms)
    dimension_types = [int(pbc) for pbc in atoms.get_pbc()]

    species_list = []
    for symbol in get_unique_elements(atoms):
        species_list.append(Species(
            name=symbol,
            chemical_symbols=[symbol],
            concentration=[1.0]))

    # The OPTIMADE toolkit has internal sanity checks for all these
    # fields so at the moment, this has no unit test since a unit test
    # would basically just be checking that the values set in the
    # fields are the values present in the fields.
    attributes = StructureResourceAttributes(
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
            structure_features=[]
    )

    return StructureResource(id=str(uuid.uuid1()), attributes=attributes)


def get_optimade_calculation_single(entry):
    """Return an OPTIMADE compliant calculation entry.

    Convert CSV calculation data for a single simulation into an
    OPTIMADE compliant calculations record.

    arguments:
        entry: dict() - dict containing CSV calculation entries

    returns:
        simulation_result: .models.SimulationResult - OPTIMADE calculation
    """
    diff_coeff = entry['self_diffusion_coefficient']
    attr = SimulationResultAttributes(
        last_modified=int(now()),
        _salsa_msd_average=entry['MSD_avr'],
        _salsa_self_diffusion_coeff=diff_coeff,
        _salsa_heat_capacity=entry['heat_capacity'],
        _salsa_debye_temperature=entry['debye_temperature'],
        _salsa_cohesive_energy=entry['cohesive_energy'],
        _salsa_equilibrium_warning=entry['equilibrium_warning'],
        _salsa_debye_warning=entry['debye_warning'],
    )

    return SimulationResult(id=str(uuid.uuid1()), attributes=attr)


def get_optimade_calculation_aggregate(entry):
    """Return an OPTIMADE compliant calculation entry.

    Convert CSV calculation data for an aggregate simulation into an
    OPTIMADE compliant calculations record.

    arguments:
        entry: dict() - dict containing CSV calculation entries

    returns:
        simulation_result: .models.SimulationResult - OPTIMADE calculation
    """
    attr = SimulationResultAttributes(
        last_modified=int(now()),
        _salsa_lattice_constant=entry['Lattice constant'],
        _salsa_bulk_modulus=entry['Bulk modulus'],
        _salsa_error_message=entry['Error message'],
        # FIXME: This is a list in text format which is not OPTIMADE
        # compatible. Changing the source data is preferred.
        # _lindeman_over_time=entry['Lindeman parameter over time'], #
        _salsa_lindeman_criterion=entry['Lindeman criterion'],
    )

    return SimulationResult(id=str(uuid.uuid1()), attributes=attr)


def get_optimade_calculation(workspace_path, entry):
    """Get an OPTIMADE calculation entry from simulation output.

    Returns an OPTIMADE compliant calculations entry for a post
    processed simulation result.

    arguments:
        workspace_path: str - path to a simulation workspace
        entry: dict()       - dict containing simulation post process data

    returns:
        conf_path, calculation_entry: str, .models.SimulationResult -
            return the path to the simulation configuration json file
            as well as an OPTIMADE compliant calculations entry
    """
    conf_path = (f'{workspace_path}/done_simulations/'
                 f'{entry["file_name"]}.json')
    if 'Lattice constant' in entry:
        if entry['Lattice constant'] == '':
            return conf_path, get_optimade_calculation_single(entry)
        else:
            traj_name = os.path.basename(entry['Trajectory file'])
            conf_name = f'{os.path.splitext(traj_name)[0]}.json'
            conf_path = f'{workspace_path}/done_simulations/{conf_name}'
            return conf_path, get_optimade_calculation_aggregate(entry)
    else:
        return conf_path, get_optimade_calculation_single(entry)


def get_optimade_data(result_path, workspace_path,
                      base_url='https://example.com'):
    """Get a generator for converting simulation results to OPTIMADE format.

    Get a generator that generates OPTIMADE compliant entries from
    simulation output. The base_url argument is used for generating
    link references between the different entries and should be set to
    the URL from which the database will be served.

    arguments:
        result_path: str    - path to a post process results CSV file
        workspace_path: str - path to a simulation workspace
        base_url: str       - URL from which the OPTIMADE database
                              will be served

    returns:
        optimade_itr: generator of StructureResource, SimulationResult -
                      generates pairs of an OPTIMADE structure entry
                      with a corresponding OPTIMADE calculation
    """
    with open(result_path, 'r') as f:
        reader = csv.DictReader(f)
        for entry in reader:
            conf_path, sim_res = get_optimade_calculation(workspace_path,
                                                          entry)

            with open(conf_path, 'r') as conf_file:
                conf = json.load(conf_file)
            with open(conf['material'], 'rb') as material_file:
                material = pickle.load(material_file)
            struct = get_optimade_structure(material)

            struct_link = Link(
                href=f'{base_url}/structures/{struct.id}',
                meta={'description': f'Calculation simulation structure.'},
            )
            sim_res.links = struct_link

            calc_link = Link(
                href=f'{base_url}/calculations/{sim_res.id}',
                meta={'description': f'Calcultion for structure.'},
            )
            struct.links = calc_link

            yield struct, sim_res
