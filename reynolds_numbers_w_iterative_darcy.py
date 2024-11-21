# Import necessary libraries
import numpy as np
import pandas as pd

# Constants
rho = 1000  # Density of water (kg/m^3)
mu = 1e-3   # Dynamic viscosity of water (Pa·s)
g = 9.81    # Gravitational acceleration (m/s^2)
D = 0.00794  # Tube diameter (m)

# Iterative calculation for Darcy friction factor and Reynolds number
def iterative_darcy_reynolds(h, L, epsilon, D, K, rho=1000, mu=1e-3, max_iter=100, tol=1e-6):
    """
    Iteratively calculate Reynolds number and Darcy friction factor.
    
    Parameters:
    - h: Water height above tube inlet (m)
    - L: Tube length (m)
    - epsilon: Roughness height (m)
    - D: Diameter of the pipe (m)
    - K: Minor loss coefficient (dimensionless)
    - rho: Fluid density (kg/m^3), default = 1000 for water
    - mu: Fluid viscosity (Pa·s), default = 1e-3 for water
    - max_iter: Maximum iterations for convergence
    - tol: Tolerance for convergence
    
    Returns:
    - Re: Final Reynolds number (dimensionless)
    - f: Final Darcy friction factor (dimensionless)
    """
    # Initial guess for Darcy friction factor
    f = 0.02
    for i in range(max_iter):
        # Calculate velocity
        v = np.sqrt(2 * g * h / (1 + f * L / D + K))
        
        # Calculate Reynolds number
        Re = (rho * v * D) / mu
        
        # Update Darcy friction factor
        if Re < 2000:  # Laminar flow
            f_new = 64 / Re
        else:  # Turbulent flow
            f_new = (-1.8 * np.log10((epsilon / D) / 3.7 + 6.9 / Re))**-2
        
        # Check for convergence
        if abs(f_new - f) < tol:
            return Re, f_new
        
        # Update friction factor
        f = f_new
    
    raise RuntimeError("Darcy friction factor did not converge")

# Parameters for the simulation
heights = np.linspace(0.01, 0.1, 10)  # Heights (m)
lengths = [0.2, 0.3, 0.4, 0.6]        # Tube lengths (m)
epsilon = 0.0015  # Pipe roughness (e.g., PVC pipe, in meters)
K = 1.5           # Minor loss coefficient (e.g., entrance + exit)

# Run the simulation
results_full_search = []
for L in lengths:
    for h in heights:
        try:
            Re, f = iterative_darcy_reynolds(h, L, epsilon, D, K)
            results_full_search.append((h, L, Re, f))
        except RuntimeError as e:
            results_full_search.append((h, L, None, None))

# Convert results to a DataFrame
columns = ["Height (m)", "Length (m)", "Reynolds Number", "Darcy Friction Factor"]
df_full_search = pd.DataFrame(results_full_search, columns=columns)

# Save results to a new file
file_path = "output/Reynolds_Darcy_Full_Search.csv"
df_full_search.to_csv(file_path, index=False)
