import biosppy.signals.emg
import serial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.signal import stft
from aux_functions import export_emg_features_to_csv, moving_average, apply_bandpass_filter, read_csv_as_emg_array, export_raw_emg_to_csv


# ---------- Data Acquisition ----------
arduino = serial.Serial('COM4', 500000)
i = 0
emg_data = []

try:
    while len(emg_data) < 5000:
        if arduino.in_waiting > 0:
            value = arduino.readline().decode('utf-8').strip()
            timestamp, data = map(float, value.split(","))
            emg_data.append(float(data))  # Convert to float
            i += 1
            progress = (i / 5000) * 100
            bar_length = 40
            filled_length = int(bar_length * i // 5000)
            bar = '=' * filled_length + '-' * (bar_length - filled_length)

            sys.stdout.write(f'\rProgress: |{bar}| {progress:.2f}% Complete')
            sys.stdout.flush()
except KeyboardInterrupt:
    print("\nData collection interrupted")

arduino.close()

# ---------- Signal Processing ----------
# emg_array = read_csv_as_emg_array("emg_raw_data.csv")
emg_array = np.array(emg_data)

emg_processed = biosppy.signals.emg.emg(signal=emg_array, sampling_rate=1000, show=False)
filtered_emg = apply_bandpass_filter(emg_array, lowcut=20, highcut=400, fs=1000, order=6)
rectified_emg = np.abs(filtered_emg)
smoothed_signal = moving_average(rectified_emg, window_size=3)



# ---------- STFT Calculation ----------
fs = 1000
nperseg = 256

frequencies, t_stft, Zxx = stft(filtered_emg, fs, nperseg=nperseg)


# Feature Extraction (Mean and Median Frequency)

# Mean frequency [MNF]
power_spectrum_stft = np.abs(Zxx) ** 2
mean_freq = np.sum(frequencies[:, np.newaxis] * power_spectrum_stft, axis=0) / np.sum(power_spectrum_stft, axis=0)

# Median frequency [MDF]

median_freq = np.sum(power_spectrum_stft, axis=0) / 2


# ---------- Plotting ----------
plt.figure(figsize=(14, 8))

plt.subplot(3,1,1)
plt.plot(emg_array, label="Raw Emg", color="blue", alpha=0.6)
plt.plot(filtered_emg, label="Filtered Emg", color="purple")
plt.title("Raw and Filtered Emg")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")
plt.grid()

plt.subplot(3,1,2)
plt.plot(rectified_emg, label="Rectified", color="red")
plt.title("Rectified Emg")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")
plt.grid()

plt.subplot(3,1,3)
plt.plot(smoothed_signal, label="Smoothed Signal", color="green")
plt.title("Smoothed Emg")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")
plt.grid()

plt.legend()
plt.tight_layout()
plt.show()

# Results Figure

plt.subplot(2,2,1)
plt.plot(mean_freq, label="Mean Frequency", color="red")
plt.title("Mean Frequency")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.grid()

plt.subplot(2,2,2)
plt.plot(median_freq, label="median frequency", color="green")
plt.title("Median Frequency")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.grid()

plt.subplot(2,1,2)
plt.plot(filtered_emg, label="Filtered Emg", color="blue")
plt.title("Filtered Emg")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (mV)")
plt.grid()

plt.legend()
plt.tight_layout()
plt.show()


export_emg_features_to_csv(mean_freq, median_freq, "emg_features.csv")
export_raw_emg_to_csv(emg_array, "emg_raw_data.csv")
