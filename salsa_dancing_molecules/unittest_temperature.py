'''
Unittest for temperature.py.
'''

import sys, unittest
from temperature import get_temperature
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution

class TemperatureTest(unittest.TestCase):
	def test_temperature(self):
		atoms = FaceCenteredCubic(directions=[[1,0,0],[0,1,0],[0,0,1]], symbol='Cu', size=(3,3,3),pbc=True)
		MaxwellBoltzmannDistribution(atoms, temperature_K=300)
		
		self.assertequal(get_temperature(atoms), 300)

if __name__ =="__main__":
	tests = [unittest.TestLoader().loadTestsFromTestCase(TemperatureTest)]
	testsuite = unittest.TestSuite(tests)
	results = unittest.TextTestRunner(verbosity=0).run(testsuite)
	sys.exit(not result.wasSuccessful())
		
