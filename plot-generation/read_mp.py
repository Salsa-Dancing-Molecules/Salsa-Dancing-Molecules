#!/usr/bin/env python3

import json, io, pickle
import numpy
from numpy.lib.recfunctions import append_fields
import ase.io

def read_mp_properties(jsonfile):
    """Reads a jsonfile representing an mp dataset.

    Args:
        jsonfile(str): Filename of the mp dataset json file.

    Returns:
        dict(numpy.ndarray): a dictionary of Numpy arrays for the columns

    """
    with open(jsonfile) as f:
        data = json.load(f)
    columns = []
    keys = {}
    for row in data["response"]:
        for key in row:
            if isinstance(row[key],dict):
                for subkey in row[key]:
                    keys[subkey] = (key, subkey)
            elif isinstance(row[key],list):
                keys[key] = key
            else:
                keys[key] = key

    outdata = {}
    for key in keys:
        column = []
        for row in data["response"]:
            try:
                if isinstance(keys[key],tuple):
                    val = row[keys[key][0]][keys[key][1]]
                else:
                    if isinstance(row[key],list):
                        val = ",".join(row[key])
                    else:
                        val = row[key]
                column.append(val)
            except Exception as e:
                column.append(numpy.nan)
        outdata[key] = numpy.array(column)

    return outdata

def read_mp_structures(picklefile):
    with open(picklefile, 'rb') as handle:
        structures = pickle.load(handle)
    return structures
