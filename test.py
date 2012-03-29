from p300csp import *
from draw import *
from cechy import *
import pylab as py
import sys


#channel_list = ('O1', 'O2', 'Fp1', 'Fp2', 'P3')
channel_list = ['Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','P3','Pz','P4','T6','O1','O2','FCz']

print 'Importing signal'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)


print 'Preparing signal'
signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)


print 'second signal importing and preparing'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania2_p300.obci', channel_list)
signal_target2, signal_non_target2 = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

print 'joining signals'
signal_target = np.concatenate((signal_target, signal_target2), axis=0)
signal_non_target = np.concatenate((signal_non_target, signal_non_target2), axis=0)
print signal_target.shape, signal_non_target.shape




'''
py.plot((signal_target[:,9,:]).transpose())
print signal_target.shape
py.plot((signal_non_target[:,9,:]).transpose())
py.show()
sys.exit(0)
'''


print 'Filtering signal'
b, a = filtr_projekt(rzad = 2, freq = 25, fs = fs)
signal_target = filtruj(b, a, signal_target)
signal_non_target = filtruj(b, a, signal_non_target)

print 'Mannwhitneyu signal'
signal_target, signal_non_target = kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=4, thre_chan = 2)

'''
py.plot(np.mean(signal_target[:,0,:], axis=0),'r.')
py.plot(np.mean(signal_non_target[:,0,:], axis=0),'b.')
py.show()
'''



print 'CSP tarin...'
P, vals = train_csp(signal_target, signal_non_target)

#print 'vals'
#print vals
#print 'Done'

print 'applying csp'
signal_target, signal_non_target = apply_csp(signal_target, signal_non_target, P)



print 'drawing nice pictures'
#draw_signal_matrix(signal_target, signal_non_target)

var_target, var_non_target = cecha_var(signal_target, signal_non_target, ilosc=3)
draw_cechy_3d(var_target,var_non_target)



