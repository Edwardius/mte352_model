import numpy as np

# Constants
rho = 1000  # Density of water (kg/m^3)
mu = 1e-3   # Dynamic viscosity of water (Pa·s)
g = 9.81    # Gravitational acceleration (m/s^2)
D = 0.00794  # Tube diameter (m)

# Function to calculate Reynolds number
def calculate_reynolds(h, L=0, f=0):
    """
    Calculate the Reynolds number for given water height (h) and tube length (L).
    
    Parameters:
    - h: Water height above tube inlet (m)
    - L: Tube length (m), default is 0 (neglect friction loss)
    - f: Darcy friction factor, default is 0 (neglect friction loss)
    
    Returns:
    - Re: Reynolds number (dimensionless)
    """
    # Calculate velocity
    if f == 0:
        v = np.sqrt(2 * g * h)  # Simplified without friction losses
    else:
        v = np.sqrt(2 * g * h / (1 + f * L / D))
    
    # Calculate Reynolds number
    Re = (rho * v * D) / mu
    return Re

# Example: Varying height and lengths
heights = np.linspace(0.01, 0.1, 10)  # Heights from 0.01m to 0.1m
lengths = [0.2, 0.3, 0.4, 0.6]       # Example tube lengths (m)

# Calculate Reynolds number for different heights and lengths
results = []
for L in lengths:
    Re_values = [calculate_reynolds(h, L=L) for h in heights]
    results.append((L, Re_values))

import pandas as pd

# Convert results to a DataFrame for clarity
data = pd.DataFrame({
    "Height (m)": heights,
    **{f"L = {L} m": values for L, values in results}
})

print(data)
