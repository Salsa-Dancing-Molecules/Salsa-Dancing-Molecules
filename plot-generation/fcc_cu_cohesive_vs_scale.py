import csv
import matplotlib.pyplot as plt
import math

post_calc_info = []
with open(f'fcc_cu_data/post_process_trimmed.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        post_calc_info.append(row)


plt.scatter([ float(x["volume"]) for x in post_calc_info], [round(float(x["cohesive_energy"]), 2) for x in post_calc_info], label='FCC Cu')

plt.ylabel('cohesive energy (eV)')
plt.xlabel('volume scale');
plt.title('Cohesive energy vs volume scale')
plt.legend()

plt.show()
