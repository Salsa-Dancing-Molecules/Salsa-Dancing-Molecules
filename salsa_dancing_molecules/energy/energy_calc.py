"""Functionfile to get total energy, potential energy and kinetic energy from an
atoms object.
"""

def get_energy(atoms):
  return(get_potential_energy(atoms) + get_kinetic_energy(atoms))

def get_potential_energy(atoms):
  return(atoms.get_potential_energy() / len(atoms))

def get_kinetic_energy(atoms):
  return(atoms.get_kinetic_energy() / len(atoms))


if __name__ == "__main__":
    get_energy(atoms)
