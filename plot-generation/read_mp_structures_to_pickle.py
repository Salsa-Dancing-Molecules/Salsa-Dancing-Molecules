#!/usr/bin/env python3

import json, io, pickle
import numpy
from numpy.lib.recfunctions import append_fields
import ase.io

def read_mp_structures_to_pickle(jsonfile, picklefile):
    with open(jsonfile, 'r') as f:
        data = json.load(f)
    structs = []
    N = len(data["response"])
    n = 0
    for row in data["response"]:
        sf = io.StringIO(row["cif"])
        structs.append(ase.io.read(sf, format="cif"))
        n+=1
        print(n,"of",N)
    with open(picklefile, 'wb') as f:
        pickle.dump(structs, f, protocol=pickle.HIGHEST_PROTOCOL)

read_mp_structures_to_pickle('mp_data.json','mp_structures.pickle')
