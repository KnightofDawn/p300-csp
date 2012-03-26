def learn_read_signal_and_tags(filename):
	wywalic niepotrzebne kanaly
	return signal, target_tags, non_target_tags


def learn_prep_signal(signal, target_tags, non_target_tags, czas_przed=-0.2, czas_po=0.5):
	#time matrix, 		
	#baseline = mean(czas przed do 0)
	#od zera do czas po odejmuje baseline
	return #macierz sygnalow target i non target [no_tag, chan, smpl]

def filtr(signal_macierz, b, a):
	return macierz po filtrze
#rozpakowac, przefiltrowac, zapakowac, zreturnowac


def kiedy_sie_sygnaly_roznia(signal_target, signal_non_target):
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







