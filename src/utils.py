import matplotlib.pyplot as plt
import numpy as np

# Generate step current stimulus and time vector from the amplitude(s)
def generate_stimulus(I_amplitudes, simulation_time, t_on=None, t_off=None, dt=1e-4, is_noisy = False):
    if t_on is None:
        t_on = 0
    
    if t_off is None:
        t_off = simulation_time
    
    if not hasattr(I_amplitudes, '__iter__'):
        I_amplitudes = np.array([I_amplitudes])
    
    t = np.arange(0, simulation_time, dt)
    I_stim = np.zeros([np.size(I_amplitudes, axis=0), np.size(t)])

    for trial_idx, I_amplitude in enumerate(I_amplitudes):
        if hasattr(I_amplitude, '__iter__') and np.size(I_amplitude, axis=0) == 2:
            min_I = I_amplitude[0]
            max_I = I_amplitude[1]
        else:
            min_I = 0
            max_I = I_amplitude

        if is_noisy:
            min_noise_1 = np.random.normal(0, max_I/100, round(t_on / dt)) if min_I != 0 else 0
            min_noise_2 = np.random.normal(0, max_I/100, np.size(t) - round(t_off / dt)) if min_I != 0 else 0
            max_noise = np.random.normal(0, max_I/100, round(t_off / dt) - round(t_on / dt))
        else:
            min_noise_1 = 0
            min_noise_2 = 0
            max_noise = 0
        
        I_stim[trial_idx][0:round(t_on / dt)] = min_I + min_noise_1
        I_stim[trial_idx][round(t_on / dt):round(t_off / dt)] = max_I + max_noise
        I_stim[trial_idx][round(t_off / dt):] = min_I + min_noise_2

    return I_stim, t

# Plot the gain function
def plot_gain_function(I_amplitudes, firing_rate, title='Gain Function', subtitle=None, xticks=None):
    plt.figure()
    plt.plot(I_amplitudes * 1e12, firing_rate, marker='x', linestyle=':')
    plt.xlabel('$I_{stim}\;(pA)$')
    plt.ylabel('$\\nu\;(Hz)$')
    if xticks is not None:
        plt.xticks(xticks)
    if subtitle is None:
        plt.title(title)
    else:
        plt.title(title + '\n' + subtitle)
    
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Plot V_m and I_stim vs. time for several applied current values
def plot_trials(t, V_m, I_stim, title='Results', subtitle=None, fig_width=2, fig_height=4):
    fig = plt.figure(figsize=(fig_width * np.shape(V_m)[0], fig_height), dpi=150)
    axs = fig.subplots(2, np.size(I_stim, axis=0), sharex='col', sharey='row')

    if np.size(I_stim, axis=0) == 1:
        axs[0].plot(t, V_m[0] * 1e3)
        axs[1].plot(t, I_stim[0] * 1e12)

        axs[0].set_ylabel('$V_{m}\;(mV)$')
        axs[1].set_ylabel('$I_{stim}\;(pA)$')   
        axs[1].set_xlabel('$t\;(s)$')

        axs[0].spines['top'].set_visible(False)
        axs[0].spines['right'].set_visible(False)
        axs[1].spines['top'].set_visible(False)
        axs[1].spines['right'].set_visible(False)


    else:
        for trial_idx, _ in enumerate(np.arange(np.shape(I_stim)[0])):
            axs[0, trial_idx].plot(t, V_m[trial_idx] * 1e3)
            axs[1, trial_idx].plot(t, I_stim[trial_idx] * 1e12)
            
            if trial_idx == 0:
                axs[0, trial_idx].set_ylabel('$V_{m}\;(mV)$')
                axs[1, trial_idx].set_ylabel('$I_{stim}\;(pA)$')   
                axs[1, trial_idx].set_xlabel('$t\;(s)$')

            axs[0, trial_idx].spines['top'].set_visible(False)
            axs[0, trial_idx].spines['right'].set_visible(False)
            axs[1, trial_idx].spines['top'].set_visible(False)
            axs[1, trial_idx].spines['right'].set_visible(False)

    if subtitle is None:
        fig.suptitle(title)
    else:
        fig.suptitle(title + '\n' + subtitle)