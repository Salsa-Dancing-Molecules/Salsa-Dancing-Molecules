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


def run(result_csv, workspace, base_url, json_out):
    """Generate OPTIMADE compliant json files from simulation results.

    Create the two files '{json_out}calculations.json' and
    '{json_out}structures.json' with OPTIMADE compliant data.

    The base_url parameter is used for internal references in the
    database and should be the URL from which the OPTIMADE database is
    served.

    arguments:
        result_csv: str - path to simulation results CSV file
        workspace: str  - path to simulation workspace
        base_url: str   - URL from which the OPTIMADE database will be
                          served
        json_out: str   - prefix to use for generated result files
    """
    with (open(f'{json_out}structures.json', 'w') as structs,
          open(f'{json_out}calculations.json', 'w') as calcs):
        structs.write('[')
        calcs.write('[')
        first = True

        for struct, calc in get_optimade_data(result_csv, workspace, base_url):
            if not first:
                structs.write(',')
                calcs.write(',')
            else:
                first = False

            structs.write(to_json(struct))
            calcs.write(to_json(calc))

        structs.write(']')
        calcs.write(']')
