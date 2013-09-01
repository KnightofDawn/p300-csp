import draw
import numpy as np

csp = np.loadtxt('mah_csp')
toz = np.loadtxt('mah_toz')
hjo = np.loadtxt('mah_hjorth')
print csp, toz, hjo


filename = 'mahalanobis.png'
draw.mahalanobis(toz, hjo, csp, filename)
