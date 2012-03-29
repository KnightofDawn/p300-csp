from p300csp import *

channel_list = ('O1', 'O2', 'Fp1', 'Fp2', 'P3')

print 'Importing signal'
signal, fs, target_tags, non_target_tags = learn_read_signal_and_tags('../eeg-signals/p300-csp/ania1_p300.obci', channel_list)

print 'Preparing signal'
signal_target, signal_non_target = learn_prep_signal(signal, fs, target_tags, non_target_tags, czas_przed=-0.2, czas_po = 0.5)

print 'Filtering signal'
b, a = filtr_projekt(rzad = 2, freq = 15, fs = fs)
signal_target = filtruj(b, a, signal_target)
signal_non_target = filtruj(b, a, signal_non_target)

print 'Mannwhitneyu signal'
signal_target, signal_non_target = kiedy_sie_sygnaly_roznia(signal_target, signal_non_target, thre=1)

print 'CSP tarin...'
P, vals = train_csp(signal_target, signal_non_target)

print 'Done'



###rysunki
py.plot(signal_target)
py.plot(signal_non_target)
py.show()


