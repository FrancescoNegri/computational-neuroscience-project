# Computational Neuroscience Project ~ A.Y. 2022-2023
### Giuseppe Leo, Francesco Negri
___
## Summary
This project consists in the implementation and comparison of two abstract neuronal models, by deriving their sub- and supra-threshold
behaviour and computing their gain functions.

### Leaky Integrate-and-Fire (LIF)
The LIF model is inspired by the famous integrate-and-fire (IF) reduced neuronal model, but it adds a leakage channel. This model is
able to display only tonic spiking activity.

$$C_{m}\frac{dV_{m}}{dt}=-I_{leak}+I_{stim}$$

where $I_{leak}=g_{leak}\bigl(V_{m}-E_{leak}\bigr)$ is the leakage current and $I_{stim}$ is the stimulation current, which might be
substituted by the synaptic current $I_{syn}$ as well.

### Integrate-and-Fire-or-Burst (IFB)
The IFB model, on the other hand, extends the LIF one and enables the simulation of bursting activity patterns as well, by taking into
account T-type low voltage activated $\text{Ca}^{2+}$ channels.

$$C_{m}\frac{dV_{m}}{dt}=-I_{leak}-I_{T}+I_{stim}$$

$$\tau_{h}\frac{dh}{dt}=-h+h_{\infty}$$

where $I_{leak}=g_{leak}\bigl(V_{m}-E_{leak}\bigr)$ is the leakage current, $I_{T}=g_{T}h\bigl(V_{m}-E_{T}\bigr)\Theta\bigl(V_{m}-V_{h}\bigr)$
and $I_{stim}$ is the stimulation current, which might be substituted by the synaptic current $I_{syn}$ as well.
Moreover, $h_{\infty}=\Theta\bigl(V_{h}-V_{m}\bigr)$ and $\tau_{h}=\tau_{h}^{-}\Theta\bigl(V_{m}-V_{h}\bigr)+\tau_{h}^{+}\Theta\bigl(V_{h}-V_{m}\bigr)$.
Finally, $\Theta\bigl({\cdot}\bigr)$ is the Heaviside step function.
