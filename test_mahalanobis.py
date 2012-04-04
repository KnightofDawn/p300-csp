import numpy as np
import p300csp





mu1 = [0, 0]
Sigma1 = np.array([[1,0],[0,1]])


z1 = np.random.multivariate_normal(mu1, Sigma1, 1000)



mu2 = [0,10]
Sigma2 = np.array([[2,0],[0,2]])

z2 = np.random.multivariate_normal(mu2, Sigma2, 1000)



print p300csp.mahalanobis(z1.T,z2.T)
