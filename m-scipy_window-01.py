#%%
import numpy as np
from scipy.signal import windows

# Generate a time series data
time_series = np.random.rand(100)

# Specify the window size and type
window_size = 10
window_type = "hamming"  # You can choose from various window types such as 'hamming', 'hann', 'blackman', etc.

# Generate the window function
window = windows.get_window(window_type, window_size)

# Reshape the window to match the shape of the time series
window = window.reshape((-1, 1))

# Apply the window to the time series data
windowed_time_series = time_series * window

# Print the results
print("Original Time Series:", time_series)
print("Window Function:", window)
print("Windowed Time Series:", windowed_time_series)

# %%
