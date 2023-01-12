#!/usr/bin/env python3
import pickle
import numpy
from numpy.lib.recfunctions import append_fields

def _read_xyzlist_formulas(xyzfile):
    """Read the tmqm file consisting of xyz-formatted segments
    and pick out the formulas.

    Args:
        file(str): The filename of the tmqm xyz file.

    Returns:
        numpy.ndarray: A list of formulas in the order they appear in the file.
    """
    f = open(xyzfile, "r")
    formulas = []
    for line in f:
        if line.startswith("CSD_code"):
            fields = line.split("|")
            sto = fields[3]
            formula = sto.partition("=")[2].strip()
            formulas.append(formula)
    f.close()
    return numpy.array(formulas,dtype=str)

def read_tmqm_properties(csvfile,xyzfile):
    """Reads the csv and xyz files comprising the tmqm dataset.

    Args:
        csvfile(str): Filename of the tmqm dataset csv file.
        xyzfile(str): Filename of the tmqm dataset xyz file.

    Returns:
        numpy.ndarray: Numpy array of named property columns

    """
    tmqm_properties = numpy.genfromtxt(csvfile, delimiter=';',names=True, dtype=None, encoding="utf-8")
    formulas = _read_xyzlist_formulas(xyzfile)
    return append_fields(tmqm_properties, 'formula', data=formulas)

# Available properties columns: CSD_code, Electronic_E, Dispersion_E, Dipole_M, Metal_q, HL_Gap, HOMO_Energy, LUMO_Energy, Polarizability, formula

def read_tmqm_structures(picklefile):
    with open(picklefile, 'rb') as handle:
        structures = pickle.load(handle)
    return structures
