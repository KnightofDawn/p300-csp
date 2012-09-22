# -*- coding: utf-8 -*-
import numpy as np
import pylab as py
import sys
sys.path.append('libsvm-3.12/python')

from svm import *
from svmutil import *
 
from p300csp import *
import draw
import cechy


channel_list = ['P3','Pz','P4','Fp1','Fp2','F7','F3','Fz','F4','F8','T3','C3','Cz','C4','T4','T5','T6','O1','O2','FCz']

signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)
####signal = signal - signal[17]/2 - signal[18]/2

#print 'Preparing signal'
signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

#print 'Filtering signal'
b, a = filtr_projekt(rzad = 2, freq = 25, fs = fs)
signal_target = filtruj(b, a, signal_target)
signal_non_target = filtruj(b, a, signal_non_target)

#print 'CSP tarin...'
P, vals = train_csp(signal_target, signal_non_target)

#print 'applying csp'
signal_target, signal_non_target = apply_csp(signal_target, signal_non_target, P)



ile = int(sys.argv[2])
po_ile = int(sys.argv[1])
signal_target_u, signal_non_target_u = losuj(signal_target, signal_non_target, ile=ile, po_ile=po_ile)
signal_target_t, signal_non_target_t = losuj(signal_target, signal_non_target, ile=ile, po_ile=po_ile)



cechy_target_u, cechy_non_target_u = cechy.test_cechy(signal_target_u, signal_non_target_u, cechy.max_cor_selective, chans=[0,1])
cechy_target_t, cechy_non_target_t = cechy.test_cechy(signal_target_t, signal_non_target_t, cechy.max_cor_selective, chans=[0,1])








#==================================================================
#                 Program
#==================================================================
 
# wczytywanie danych


 
# kopiujemy dane do zbioru uczącego (pierwsze 75% grupy0 i grupy1)
Xu = (np.concatenate((cechy_target_u, cechy_non_target_u),axis=1).T)/1000000
yu = np.concatenate((np.ones((ile)), np.ones((ile))*-1))
# kopiujemy dane do zbioru testowego (końcowe 25% grupy0 i grupy1)
Xt = (np.concatenate((cechy_target_t, cechy_non_target_t),axis=1).T)/1000000
yt = np.concatenate((np.ones((ile)), np.ones((ile))*-1))

 
# trenujemy model
yul = yu.tolist()
Xul = Xu.tolist()
ytl = yt.tolist()
Xtl = Xt.tolist()

prob  = svm_problem(yul, Xul, isKernel=False)
Ng = 20
zakresC = np.logspace(np.log2(0.1),np.log2(10),20, base=2)
zakresS = np.logspace(np.log2(0.1),np.log2(10),10, base=2)
bestC = 0
bestS = 0
bestTPR =0
TPR=np.zeros((20,10))
for i,C in enumerate(zakresC):
    for j,S in enumerate(zakresS):
        param_string = '-t 2 -q -b 1 -e 0.00001 -c '+str(C)+' -g '+str(S)
        param = svm_parameter(param_string)
        m = svm_train(prob, param)
        p_label, p_acc, p_val = svm_predict(ytl, Xtl, m, '-b 1')
        TPR[i,j] = np.sum(np.array(ytl)==np.array(p_label))/float(len(ytl))
        if TPR[i,j]>bestTPR:
            bestTPR = TPR[i,j]
            bestModel = m
            bestC = C
            bestS = S
        #print C,S,TPR[i,j]
# prezentujemy podział przestrzeni wejść reprezentowany przez model



draw.cechy(cechy_target_t/1000000, cechy_non_target_t/1000000)
draw.rysujPodzial(bestModel, Xt, filename='class-'+sys.argv[1])
