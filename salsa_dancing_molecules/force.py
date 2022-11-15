"""Functionfile for forces."""


def get_force(atoms):
    """Get forces from a ASE atoms object.

    Input is the atoms object and output is a 3x1 vector for each atom in
    "atoms". The vector describes the force action on the atom in
    x-, y- and z-direction.
    """
    return atoms.get_forces()
