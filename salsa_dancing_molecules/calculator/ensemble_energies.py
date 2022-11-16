"""Calculate ensemble energy and ensemble square energy."""
import numpy as np


def get_kinetic_energies(a):
    """Get the kinetic energy."""
    kinetic_energies = []
    momenta = a.arrays.get('momenta')
    if momenta is None:
        return None
    else:
        xyz_kin = 0.5 * np.multiply(momenta, a.get_velocities())
        for k in xyz_kin:
            kinetic_energies.append(np.sqrt(np.dot(k, k)))
        return np.asarray(kinetic_energies)


def get_kine_sqr_ensemble(a):
    """Calculate enesemble average of square of kinetik energy."""
    k = get_kinetic_energies(a)
    if k is None:
        return 0.0
    else:
        return np.dot(k, k) / len(a)


def get_kine_ensemble_sqr(a):
    """Calculate square of enesemble average of kinetik energy."""
    return (a.get_kinetic_energy() / len(a))**2


def get_tot_e_ensemble_sqr(a):
    """Calculate square of enesemble average of total energy."""
    return (a.get_total_energy() / len(a))**2


def get_tot_e_sqr_ensemble(a):
    """Calculate enesemble average of square of total energy."""
    etot = get_kinetic_energies(a) + a.get_potential_energies()
    return etot.dot(etot) / len(a)
