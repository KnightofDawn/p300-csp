from p300csp import *
import pylab as py
import sys

#channel_list = ('O1', 'O2', 'Fp1', 'Fp2', 'P3')
channel_list = ['Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','P3','Pz','P4','T6','O1','O2','FCz']

print 'Importing signal'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)

print 'Preparing signal'
signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

#py.plot((signal_target[:,9,:]).transpose())
#print signal_target.shape
#py.plot((signal_non_target[:,9,:]).transpose())
#py.show()

#sys.exit(0)

print 'Filtering signal'
b, a = filtr_projekt(rzad = 2, freq = 20, fs = fs)
signal_target = filtruj(b, a, signal_target)
signal_non_target = filtruj(b, a, signal_non_target)

print 'Mannwhitneyu signal'
signal_target, signal_non_target = kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=3, thre_chan = 2)

#for i in np.linspace(1,3,10):
#    kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=i)
#sys.exit(0)


#py.plot(np.mean(signal_target[:,0,:], axis=0),'r.')
#py.plot(np.mean(signal_non_target[:,0,:], axis=0),'b.')
#py.show()




print 'CSP tarin...'
P, vals = train_csp(signal_target, signal_non_target)
print'p'
print P
print 'vals'
print vals
print 'Done'





print 'applaying csp'
signal_target_csp = np.zeros(signal_target.shape)
signal_non_target_csp = np.zeros(signal_non_target.shape)
for tag in range(signal_target.shape[0]):
    signal_target_csp[tag,:,:] = np.dot(P.transpose(),signal_target[tag,:,:])
for tag in range(signal_non_target.shape[0]):
    signal_non_target_csp[tag,:,:] = np.dot(P.transpose(),signal_non_target[tag,:,:])


print 'drawing nice picture'


for chan in range(signal_target_csp.shape[1]):
    py.subplot(signal_target_csp.shape[1]/5,5,chan+1)
    py.plot((signal_non_target_csp[:,chan,:]).transpose(), 'b')
    py.plot((signal_target_csp[:,chan,:]).transpose(),'r')
    #py.plot(np.var(signal_target_csp[:,chan,:], axis=1),'r.')
    #py.plot(np.var(signal_non_target_csp[:,chan,:], axis=1),'b.')

py.show()



#rysunek 3d
'''

from mpl_toolkits.mplot3d import Axes3D
fig = py.figure()
ax = fig.add_subplot(111, projection='3d')
x_t = np.var(signal_target_csp[:,0,:], axis=1)
y_t = np.var(signal_target_csp[:,1,:], axis=1)
z_t = np.var(signal_target_csp[:,2,:], axis=1)
#z_t = np.array(x_t)*np.array(y_t)

x_nt = np.var(signal_non_target_csp[:,0,:],axis=1)
y_nt = np.var(signal_non_target_csp[:,1,:],axis=1)
z_nt = np.var(signal_non_target_csp[:,2,:],axis=1)
#z_nt = np.array(x_nt)*np.array(y_nt)
#print z_nt

ax.scatter(x_t,y_t,z_t,c='r')
ax.scatter(x_nt,y_nt,z_nt,c='b')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

py.show()

'''
