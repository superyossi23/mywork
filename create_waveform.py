"""
22.08.30

"""

import numpy as np
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt


n = np.linspace(0, 400*10**-6, 500)
pulse_freq = 20*10**3  # us
amplitude = 10  # V
noise_pulse = signal.square(np.pi * pulse_freq * n, duty=10**-2) * amplitude + amplitude

pulse_freq = 5 * 10**3  # us
amplitude = 2.5  # V
signal_pulse = signal.square(2 * np.pi * pulse_freq * n) * amplitude + amplitude

signal = noise_pulse + signal_pulse

# save_file = np.array([n, signal])
# np.savetxt('create_waveform.csv', save_file, delimiter=',')
save_file = pd.DataFrame([n, signal])
save_file = save_file.T
save_file.to_csv('create_waveform.csv', header=False, index=False)

