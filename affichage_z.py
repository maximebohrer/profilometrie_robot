import os
import matplotlib.pyplot as plt

FILE_NAME = "nuage.txt"
SCRIPT_DIR = os.path.dirname(__file__)

f = open(FILE_NAME, 'r')

k = 0
abs = []
les_z = []
for line in f:
    if k % 100 == 0:
        x, y, z = line.strip().split('\t')
        les_z.append(float(z))
        abs.append(k)
    k += 1

plt.plot(abs, les_z)
plt.show()
f.close()