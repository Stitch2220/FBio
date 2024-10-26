import numpy as np 
import matplotlib.pyplot as plt

# Generate random EMG data
emg_data = np.random.rand(1000)
sampling_rate = 1000

# Compute FFT and power spectrum
n = len(emg_data)
frequencies = np.fft.rfftfreq(n, d=1/sampling_rate)
fft_magnitude = np.abs(np.fft.rfft(emg_data))
power_spectrum = fft_magnitude ** 2

# Calculate mean and median frequencies
mean_frequency = np.sum(frequencies * power_spectrum) / np.sum(power_spectrum)
cumulative_power = np.cumsum(power_spectrum)
total_power = cumulative_power[-1]
median_frequency = frequencies[np.where(cumulative_power >= total_power/2)[0][0]]

# Plot power spectrum
plt.figure(figsize=(10, 6))
plt.plot(frequencies, power_spectrum, label='Power Spectrum')
plt.axvline(mean_frequency, color='r', linestyle='--', label=f'Mean Frequency: {mean_frequency:.2f} Hz')
plt.axvline(median_frequency, color='g', linestyle='--', label=f'Median Frequency: {median_frequency:.2f} Hz')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.title('Power Spectrum with Mean and Median Frequencies')
plt.legend()
plt.show()