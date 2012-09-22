# -*- coding: utf-8 -*-
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#Copyright © 2012 Karol Augustin <karol@augustin.pl>
#License can be found in license

from p300csp import *
import draw
import cechy
import pylab as py
import sys


#channel_list = ('O1', 'O2', 'Fp1', 'Fp2', 'P3')
channel_list = ['P3','Pz','P4','Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','T6','O1','O2','FCz']
#channel_list = ['O1','O2','Oz','Cz','P07','P08']
#print 'Importing signal'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)
signal = signal - signal[17]/2 - signal[18]/2



#print 'Preparing signal'
signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)



#print 'second signal importing and preparing'
#signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania2_p300.obci', channel_list)
#signal_target_2, signal_non_target_2 = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)
'''
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


#print 'Filtering signal'
b, a = filtr_projekt(rzad = 2, freq = 25, fs = fs)
signal_target = filtruj(b, a, signal_target)
signal_non_target = filtruj(b, a, signal_non_target)

#signal_target_2 = filtruj(b,a,signal_target_2)
#signal_non_target_2 = filtruj(b,a,signal_non_target_2)

#print signal_target.shape, signal_non_target.shape


#print 'Mannwhitneyu signal'

#signal_target, signal_non_target = kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=4, thre_chan = 2)


#py.plot(np.mean(signal_target[:,0,:], axis=0),'r.')
#py.plot(np.mean(signal_non_target[:,0,:], axis=0),'b.')
#py.show()




#print 'CSP tarin...'

#P, vals = train_csp(signal_target, signal_non_target)
#signal_target, signal_non_target = apply_csp(signal_target, signal_non_target, P)



signal_target, signal_non_target = losuj(signal_target, signal_non_target, ile=70, po_ile=int(sys.argv[1]))



#print 'drawing nice pictures'
filename = 'macierz_toz_'+sys.argv[1]+'.svg'
#channel_list=False

draw.signal_matrix(signal_target, signal_non_target, mean=True, axis=(-250,250), filename=filename, titles=channel_list)


filename='sygnal_toz_12_'+sys.argv[1]+'.svg'
draw.signal(signal_target, signal_non_target, mean=False, axis=(-350,350), filename=filename, titles=channel_list, chan=12)

#filename='sygnal_csp_1_'+sys.argv[1]+'.svg'
#draw.signal(signal_target, signal_non_target, mean=False, axis=(-15,15), filename=filename, titles=False, chan=1)



#signal_target_fft, signal_non_target_fft = fft_matrix(signal_target, signal_non_target)

#draw.signal_matrix(signal_target, signal_non_target, mean=False)

#template = np.mean(signal_target_fft, axis=0)
#k_target = cechy.kwroz(signal_target_fft, template)
#k_non_target = cechy.kwroz(signal_non_target_fft, template)
#to do rysunkow przenies
#for i in range(k_target.shape[1]):
#    py.subplot(5, 4, i+1)
#    rys = [k_target[:,i], k_non_target[:,i]]
#    py.boxplot(rys)
#py.show()

#cechy_target2, cechy_non_target2 = cechy.test_cechy(signal_target, signal_non_target, cechy.min_cor, chans=[0])
cechy_target, cechy_non_target = cechy.test_cechy(signal_target, signal_non_target, cechy.max_cor_selective, chans=[12])

#cechy_target = np.zeros((3, cechy_target1.shape[1]))
#cechy_non_target = np.zeros((3, cechy_non_target1.shape[1]))

#cechy_target[0:2,:] = cechy_target1
#cechy_non_target[0:2,:] = cechy_non_target1

#cechy_target[2] = cechy_target2
#cechy_non_target[2] = cechy_non_target2



#cechy_target4, cechy_non_target4 = cechy.test_cechy(signal_target_fft, signal_non_target_fft, cechy.var, chans=range(20))
#cechy_target2, cechy_non_target2 = cechy.test_cechy(signal_target, signal_non_target, cechy.var, chans=range(20))
#cechy_target, cechy_non_target = cechy.test_cechy(signal_target, signal_non_target, cechy.max_cor, chans=range(20))

#cechy_target_final = np.zeros((40, cechy_target.shape[1]))
#cechy_non_target_final = np.zeros((40, cechy_non_target.shape[1]))
#cechy_target_final[0:20,:] = cechy_target
#cechy_non_target_final[0:20,:] = cechy_non_target
#cechy_target_final[20:40,:] = cechy_target2
#cechy_non_target_final[20:40,:] = cechy_non_target2

#cechy_target_final[40:60,:] = cechy_target3
#cechy_non_target_final[40:60,:] = cechy_non_target3
#cechy_target_final[60:80,:] = cechy_target4
#cechy_non_target_final[60:80,:] = cechy_non_target4

#cechy_target[1] = cechy_target2[0]
#cechy_non_target[1] = cechy_non_target2[0]
#cechy_target[2] = cechy_target3[0]
#cechy_non_target[2] = cechy_non_target3[0]




print mahalanobis(cechy_non_target, cechy_target)

filename = 'cecha_toz_hist_'+sys.argv[1]+'.svg'
draw.cechy(cechy_target/100000,cechy_non_target/100000,filename)
