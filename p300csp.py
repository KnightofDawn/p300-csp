import numpy as np



def learn_read_signal_and_tags(filename, channel_list):
	from sva2py import sva2py
	s = sva2py(filename)
	signal = np.zeros((len(channel_list), np.shape(s.channel(1,type='int'))[0]))
	for channel in range(len(channel_list)):
		ch = s.channel(channel_list[channel])
		signal[channel] = ch
	
	fs = s.samplingFrequency()
	signal = signal - np.mean(signal, axis = 0)
	target_tags = s.get_p300_tags(idx = 1, rest = False)
	non_target_tags = s.get_p300_tags(idx = 1, rest = True)
	return signal, fs, target_tags, non_target_tags

def learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po=0.5):
	signal_target = np.zeros((len(target_tags), signal.shape[0], (czas_po-czas_przed)*fs))
	signal_non_target = np.zeros((len(non_target_tags), signal.shape[0], (czas_po-czas_przed)*fs))

	for tag in range(len(target_tags)):
		signal_target[tag,:,:] = signal[:,int(target_tags[tag])+int(czas_przed*fs):int(target_tags[tag])+int(czas_po*fs)]
	for tag in range(len(non_target_tags)):
		signal_non_target[tag,:,:] = signal[:,int(non_target_tags[tag])+int(czas_przed*fs):int(non_target_tags[tag])+int(czas_po*fs)]
	
	baseline_target = signal_target[:,:,0:-1*czas_przed*fs]
	baseline_non_target = signal_non_target[:,:,0:-1*czas_przed*fs]
	baseline_target = np.mean(baseline_target, axis=2)
	baseline_non_target = np.mean(baseline_non_target, axis=2)

	signal_target = signal_target - baseline_target[:,:,np.newaxis]
	signal_non_target = signal_non_target - baseline_non_target[:,:,np.newaxis]
	return signal_target, signal_non_target

def filtr_projekt(rzad, freq, fs):
	from scipy.signal import butter
	[b,a] = butter(rzad,freq/(fs/2.0), btype='low')
	return b, a

def filtruj(b, a, signal):
	from filtfilt import filtfilt
	for tag in range(signal.shape[0]):
		for chan in range(signal.shape[1]):
			signal[tag,chan,:] = filtfilt(b, a, signal[tag,chan,:])
	return signal

def kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=1, thre_chan = 1):
	from scipy.stats import mannwhitneyu
	p = np.zeros(signal_target.shape[1:3])
	p0 = np.zeros(signal_target.shape[1:3])
	for chan in range(signal_target.shape[1]):
		for sample in range(signal_target.shape[2]):
			U, p[chan, sample] = mannwhitneyu(signal_target[:,chan,sample], signal_non_target[:,chan,sample])
		
	p0[np.where(p[:,:]*100 < thre)] = 1
	p = np.sum(p0, axis=0)
	#print p
	p_wieksze, = np.where(p>=thre_chan)
	#print p_wieksze
	signal_target_cut = np.zeros((signal_target.shape[0], signal_target.shape[1], p_wieksze.shape[0]))
	signal_non_target_cut = np.zeros((signal_non_target.shape[0], signal_non_target.shape[1], p_wieksze.shape[0]))
	count = 0
	for sample in p_wieksze:
		signal_target_cut[:,:,count] = signal_target[:,:,sample]
		signal_non_target_cut[:,:,count] = signal_non_target[:,:,sample]
		count += 1
	return signal_target_cut, signal_non_target_cut

def train_csp(signal_target, signal_non_target):
	from scipy.linalg import eig
        trial_target, chNo, smpl = signal_target.shape
        trial_non_target = signal_non_target.shape[0]
	cov_trg = np.zeros((chNo, chNo))
        cov_non_trg = np.zeros((chNo, chNo))
        for trial in range(trial_target):
                A = np.matrix(signal_target[trial,:,:])
                cov_trg += A * A.T/ np.trace(A * A.T)
        cov_trg /= trial_target
        for trial in range(trial_non_target):
                A = np.matrix(signal_non_target[trial,:,:])
                cov_non_trg += A * A.T/ np.trace(A * A.T)
        cov_non_trg /= trial_non_target
	vals, vects = eig(cov_trg, cov_trg + cov_non_trg)
        vals = vals.real
        vals_idx = np.argsort(vals)[::-1]    
	P = np.zeros([len(vals), len(vals)])
        for i in xrange(len(vals)):
            P[:,i] = vects[:,vals_idx[i]] / np.sqrt(vals[vals_idx[i]])
        return P, vals[vals_idx]

def apply_csp(signal_target, signal_non_target, P):
	signal_target_csp = np.zeros(signal_target.shape)
	signal_non_target_csp = np.zeros(signal_non_target.shape)
	for tag in range(signal_target.shape[0]):
		signal_target_csp[tag,:,:] = np.dot(P.transpose(),signal_target[tag,:,:])
	for tag in range(signal_non_target.shape[0]):
		signal_non_target_csp[tag,:,:] = np.dot(P.transpose(),signal_non_target[tag,:,:])
	return signal_target_csp, signal_non_target_csp

def losuj(signal_target, signal_non_target, ile=100, po_ile=2):
	signal_target_rand = np.zeros((ile, signal_target.shape[1], signal_target.shape[2]))
	signal_non_target_rand = np.zeros((ile, signal_non_target.shape[1], signal_non_target.shape[2]))

	for i in range(ile):
		np.random.shuffle(signal_target)
		np.random.shuffle(signal_non_target)
		signal_target_rand[i] = np.mean(signal_target[0:po_ile+1], axis=0)
		signal_non_target_rand[i] = np.mean(signal_non_target[0:po_ile+1], axis=0)
	return signal_target_rand, signal_non_target_rand

def mahalanobis(x,y):
	import scipy.spatial.distance as ssd
	cov = np.cov(x,y)
	print cov.shape
	cov = np.linalg.inv(cov)
	print cov.shape
	ret = ssd.mahalanobis(x,y,cov)
	return ret

