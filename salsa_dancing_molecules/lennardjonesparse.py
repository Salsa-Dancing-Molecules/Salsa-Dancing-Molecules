"""Functionfile to parse Lennard-Jones (L-J) parameters for a given element."""
from .third_party import lj_params


def parse_lj_params(atom_letters):
    """Get L-J parameters for a given element.

    Input is a string with chemical symbol of an element.
    Output is the L-J parameters cutoff, eplsion and sigma.
    The parameters are parsed from LennardJones612_UniversalShifted.params
    and are ordered after atomic number. The parameters were calculated with
    the help Lorentz-Berthelot mixing rules by Ryan S. Elliot and
    Andrew Akerson.
    """
    return lj_params[atom_letters]
