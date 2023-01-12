#!/usr/bin/env python3
import io, pickle
import numpy, ase.io
from numpy.lib.recfunctions import append_fields

def read_xyzlist(xyzfile):

    def xyz_lines_to_atoms(lines):
        s = "".join(lines)
        sf = io.StringIO(s)
        return ase.io.read(sf, format="xyz")

    f = open(xyzfile, "r")
    all_structures = []
    lines = []
    for line in f:
        if line == "\n":
            all_structures.append(xyz_lines_to_atoms(lines))
            print(len(all_structures))
            lines = []
        else:
            lines.append(line)
    if len(lines)>0:
        all_structures.append(xyz_lines_to_atoms(lines))
    f.close()
    return all_structures

structs = read_xyzlist('tmQM_X.xyz')
with open('tmqm_structures.pickle', 'wb') as f:
    pickle.dump(structs, f, protocol=pickle.HIGHEST_PROTOCOL)

