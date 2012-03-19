#!/usr/bin/env python
#-*- coding: utf-8 -*-


import p300
reload(p300)
import numpy as np
import matplotlib.pyplot as plt
from signalParser import signalParser as sp
import scipy.signal as ss
from filtfilt import filtfilt
filename = 'signals/ania1_p300.obci'
channels = ['Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','P3','Pz','P4','T6','O1','O2','FCz']
#channels = ['T3','C3','Cz','C4','T4','T5','P3','Pz','P4','T6', 'FCz','Fz']
#channels = ['O1','Oz','O2','PO8','PO3','PO4','Pz','Cz']
#channels = ['']

fs = 128
dat = p300.p300_train(filename, channels, fs, idx=1, csp_time=[0.0, 0.5])
ntt = dat.data.get_p300_tags(idx=-1, samples=False)
#nt = dat.wyr(time=[0, 0.5], xc_time=0.05)
nt = dat.tags
#dat.show_mean_CSP([0, 0.5], nt)
#mean, left, right = dat.get_mean(nt, m_time=[0, 0.5])
#t_vec = np.linspace(-0, 0.5, len(mean))
#plt.plot(t_vec, -mean, 'r-')
#plt.xlabel('Czas (s)')
#plt.ylabel('Amplituda (uV)')
#plt.show()
#plt.plot([t_vec[left], t_vec[left]], [max(mean), min(mean)], 'g-')
#plt.plot([t_vec[right], t_vec[right]], [max(mean), min(mean)], 'g-')
#plt.show()
#z1, z2 = dat.get_stats([0.1, 0.5], nt, show=True)
#mean[:left] = 0
#mean[right:] = 0
sr = 8
#trgs = np.zeros([sr, len(nt)])
#no_trgs = np.zeros([sr, len(ntt)])
#no_mu = np.zeros(sr)
#no_sigma = np.zeros(sr)
cl, mu, sigma, mean, left, right = dat.prep_classifier(sr, P_vectors=2, reg=1)
cl[0].plot_features()
print '#########ANALYSIS###############'
from artifactClassifier import artifactsClasifier as ac
analyze = p300.p300analysis2(cl, dat.P, 2, mean,mu, sigma, left, right)

b,a = ss.butter(3, 2*1.0/fs, btype = 'high')
b_l, a_l = ss.butter(3, 20.0*2/fs, btype = 'low')
s = sp('signals/ania2_p300.obci')
sig = s.prep_signal(fs, channels)
tags = []
for i in xrange(8):
    t = s.get_p300_tags(idx=i, samples=False)
    tags.extend([(p, i) for p in t])
fp,tn,tp,fn=0,0,0,0
for p,idx in tags:    
    tmp_sig = sig[:, p*fs:p*fs+0.5*fs]
    tmp_sig2 = np.zeros(tmp_sig.shape)
    for i in xrange(len(channels)):
        tmp_sig1 = filtfilt(b,a, tmp_sig[i,:])
        tmp_sig2[i, :] = filtfilt(b_l, a_l, tmp_sig1)
    
    #signal = np.dot(dat.P[:, 0], tmp_sig2)
    #analyze.woody(signal)
    if ac(tmp_sig2, dat.a_features, dat.bands, s.sampling_frequency):
        ix = analyze.analyze(tmp_sig2, idx, tr=.05)
    else:
        ix = -1

    if ix != -1 and idx!=1:
        fp += 1
    if ix == 1 and idx == 1:
        tp += 1
    if ix == -1 and idx != 1:
        tn += 1
    if ix == -1 and idx == 1:
        fn += 1
        
for x in np.arange(-5, 5, 0.5):
    for y in np.arange(-3, 3, 0.5):
        if cl[0].predict(np.array([x,y])) <=0.5:
            plt.plot(x,y,'r+')
        else:
            plt.plot(x,y,'g+')
plt.show()
prec = tp/float(tp+fp)
recall = tp/float(fn + tp)
spec = tn/float(tn + fp)
acc = (tp + tn)/float(tp+tn+fp+fn)
print 'Precision:', tp/float(tp + fp)
print 'Recall:', tp/float(tp + fn)
print 'Specificity:', spec
print 'Accuracy:', acc
print 'F-score:', 2*prec*recall/(prec + recall)