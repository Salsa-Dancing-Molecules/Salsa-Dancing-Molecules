"""Convert data to OPTIMADE format."""

import json

from .adapters import get_optimade_data


def to_json(struct):
    """Convert an OPTIMADE structure to json.

    The python implementation of the OPTIMADE server expects the
    attribute fields to be present directly in the entry and not under
    the attributes key. Move all attribute entries up into the
    structure itself.

    arguments:
        struct: optimade structure - structure to convert to json

    returns:
        json: str - json representation of the OPTIMADE data
    """
    data = json.loads(struct.json())
    attributes = data['attributes']

    for key, value in attributes.items():
        data[key] = value
    data.pop('attributes')

    return json.dumps(data)


def run(result_csv, workspace, json_out):
    """Generate OPTIMADE compliant json files from simulation results.

    Create the files '{json_out}' with OPTIMADE compliant data.

    arguments:
        result_csv: str - path to simulation results CSV file
        workspace: str  - path to simulation workspace
        json_out: str   - path to output json file
    """
    with open(f'{json_out}', 'w') as structs:
        structs.write('[')
        first = True

        for struct in get_optimade_data(result_csv, workspace):
            if not first:
                structs.write(',')
            else:
                first = False

            structs.write(to_json(struct))

        structs.write(']')
