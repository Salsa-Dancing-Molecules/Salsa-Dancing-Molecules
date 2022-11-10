"""
Calculates the specific heat capacity for an NVE ensamble.

Takes an atoms object
Returns the capacity as a float

"""

import numpy as np
from ase import units
from .ensemble_energies import (get_kine_sqr_ensemble,
                                get_kine_ensemble_sqr)


def get_NVE_heat_capacity(a):
    """Calculat Heat Capacity for a NVE ensamble."""
    T2 = a.get_temperature()**2
    k_sqr_ensemble = get_kine_sqr_ensemble(a)
    k_ensemble_sqr = get_kine_ensemble_sqr(a)
    return (len(a)*units.kB*1.5/(1 - (k_sqr_ensemble
                                      - k_ensemble_sqr)
                                 / (1.5*T2*units.kB**2)))
