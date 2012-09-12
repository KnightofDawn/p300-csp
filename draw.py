# -*- coding: utf-8 -*-
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#Copyright © 2012 Karol Augustin <karol@augustin.pl>
#License can be found in license

import pylab as py
import numpy as np

def cechy(cecha_target, cecha_non_target, filename):
    py.figure(figsize=(11, 8))
    if cecha_target.shape[0] == 2 and cecha_non_target.shape[0] == 2:
        py.plot(cecha_non_target[0], cecha_non_target[1], 'bo')
        py.plot(cecha_target[0], cecha_target[1], 'ro')

    elif cecha_target.shape[0] == 1 and cecha_non_target.shape[0] == 1:
        py.hist(cecha_target[0], normed=False, label='Non Targets')
        py.hist(cecha_non_target[0], normed=False, alpha=.5, label='Targets')    
        #py.xlabel('Max-corr')
        #py.ylabel('P')
        py.legend()
    py.savefig(filename, format='svg')




def signal_matrix(signal_target, signal_non_target, rows=4, columns=5, type='plain', mean=False, axis=False, filename=False, titles=False):
    py.figure(figsize=(21, 14))
    for chan in range(signal_target.shape[1]):
        py.subplot(rows,columns,chan+1)
    
        if type == 'plain':
            non_target_plot = (signal_non_target[:,chan,:]).transpose()
            target_plot = (signal_target[:,chan,:]).transpose()
        elif type == 'var':
            target_plot = np.var(signal_target[:,chan,:], axis=1)
            non_target_plot = np.var(signal_non_target[:,chan,:], axis=1)
        if mean:
            target_plot = np.mean(target_plot, axis=1)
            non_target_plot = np.mean(non_target_plot, axis=1)

        xs = np.linspace(-0.2,0.5,len(non_target_plot))
        if titles:
            py.title(titles[chan])
        py.plot(xs,non_target_plot, 'b')
        py.plot(xs,target_plot,'r', alpha=.5)
#        if not mean:
#            py.plot(xs,np.mean(non_target_plot, axis=1),'c')
#            py.plot(xs,np.mean(target_plot,axis=1),'y')

        if axis is not False:
            py.ylim(axis)
        py.xlim((min(xs),max(xs)))
        py.savefig(filename, format='svg')
    

def signal(signal_target, signal_non_target, chan, mean=False, type='plain', axis=False, filename=False, titles=False):
    py.figure(figsize=(21, 14))

    if type == 'plain':
        non_target_plot = (signal_non_target[:,chan,:]).transpose()
        target_plot = (signal_target[:,chan,:]).transpose()
    elif type == 'var':
        target_plot = np.var(signal_target[:,chan,:], axis=1)
        non_target_plot = np.var(signal_non_target[:,chan,:], axis=1)
    if mean:
        target_plot = np.mean(target_plot, axis=1)
        non_target_plot = np.mean(non_target_plot, axis=1)

    xs = np.linspace(-0.2,0.5,len(non_target_plot))
    if titles:
        py.title(titles[chan])
    py.plot(xs,non_target_plot, 'b')
    py.plot(xs,target_plot,'r',alpha=.5)
#        if not mean:
#            py.plot(xs,np.mean(non_target_plot, axis=1),'c')
#            py.plot(xs,np.mean(target_plot,axis=1),'y')

    if axis is not False:
        py.ylim(axis)
    py.xlim((min(xs),max(xs)))
    py.savefig(filename, format='svg')
