# -*- coding: utf-8 -*-
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#Copyright © 2012 Karol Augustin <karol@augustin.pl>
#License can be found in license


import numpy as np

def test_cechy(signal_target, signal_non_target, func, chans=[0,1], tre=10, ile=100, poile=2):
    cechy_target = np.zeros((len(chans), ile))
    cechy_non_target = np.zeros((len(chans), ile))
    for tag_target in range(ile):
        np.random.shuffle(signal_target)
        np.random.shuffle(signal_non_target)
        signal_t = np.mean(signal_target[0:poile], axis=0)
        signal_nt = np.mean(signal_non_target[0:poile], axis=0)
        cechy_target[:,tag_target] = func(signal_t, signal_target[tre:], signal_non_target, chans)
        cechy_non_target[:,tag_target] = func(signal_nt, signal_target[tre:], signal_non_target, chans)
    return cechy_target, cechy_non_target

def var(signal, signal_target, signal_non_target, chans):
    _var = np.zeros((len(chans)))
    for chan in range(len(chans)):
        _var[chan] = np.var(signal[chans[chan],:])
    return _var

def max_cor(signal, signal_target, signal_non_target, chans):
    _cor = np.zeros((len(chans)))
    for chan in range(len(chans)):
        _cor[chan] = max(np.correlate(signal[chans[chan],:], np.mean(signal_target[:,chans[chan],:], axis=0), 'full'))
    return _cor

def min_cor(signal, signal_target, signal_non_target, chans):
    _cor = np.zeros((len(chans)))
    for chan in range(len(chans)):
        corchan = np.correlate(signal[chans[chan],:], np.mean(signal_target[:,chans[chan],:], axis=0), 'full')
        _cor[chan] = min(corchan[(len(corchan)/2)-10:(len(corchan)/2)+10])
        #_cor[chan] = corchan[len(corchan)/2]
    return _cor

def max_cor_selective(signal, signal_target, signal_non_target, chans):
    _cor = np.zeros((len(chans)))
    for chan in range(len(chans)):
        corchan = np.correlate(signal[chans[chan],:], np.mean(signal_target[:,chans[chan],:], axis=0), 'full')
        #_cor[chan] = max(corchan[(len(corchan)/2)-3:(len(corchan)/2)+3])
        _cor[chan] = corchan[len(corchan)/2]
    return _cor

def max_power(signal, signal_target, signal_non_target, chans):
    _pow = np.zeros((len(chans)))
    for chan in range(len(chans)):
        _pow[chan] = max(signal[chans[chan],:]**2)
    return _pow

#to popraw zeby pasowalo do reszty
def kwroz(signal_matrix, template):
    ret = np.sum((signal_matrix - template[np.newaxis, :, :])**2, axis=2)
    return ret
