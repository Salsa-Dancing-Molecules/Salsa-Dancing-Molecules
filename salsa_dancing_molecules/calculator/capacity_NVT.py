"""
Calculates the specific heat capacity for an NVT ensamble.

Takes an atoms object
Returns the capacity as a float

"""

import numpy as np
from ase import units
# from temperature import get_temperature()
from .energies_ensamble import (get_tot_e_ensemble_average_sqr,
                                get_tot_e_sqr_ensemble_average)


def get_NVT_heat_capacity(a):
    """Calculat Heat Capacity for a NVT ensamble."""
    e_sqr_ensemble = get_tot_e_sqr_ensemble_average(a)
    e_ensemble_sqr = get_tot_e_ensemble_average_sqr(a)
    return ((e_sqr_ensemble - e_ensemble_sqr)
            / (units.kB*a.get_temperature()**2))
