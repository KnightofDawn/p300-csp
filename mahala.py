import numpy as np
import pylab as py

mahala = np.loadtxt('mahala.txt')


py.figure(figsize=(11, 8))
py.plot(mahala, 'bo')

py.savefig('mahala.svg', format='svg')



