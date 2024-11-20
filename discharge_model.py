import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # gravitational acceleration (m/s^2)
rho = 1000  # density of water (kg/m^3)
mu = 0.001  # dynamic viscosity of water (Pa·s)
diameter = 7.94 / 1000  # tube diameter in meters
area = np.pi * (diameter / 2)**2  # cross-sectional area of the tube (m^2)
H = 0.08  # initial height of water in the reservoir (m)

# Function to calculate Reynolds number
def reynolds_number(v, d, mu):
    return (v * d) / mu

# Friction factor using the Darcy-Weisbach equation
def friction_factor(Re):
    if Re < 2000:  # Laminar flow
        return 64 / Re
    elif Re < 4000:  # Transitional flow
        return 0.3164 * (Re**-0.25)
    else:  # Turbulent flow
        return 0.184 * (Re**-0.2)

# Drain time calculation
def drain_time(L):
    h = H
    dt = 0.01  # time step (s)
    time = 0

    while h > 0.04:  # Stop draining when water height reaches 4 cm
        v = np.sqrt(2 * g * h)  # velocity using Bernoulli's principle
        Re = reynolds_number(v, diameter, mu)
        f = friction_factor(Re)
        head_loss = f * (L / diameter) * (v**2 / (2 * g))  # Major losses
        v_actual = np.sqrt(2 * g * (h - head_loss))  # Adjusted velocity
        dh = -(v_actual * area * dt) / (np.pi * (0.5)**2)  # Change in height
        h += dh
        time += dt

    return time

# Evaluate different tube lengths
tube_lengths = np.arange(0.2, 0.7, 0.1)  # Tube lengths from 20 cm to 60 cm
times = [drain_time(L) for L in tube_lengths]

# Optimal tube length (minimum drain time)
optimal_length = tube_lengths[np.argmin(times)]

# Plotting results
plt.figure()
plt.plot(tube_lengths, times, marker='o')
plt.title("Drain Time vs Tube Length")
plt.xlabel("Tube Length (m)")
plt.ylabel("Drain Time (s)")
plt.grid()
plt.show()

print(f"Optimal tube length for minimum drain time: {optimal_length:.2f} m")
