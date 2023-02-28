import numpy as np
import scipy
import warnings

class BaseNeuron:
    def __init__(self, E_rest = -0.070, V_th = -0.050, V_spike = 0.020, g_leak = 10e-9, E_leak = -0.070, C_m = 100e-12, T_ref = 0.003):
        self.V_m = None     # With spikes (for output)
        self._V_m = None    # Without spikes
        self._t = None
        self._t_last_spike = None
        self.I_stim = None
        
        self.E_rest = E_rest
        self.V_th = V_th
        self.V_spike = V_spike
        self.g_leak = g_leak
        self.E_leak = E_leak
        self.C_m = C_m
        self.tau_m = C_m / g_leak
        self.T_ref = T_ref

    def count_spikes(self):
        if self.V_m is not None:
            spikes_count = np.zeros(np.size(self.V_m, axis=0))

            for trial_idx in range(np.size(self.V_m, axis=0)):
                peaks, _ = scipy.signal.find_peaks(self.V_m[trial_idx], height=0)
                spikes_count[trial_idx] = np.size(peaks, axis=0)
        else:
            warnings.warn('The model is initialized, but has not been executed yet.')
            spikes_count = None

        return spikes_count

    def run(self, I_stim, dt):
        self._reset_simulation_params()

        self._t = np.arange(0, np.shape(I_stim)[1] * dt, dt)
        self._t_last_spike = -self.T_ref

        self._V_m = self.E_rest * np.ones([np.shape(I_stim)[0], np.size(self._t)])
        self.V_m = np.copy(self._V_m)

        self.I_stim = I_stim

    def _reset_simulation_params(self):
        self.V_m = None     # With spikes (for output)
        self._V_m = None    # Without spikes
        self._t = None
        self._t_last_spike = None
        self.I_stim = None