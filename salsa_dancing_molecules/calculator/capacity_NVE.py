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
    u_to_kg = sum(a.get_masses())*1.6605*10**(-27)
    eV_to_J = 1.602*10**(-19)
    unit_converstion = eV_to_J/u_to_kg
    T2 = a.get_temperature()**2
    k_sqr_ensemble = get_kine_sqr_ensemble(a)
    k_ensemble_sqr = get_kine_ensemble_sqr(a)
    return (unit_converstion*len(a)*units.kB*1.5/(1 - (k_sqr_ensemble
                                                  - k_ensemble_sqr)
                                                  / (1.5*T2*units.kB**2)))
