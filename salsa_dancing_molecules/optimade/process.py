"""Convert data to OPTIMADE format."""

from .adapters import get_optimade_data


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
        for struct, calc in get_optimade_data(result_csv, workspace, base_url):
            structs.write(struct.json())
            calcs.write(calc.json())
