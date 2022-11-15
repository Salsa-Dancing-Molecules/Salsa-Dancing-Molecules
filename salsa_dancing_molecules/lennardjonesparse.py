"""Functionfile to parse Lennard-Jones (L-J) parameters for a given element."""


def parse_lj_params(atom_letters):
    """Get L-J parameters for a given element.

    Input is a string with chemical symbol of an element.
    Output is the L-J parameters cutoff, eplsion and sigma.
    The parameters are parsed from LennardJones612_UniversalShifted.params
    and were calculated with the help Lorentz-Berthelot mixing rules by
    Ryan S. Elliot and Andrew Akerson.
    """
    with open('LennardJones612_UniversalShifted.params') as param_file:
        lines = param_file.readlines()[7:]
        for line in lines:
            if 'electron' in line:
                break
            elif atom_letters + ' ' in line:
                params = line.split()
        cutoff = float(params[2])
        epsilon = float(params[3])
        sigma = float(params[4])
    return cutoff, epsilon, sigma
