from p300csp import *
import draw
import cechy
import pylab as py
import sys


#channel_list = ('O1', 'O2', 'Fp1', 'Fp2', 'P3')
channel_list = ['P3','Pz','P4','Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','T6','O1','O2','FCz']
#channel_list = ['O1','O2','Oz','Cz','P07','P08']
print 'Importing signal'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)


print 'Preparing signal'
signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

'''
print 'second signal importing and preparing'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania2_p300.obci', channel_list)
signal_target2, signal_non_target2 = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

print 'joining signals'
signal_target = np.concatenate((signal_target, signal_target2), axis=0)
signal_non_target = np.concatenate((signal_non_target, signal_non_target2), axis=0)
print signal_target.shape, signal_non_target.shape

'''


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

#print signal_target.shape, signal_non_target.shape


print 'Mannwhitneyu signal'

signal_target, signal_non_target = kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=4, thre_chan = 2)


#py.plot(np.mean(signal_target[:,0,:], axis=0),'r.')
#py.plot(np.mean(signal_non_target[:,0,:], axis=0),'b.')
#py.show()




print 'CSP tarin...'
P, vals = train_csp(signal_target, signal_non_target)

#print 'vals'
#print vals
#print 'Done'

print 'applying csp'
signal_target, signal_non_target = apply_csp(signal_target, signal_non_target, P)



signal_target, signal_non_target = losuj(signal_target, signal_non_target, ile=1000, po_ile=2)



print 'drawing nice pictures'

#draw.signal_matrix(signal_target, signal_non_target, mean=True)
signal_target_fft, signal_non_target_fft = fft_matrix(signal_target, signal_non_target)
#draw.signal_matrix(signal_target_fft, signal_non_target_fft, mean=True)



cechy_target3, cechy_non_target3 = cechy.test_cechy(signal_target_fft, signal_non_target_fft, cechy.max_cor, chans=range(20))
cechy_target4, cechy_non_target4 = cechy.test_cechy(signal_target_fft, signal_non_target_fft, cechy.var, chans=range(20))
cechy_target2, cechy_non_target2 = cechy.test_cechy(signal_target, signal_non_target, cechy.var, chans=range(20))
cechy_target, cechy_non_target = cechy.test_cechy(signal_target, signal_non_target, cechy.max_cor, chans=range(20))



cechy_target_final = np.zeros((80, cechy_target.shape[1]))
cechy_non_target_final = np.zeros((80, cechy_non_target.shape[1]))
cechy_target_final[0:20,:] = cechy_target
cechy_non_target_final[0:20,:] = cechy_non_target
cechy_target_final[20:40,:] = cechy_target2
cechy_non_target_final[20:40,:] = cechy_non_target2
cechy_target_final[40:60,:] = cechy_target3
cechy_non_target_final[40:60,:] = cechy_non_target3
cechy_target_final[60:80,:] = cechy_target4
cechy_non_target_final[60:80,:] = cechy_non_target4

#cechy_target[1] = cechy_target2[0]
#cechy_non_target[1] = cechy_non_target2[0]
#cechy_target[2] = cechy_target3[0]
#cechy_non_target[2] = cechy_non_target3[0]


print mahalanobis(cechy_non_target_final, cechy_target_final)

draw.cechy(cechy_target,cechy_non_target)



