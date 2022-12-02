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
    u_to_kg = sum(a.get_masses())*1.6605*10**(-27)
    eV_to_J = 1.602*10**(-19)
    unit_converstion = eV_to_J/u_to_kg
    e_sqr_ensemble = get_tot_e_sqr_ensemble(a)
    e_ensemble_sqr = get_tot_e_ensemble_sqr(a)
    return (unit_converstion*(e_sqr_ensemble - e_ensemble_sqr)
            / (units.kB*a.get_temperature()**2))
