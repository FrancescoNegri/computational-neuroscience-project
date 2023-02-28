import numpy as np
from src.neuron import BaseNeuron

class LIF(BaseNeuron):
    def __init__(self, E_rest = -0.070, V_th = -0.050, V_spike = 0.020, g_leak = 10e-9, E_leak = -0.070, C_m = 100e-12, T_ref = 0.003):
        super().__init__(E_rest, V_th, V_spike, g_leak, E_leak, C_m, T_ref)

    def run(self, I_stim, dt):
        super().run(I_stim, dt)

        for trial_idx in np.arange(np.shape(self.I_stim)[0]):
            # Reset self._t_last_spike
            self._t_last_spike = -self.T_ref

            for i in np.arange(1, np.size(self._t)):
                if self._t[i] - self._t_last_spike > self.T_ref:
                    V_ss = (self.I_stim[trial_idx][i] + self.g_leak * self.E_leak) / self.g_leak

                    self._V_m[trial_idx][i] = V_ss + (self._V_m[trial_idx][i-1] - V_ss) * np.exp(-dt/self.tau_m)
                    self.V_m[trial_idx][i] = self._V_m[trial_idx][i]

                    if self._V_m[trial_idx][i] > self.V_th:
                        # _V_m remains to E_rest (already initialized)
                        self.V_m[trial_idx][i] = self.V_spike
                        self._t_last_spike = self._t[i]
                else:
                    # Already initialized to E_rest
                    pass

        return self.V_m

            