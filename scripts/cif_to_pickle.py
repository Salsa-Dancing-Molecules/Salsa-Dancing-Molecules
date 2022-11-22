from ase.io import read
from pickle import dump, load

def do_conversion(path):
    atoms_object = read(path)
    pickle_file = open("Ar.pickle", "wb")
    dump(atoms_object, pickle_file)
    pickle_file.close()

if __name__ == "__main__":
    do_conversion("./Ar.cif")