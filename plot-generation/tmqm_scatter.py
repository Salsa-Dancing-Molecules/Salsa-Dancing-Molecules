#!/usr/bin/env python3

from read_tmqm import read_tmqm_properties
import matplotlib.pyplot as plt

tmqm_properties = read_tmqm_properties('si_nve.csv','tmQM_X.xyz')

print("Available properties:",tmqm_properties.dtype.names)

plt.scatter(tmqm_properties["cohesive_energy"],tmqm_properties["heat_capacity"])
plt.xlim(xmin=3.8, xmax = 5)

plt.title('Si NVE simulations')

plt.ylabel('Heat capacity J/(kgK)')
plt.xlabel('Cohesive Energy (eV)');

plt.show()



