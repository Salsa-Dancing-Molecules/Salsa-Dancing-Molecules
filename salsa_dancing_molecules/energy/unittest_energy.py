'''
Unittest for energy_calc.py.
'''

import sys, unittest
from energy_calc import get_energy
from energy_calc import get_potential_energy
from energy_calc import get_kinetic_energy
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.calculators.emt import EMT

class TestEnergy(unittest.TestCase):
	def test_energy(self):
		atoms = FaceCenteredCubic(directions=[[1,0,0],[0,1,0],[0,0,1]], symbol='Cu', size=(3,3,3),pbc=True)
		MaxwellBoltzmannDistribution(atoms, temperature_K=300)
		
		atoms.calc = EMT()
		
		if get_energy(atoms) == get_kinetic_energy(atoms) + get_potential_energy(atoms):
			self.assertTrue(True)
		else:
			self.assertTrue(False)

if __name__ =="__main__":
	tests = [unittest.TestLoader().loadTestsFromTestCase(TestEnergy)]
	testsuite = unittest.TestSuite(tests)
	result = unittest.TextTestRunner(verbosity=0).run(testsuite)
	sys.exit(not result.wasSuccessful())
