#!/usr/bin/env python
#-*- coding: utf-8 -*-

import p300
from signalParser import signalParser as sp
import numpy as np
import scipy.signal as ss

filename = 'ania2_p300.obci'
channels = ['O1','O2','Cz','Pz','T5','T6','FCz','Fz']
fs = 128
###POCZĄTEK KALIBRACJI##############
data = p300.p300_train(filename, channels, fs, idx=1)#idx oznacza indeks na który
                                                    #należało patrzeć podczas kalibracji
new_tags = data.wyr()
not_idx_tags = data.data.get_p300_tags(idx=-1, samples=False)#Tutaj idx musi być -idx z linijki 13
                                                            #Tagi pozostałych przypadków
mean, left, right = data.get_mean(new_tags, m_time=[0, 0.5])
mean[:left] = 0
mean[right:] = 0
sr = 5 #Maksymalna liczba odcinków do uśrednienia; gdzieś do parametryzacji
targets = np.zeros([sr, len(new_tags)])
non_targets = np.zeros([sr, len(not_idx_tags)])
mu = np.zeros(sr)
sigma = np.zeros(sr)
for i in xrange(1, sr + 1):
    targets[i - 1, :], non_targets[i - 1, :],\
    mu[i - 1], sigma[i - 1] = data.get_n_mean(i, new_tags, [0.0, 0.5], 0.05)
####################KONIEC KALIBRACJI

#######ON-LINE############
#Zakładamy, że signal to nieprzefiltrowany, niezmontowany sygnał o długości takiej
#jak mean (tutaj 0.5 sekundy) i o kanałach takich jak w channels (o takiej samej kolejności)
#Zakładamy, że również mamy indeks pola, które się właśnie zaświeciło - zmienna idx

#0 Konstruktor klasy analizującej; wystarczy raz
analyze = p300.p300analysis(targets, non_targets, mean, mu, sigma, left, right)

#1 najpierw trzeba go przefiltrować
#Te filtry powinny być policzone gdzieś tylko raz
b, a = ss.butter(3, 2*1.0/fs, btype='high')
b_l, a_l = ss.butter(3, 2*20.0/fs, btype='low')

#Wszystko dalej powinno się robić dla każdego nowego sygnału
tmp_sig = np.zeros(signal.shape)
for e in xrange(len(channels)):
    tmp = filtfilt(b,a, signal[e, :])
    tmp_sig[e, :] = filtfilt(b_l, a_l, tmp)

#2 Montujemy CSP
sig = np.dot(data.P[:, 0], tmp_sig)

#3 Klasyfikacja: indeks pola albo 0, gdy nie ma detekcji
ix = analyze.analyze(sig, idx, tr=0.05)