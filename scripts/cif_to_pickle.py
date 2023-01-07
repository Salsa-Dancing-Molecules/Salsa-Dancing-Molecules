"""Module for converting .cif file to pickle file."""
from ase.io import read
from pickle import dump


def do_conversion(path):
    """Take path to .cif file and do conversion."""
    atoms_object = read(path)
    # TODO: Add argument for output path.
    pickle_file = open("Ar.pickle", "wb")
    dump(atoms_object, pickle_file)
    pickle_file.close()


if __name__ == "__main__":
    do_conversion("./Ar.cif")
