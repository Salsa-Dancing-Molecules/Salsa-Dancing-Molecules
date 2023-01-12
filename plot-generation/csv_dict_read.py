import csv
import matplotlib.pyplot as plt

post_calc_info = []
with open(f'ar_scale_1.0.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        post_calc_info.append(row)


plt.hist([ float(x["cohesive_energy"]) for x in post_calc_info], bins=2)
plt.xlim(xmin=-0.6, xmax = 0.2)


plt.ylabel('Counts')
plt.xlabel('cohesive_energy (eV)');
plt.title('Ar simulations with vol = a*1')

plt.show()