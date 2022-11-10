"""
Calculates the specific heat capacity for an NVT ensamble.

Takes an atoms object
Returns the capacity as a float

"""

import numpy as np
from ase import units
from .ensemble_energies import (get_tot_e_ensemble_sqr,
                                get_tot_e_sqr_ensemble)


def get_NVT_heat_capacity(a):
    """Calculat Heat Capacity for a NVT ensamble."""
    e_sqr_ensemble = get_tot_e_sqr_ensemble(a)
    e_ensemble_sqr = get_tot_e_ensemble_sqr(a)
    return ((e_sqr_ensemble - e_ensemble_sqr)
            / (units.kB*a.get_temperature()**2))
