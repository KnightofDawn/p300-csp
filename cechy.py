import numpy as np




def cecha_var(signal_target, signal_non_target, ilosc=2):
    var_target = np.zeros((ilosc, signal_target.shape[0]))
    var_non_target = np.zeros((ilosc, signal_non_target.shape[0]))
    for chan in range(ilosc):
        var_target[chan] = np.var(signal_target[:,chan,:], axis=1)
        var_non_target[chan] = np.var(signal_non_target[:,chan,:], axis=1)
    return var_target, var_non_target
