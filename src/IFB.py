import numpy as np
from src.neuron import BaseNeuron


class IFB(BaseNeuron):
    def __init__(self, S=0.03e-2, E_reset=-0.060, V_th=-0.050, V_spike=0.020, g_leak=0.035e-3, E_leak=-0.075, C_m=2e-6, T_ref=0, V_h=-0.070, g_T=0.08e-3, E_T=-0.120, tau_h_plus=100e-3, tau_h_minus=20e-3):
        super().__init__(E_reset, V_th, V_spike, (g_leak * S), E_leak, (C_m * S), T_ref)

        self.V_h = V_h
        self.g_T = g_T * S
        self.E_T = E_T
        self.tau_h_plus = tau_h_plus
        self.tau_h_minus = tau_h_minus

    def run(self, I_stim, dt, V_0 = None):
        super().run(I_stim, dt, V_0)

        # Parameter h(0) = 1 since 1 - h is the fraction of inactivated channels
        self.h = np.ones(np.shape(self.I_stim))

        for trial_idx in np.arange(np.shape(self.I_stim)[0]):
            # Reset self._t_last_spike
            self._t_last_spike = -self.T_ref

            for i in np.arange(1, np.size(self._t)):
                if self._t[i] - self._t_last_spike > self.T_ref:                
                    h_inf = np.heaviside(self.V_h - self._V_m[trial_idx][i-1], 0.5)
                    tau_h = self.tau_h_minus * np.heaviside(self._V_m[trial_idx][i-1] - self.V_h, 0.5) + self.tau_h_plus * np.heaviside(self.V_h - self._V_m[trial_idx][i-1], 0.5)
                    self.h[trial_idx][i] = self.h[trial_idx][i-1] + dt * (h_inf - self.h[trial_idx][i-1]) / tau_h

                    I_leak = self.g_leak * (self._V_m[trial_idx][i-1] - self.E_leak)
                    I_T = self.g_T * self.h[trial_idx][i] * (self._V_m[trial_idx][i-1] - self.E_T) * np.heaviside(self._V_m[trial_idx][i-1] - self.V_h, 0.5)
                    I_tot = self.I_stim[trial_idx][i] - I_leak - I_T

                    self._V_m[trial_idx][i] = self._V_m[trial_idx][i-1] + dt * I_tot / self.C_m

                    self.V_m[trial_idx][i] = self._V_m[trial_idx][i]

                    if self._V_m[trial_idx][i] > self.V_th:
                        self._V_m[trial_idx][i] = self.E_reset
                        self.V_m[trial_idx][i] = self.V_spike
                        self._t_last_spike = self._t[i]
                else:
                    # Already initialized to E_reset
                    pass
        
        return self.V_m
