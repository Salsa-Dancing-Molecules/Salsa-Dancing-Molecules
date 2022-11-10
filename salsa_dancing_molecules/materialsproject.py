"""Helpers for fetching data from materialsproject.org."""
from mp_api.client import MPRester
from pymatgen.io.ase import AseAtomsAdaptor


class MatClient(MPRester):
    """Materialsproject atoms query client.

    This class uses the MPRester materialsproject API client to fetch
    materials data and convert it to a format that ASE can understand.

    Example:
    from salsa_dancing_molecules.materialsproject import MatClient
    from ase.visualize import view

    # Initialise the MatClient with an API key.
    with MatClient('put_a_real_api_key_here') as client:
        # Fetch materials containing oxygen.
        atoms = client.get_atoms('O')

    # Visualise the first returned material containing oxygen.
    view(atoms[0])
    """

    def __init__(self, api_key):
        """Initialise the MatClient class with an API key.

        arguments:
            api_key - key for the materialsproject.org API
        """
        super().__init__(api_key)

    def get_atoms(self, formula):
        """Get ASE atom objects containing specfici elements.

        arguments:
            formula - chemical formula to search for, ex. 'Li-Fe-O'

        returns:
            list of ASE atom objects
        """
        structs = self.get_structures(formula)
        atoms = [
            AseAtomsAdaptor.get_atoms(struct) for struct in structs
        ]
        return atoms
