"""
Calculates the specific heat capacity for an NVE ensamble.

Takes an atoms object
Returns the capacity as a float

"""

import numpy as np
from ase import units
# when accesable import:
# from temperature import get_temperature()
from .energies_ensamble import (get_kine_sqr_ensemble_average,
                                get_kine_ensemble_average_sqr)


def get_NVE_heat_capacity(a):
    """Calculat Heat Capacity for a NVE ensamble."""
    T2 = a.get_temperature()**2
    k_sqr_ensemble = get_kine_sqr_ensemble_average(a)
    k_ensemble_sqr = get_kine_ensemble_average_sqr(a)
    return (len(a)*units.kB*1.5/(1 - (k_sqr_ensemble
                                      - k_ensemble_sqr)
                                 / (1.5*T2*units.kB**2)))
