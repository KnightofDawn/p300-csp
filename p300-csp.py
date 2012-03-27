from filtfilt import *
import numpy as np
from sva2py import *
from scipy.stats import mannwhitneyu







def learn_read_signal_and_tags(filename):
	s = sva2py(filename)
	signal = s.signal()
#brakuje tagow

	return signal, target_tags, non_target_tags


def learn_prep_signal(signal, target_tags, non_target_tags, czas_przed=-0.2, czas_po=0.5):
	fs = s.samplingFrequency()
	signal_target = np.zeros((len(target_tags), signal.shape[0], signal.shape[1]))
	signal_non_target = np.zeros((len(non_target_tags), signal.shape[0], signal.shape[1]))

	for tag in range(len(non_target_tags)):
		signals_target[tag,:,:] = (signal[:,:])[non_target_tags[tag]+(czas_przed*fs):non_target_tags[tag]+(czas_po*fs)]
	for tag in range(len(target_tags)):
		signals_non_target[tag,:,:] = (signal[:,:])[target_tags[tag]+(czas_przed*fs):non_target_tags[tag]+(czas_po*fs)]
#jeszcze baseline
	return filtr(signal_target), filtr(signal_non_target)


def filtr_projekt(freq, fs):
	[b,a] = butter(3,freq/(fs/2.0), btype='low')
	return b, a


def filtruj(signal, b, a):
	for tag in range(signal.shape[0]):
		for chan in range(signal.shape[1]):
			signal[tag,chan,:] = filtfilt(signal[tag,chan,:])
	return signal


def kiedy_sie_sygnaly_roznia(signal_target, signal_non_target):
	#w ktorych kanalach?
	
	
	U, pe[i] = mannwhitneyu(sigs[:,i], sigs_trg[:,i])	



	return signal_target, signal_non_target


def train_csp(signal_target, signal_non_target):
        trial_target, chNo, smpl = signal_target.shape
        trial_non_target = signal_non_target.shape[0]
	cov_trg = np.zeros((chNo, chNo))
        cov_non_trg = np.zeros((chNo, chNo))
        for i in range(trial_target):
                A = np.matrix(signal_target[i,:,:])
                cov_trg += A * A.T/ np.trace(A * A.T)
        cov_trg /= trial_target
        for i in range(trial_non_target):
                A = np.matrix(signal_non_target[i,:,:])
                cov_non_trg += A * A.T/ np.trace(A * A.T)
        cov_non_trg /= trial_non_target
	vals, vects = eig(cov_trg, cov_trg + cov_non_trg)
        vals = vals.real
        vals_idx = np.argsort(vals)[::-1]
#POOGLADAC        
	P = np.zeros([len(vals), len(vals)])
        for i in xrange(len(vals)):
            P[:,i] = vects[:,vals_idx[i]] / np.sqrt(vals[vals_idx[i]])
        return P, vals[vals_idx]







