# Function to apply moving average with a window size of 3
import numpy as np
from scipy.signal import butter, filtfilt
import pandas as pd


def moving_average(signal, window_size):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='valid')

def butter_bandpass(lowcut, highcut, fs, order):
    nyquist = 0.5 * fs  # Nyquist frequency
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def compute_mnf(fi, Pi):
    """
    Compute the Mean Frequency (MNF) for each time segment.

    Parameters:
    - fi: array of frequencies (f_i)
    - Pi: 2D array of power spectral density (PSD) values (time x frequency)

    Returns:
    - MNF: Array of MNF values for each time segment
    """
    numerator = np.sum(Pi * fi[:, np.newaxis], axis=0)
    denominator = np.sum(Pi, axis=0)
    
    MNF = np.where(denominator != 0, numerator / denominator, 0)
    return MNF

def compute_mdf(Pi):
    """
    Compute the Median Frequency (MDF) for each time segment.

    Parameters:
    - Pi: 2D array of power spectral density (PSD) values (time x frequency)

    Returns:
    - MDF: Array of MDF values for each time segment
    """
    sum_Pi = np.sum(Pi, axis=0)
    MDF = sum_Pi / 2
    return MDF


def apply_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def export_emg_features_to_csv(mean_freq, median_freq, output_file):
    """Exports raw EMG data, mean frequency, and median frequency to a CSV file.
    
    Args:
        emg_data (np.ndarray): The raw EMG data.
        mean_freq (np.ndarray): The computed mean frequencies.
        median_freq (np.ndarray): The computed median frequencies.
        output_file (str): The path to the output CSV file.
    """
    # Create a DataFrame to hold the data
    data = {
        'Mean Frequency (Hz)': mean_freq,
        'Median Frequency (Hz)': median_freq
    }
    
    df = pd.DataFrame(data)
    
    # Export to CSV
    df.to_csv(output_file, index=False)
    print(f"Data exported to {output_file}")

def export_raw_emg_to_csv(emg_data, output_file):
    """Exports raw EMG data, mean frequency, and median frequency to a CSV file.
    
    Args:
        emg_data (np.ndarray): The raw EMG data.
        mean_freq (np.ndarray): The computed mean frequencies.
        median_freq (np.ndarray): The computed median frequencies.
        output_file (str): The path to the output CSV file.
    """
    # Create a DataFrame to hold the data
    data = {
        'Raw Emg': emg_data
    }
    
    df = pd.DataFrame(data)
    
    # Export to CSV
    df.to_csv(output_file, index=False)
    print(f"Data exported to {output_file}")    

def read_csv_as_emg_array(file_path):
    """Reads a CSV file and returns the EMG data as a numpy array.
    
    Assumes that the EMG data is in the first column.
    
    Args:
        file_path (str): Path to the CSV file.

    Returns:
        np.ndarray: Array of EMG data.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Assuming EMG data is in the first column
        emg_array = df.iloc[:, 0].values
        return np.array(emg_array)
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    