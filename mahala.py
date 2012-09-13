import numpy as np
import pylab as py
import sys

mahala = np.loadtxt(sys.argv[1])


py.figure(figsize=(11, 8))
py.plot(mahala, 'bo')

py.savefig('mahala.svg', format='svg')



