import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Cosinor model function
def cosinor_model(t, mesor, amplitude, acrophase):
    return mesor + amplitude * np.cos(2 * np.pi * t - acrophase)

# Function to perform Cosinor analysis
def perform_cosinor_analysis(data, time_col, temp_col):
    # Extract time and temperature values
    time = data[time_col]
    temp = data[temp_col]
    
    # Initial guesses for MESOR, Amplitude, Acrophase
    mesor_guess = temp.mean()
    amplitude_guess = (temp.max() - temp.min()) / 2
    acrophase_guess = 0
    
    # Fit the Cosinor model to the data
    params, covariance = curve_fit(cosinor_model, time, temp, p0=[mesor_guess, amplitude_guess, acrophase_guess])
    
    mesor, amplitude, acrophase = params
    
    return {
        "MESOR": mesor,
        "Amplitude": amplitude,
        "Acrophase": acrophase,
        "Fitted Values": cosinor_model(time, *params)
    }

# Additional utility functions from your notebook can be added here
