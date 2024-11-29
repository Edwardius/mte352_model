import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # Import tqdm for progress tracking

# Constants
G = 9.81  # Gravitational acceleration (m/s^2)
RHO = 1000  # Water density (kg/m^3)
MU = 0.001  # Dynamic viscosity of water (Pa.s)
D_TUBE = 0.00794  # Tube diameter (m)
A_TUBE = np.pi * (D_TUBE / 2)**2  # Tube cross-sectional area (m^2)
LENGTH_TANK = 0.32  # Tank length (m)
WIDTH_TANK = 0.26  # Tank width (m)
A_TANK = LENGTH_TANK * WIDTH_TANK  # Tank cross-sectional area
EPSILON = 0.0000015  # Roughness of the tube (m), PVC

# Minor Losses
"""
For a sharp-edged entrance (common for pipes entering a sidewall): K_ENTRANCE = 0.5
This value ranges from 0 to 0.5 based on how rounded the edge is.
"""
K_ENTRANCE = 0.45 # Entrance loss coefficient (approx common value for pipes entering a sidewall apparently)
"""
K_EXIT = 0 when:
    - Steady Stream: If the flow exits the pipe smoothly without significant turbulence or energy dissipation into free space (e.g., directly into another container or system).
    - Laminar Flow at Exit: If the flow inside the pipe is laminar and continues to flow as a steady stream, the exit loss is minimal.
    - No Sharp Discontinuity: If the pipe discharges into an environment at the same pressure (e.g., into water at atmospheric pressure without sudden expansion).
K_EXIT != 0 when
    - Free Jet Expansion: When water exits into open air or free space and undergoes a sudden expansion, causing dissipation of kinetic energy.
    - Turbulent Flow at Exit: If the flow inside the pipe is turbulent and disperses upon exiting, the kinetic energy lost to turbulence needs to be accounted for.
    - Sudden Contraction Upstream: If there is a sharp change in flow cross-section before the pipe exit, turbulence at the exit can increase losses.
"""
K_EXIT = 0  # Exit loss coefficient (no significant turbulence)

# Initial conditions
H_INITIAL = 0.10  # Initial water height (m)
H_FINAL = 0.02  # Final height (m)
DT = 0.01  # Time step (s)

# Functions
def colebrook(Re, d, f):
    """Colebrook-White equation for friction factor."""
    return (-2.0 * np.log10(EPSILON / (3.7 * d) + 2.51 / (Re * np.sqrt(f)))) ** -2

def calculate_velocity_and_friction(h, L, tol=1e-6, max_iterations=100):
    """
    Calculate velocity and friction factor iteratively until friction factor converges.

    Parameters:
        h: Water height (m)
        L: Tube length (m)
        tol: Convergence tolerance for the friction factor
        max_iterations: Maximum number of iterations to prevent infinite loop

    Returns:
        v: Velocity (m/s)
        f: Friction factor
    """
    f = 0.02  # Initial guess for friction factor
    v = np.sqrt(2 * G * h / (1 + (f * L / D_TUBE) + K_ENTRANCE + K_EXIT))  # Initial velocity
    for _ in range(max_iterations):
        Re = RHO * v * D_TUBE / MU
        if Re < 1e-6:  # Avoid division by zero
            Re = 1e-6
        if Re < 2300:  # Laminar flow
            new_f = 64 / Re
        else:  # Turbulent flow
            new_f = colebrook(Re, D_TUBE, f)
        
        # Check for convergence
        if abs(new_f - f) < tol:
            break
        
        f = new_f  # Update friction factor
        v = np.sqrt(2 * G * h / (1 + (f * L / D_TUBE) + K_ENTRANCE + K_EXIT))  # Update velocity

    return v, f


def simulate_drain_time(L):
    """Simulate the total drain time for a given tube length."""
    h = H_INITIAL
    total_time = 0
    heights = []  # To store height values over time
    times = []    # To store corresponding time values

    while h > H_FINAL:
        v, f = calculate_velocity_and_friction(h, L)
        dh = (A_TUBE / A_TANK) * v * DT  # Change in height
        h -= dh  # Update height
        total_time += DT  # Increment time
        
        # Store values for plotting
        heights.append(h)
        times.append(total_time)

    return total_time, times, heights

# Tube lengths from 20 to 60 cm (converted to meters)
tube_lengths = np.linspace(0.2, 0.6, 10)  # Tube lengths in meters
# Compute drain times and friction factors
results = [simulate_drain_time(L) for L in tqdm(tube_lengths, desc="Simulating drain times")]

# Unpack the results into separate lists
total_times, times_list, heights_list = zip(*results)

# Plot total drain times for different tube lengths
plt.figure(figsize=(8, 6))
# Data extracted from the image
cases_cm = [0.20, 0.30, 0.40, 0.60]  # Tube lengths in cm
average_times = [3*60 + 19, 3*60 + 34, 4*60 + 26, 4*60 + 48]  # Average times converted to seconds
plt.plot(cases_cm, average_times, marker="x", label="Experimental Average Drain Time")
plt.plot(tube_lengths, total_times, marker="o", label="Drain Times")
for i, (L, time) in enumerate(zip(tube_lengths, total_times)):
    plt.annotate(f"{time:.1f}s", (L, time), textcoords="offset points", xytext=(5, 10), ha="center")
plt.xlabel("Tube Length (m)")
plt.ylabel("Total Drain Time (s)")
plt.title("Total Drain Time vs Tube Length")
plt.legend()
plt.grid(True)
plt.show()

# Plot all height-time curves on a single plot
plt.figure(figsize=(10, 6))
for i, (L, times, heights) in enumerate(zip(tube_lengths, times_list, heights_list)):
    plt.plot(times, heights, label=f"L = {L:.2f} m")

plt.xlabel("Time (s)")
plt.ylabel("Height (m)")
plt.title("Height of Water Over Time for Different Tube Lengths")
plt.legend(title="Tube Lengths")
plt.grid(True)
plt.show()
