"""Helpers for fetching data from materialsproject.org."""
import pickle
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
            api_key: str - key for the materialsproject.org API
        """
        super().__init__(api_key)

    def get_atoms(self, formula):
        """Get ASE atom objects containing specfici elements.

        arguments:
            formula: str - chemical formula to search for, ex. 'Li-Fe-O'

        returns:
            list of ASE atom objects
        """
        structs = self.get_structures(formula)
        atoms = [
            AseAtomsAdaptor.get_atoms(struct) for struct in structs
        ]
        return atoms

    def _pickle(self, atom, output_dir, id=-1):
        """Pickle an atom.

        Pickle an atom and save it to a file on disk named the
        material's chemical formula and an optional index number.

        arguments:
            atom: ASE atom - atom object to pickle
            output_dir: str - directory in which to save the pickles
            id: int - the numerical ID to append to the file name. -1
                      means no ID is wanted

        returns:
            (success: bool, name: str)
                success is True if the material was successfully
                downloaded and name is the name of the resulting
                pickle file in output_dir
        """
        try:
            if id == -1:
                name = f"{atom.get_chemical_formula()}.pickle"
            else:
                name = f"{atom.get_chemical_formula()}-{id}.pickle"
            path = f"{output_dir}/{name}"

            with open(path, 'xb') as file:
                pickle.dump(atom, file)
            return (True, name)
        except FileExistsError:
            # If the atom without an ID collided, automatically create
            # one with an ID.
            if id == -1:
                return self._pickle(atom, output_dir, 0)
            else:
                return (False, "")

    def pickle_atoms(self, formula, output_dir):
        """Download and pickle a material.

        Download all configurations fro a material with a given
        formula and save a pickled ASE atoms in output_dir.

        Atoms are saved to files named their chemical formula with
        the file extension .pickle. Materials with the same chemical
        formula will have an index number appended at the end of the
        material.

        arguments:
            formula:    str - chemical formula to search for, ex. 'Li-Fe-O'
            output_dir: str - path to a directory in which to save the
                              atom objects

        returns:
            saved_atoms: str - list of names of the pickle files
                               saved in output_dir
        """
        atoms = self.get_atoms(formula)
        saved_atoms = []
        for atom in atoms:
            # To avoid overwriting an atom object with identical
            # chemical formula, append an id that is incremented until
            # one that is free is found.
            id = -1
            success = False
            while not success:
                success, name = self._pickle(atom, output_dir, id)
                id += 1
            saved_atoms.append(name)

        return saved_atoms
