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



channel_list = ['Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','P3','Pz','P4','T6','O1','O2','FCz']
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)
signal = signal - signal[17]/2 - signal[18]/2

signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

b, a = filtr_projekt(rzad = 2, freq = 25, fs = fs)
signal_target = filtruj(b, a, signal_target)
signal_non_target = filtruj(b, a, signal_non_target)


analize_channels = [4,9]
####CSP####
if sys.argv[1] == 'csp':
    P, vals = train_csp(signal_target, signal_non_target)
    signal_target, signal_non_target = apply_csp(signal_target, signal_non_target, P)
    channel_list = range(0,len(channel_list))
    analize_channels = [0,1]
####CSP####

####HJORTH####
if sys.argv[1] == 'hjorth':
    signal_target = hjorth(signal_target)
    signal_non_target = hjorth(signal_non_target)
    analize_channels = [12,14]
####HJORTH####



if int(sys.argv[2]) == 1:
    filename = 'macierz_'+sys.argv[1]+'.png'
    draw.signal_matrix(signal_target, signal_non_target, mean=True, axis=(-250,250), filename=filename, titles=channel_list)

filename='sygnal_'+sys.argv[1]+'.png'
draw.signal_matrix(signal_target, signal_non_target, mean=False, axis=(-400,400), filename=filename, titles=channel_list, chans=analize_channels, rows=2, columns=1, small=True)



signal_target, signal_non_target = losuj(signal_target, signal_non_target, ile=100, po_ile=int(sys.argv[2]))
cechy_target, cechy_non_target = cechy.test_cechy(signal_target, signal_non_target, cechy.max_cor_selective, chans=analize_channels, tre=10, ile=100, poile=int(sys.argv[2]))
mah = mahalanobis(cechy_non_target, cechy_target)

filename = 'cecha_'+sys.argv[1]+'_'+sys.argv[2]+'.png'
draw.cechy(cechy_target/100000,cechy_non_target/100000,filename)
print mah
