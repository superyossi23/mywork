"""
22.08.30

"""

import numpy as np
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt


n = np.linspace(0, 1000, 1000)  # 0 to 1000 us sampled at 1000 MHz

# NOISE
pulse_freq = 20  # kHz
amplitude = 10  # V
noise_pulse = signal.square(2 * np.pi * pulse_freq * n, duty=0.8*10**-2) * amplitude + amplitude

# SIGNAL
pulse_freq = 5  # kHz
amplitude = 2.5  # V
signal_pulse = signal.square(2 * np.pi * pulse_freq * n) * amplitude + amplitude

# SAVING WAVEFORM
n = n * 10**-6  # us
signal = (noise_pulse + signal_pulse)

# SAVE
save_file = pd.DataFrame([n, signal])
save_file = save_file.T
# save_file.to_csv('create_waveform.csv', header=False, index=False)

print('create_waveform.py done!!\ncreate_waveform.csv was saved.')

