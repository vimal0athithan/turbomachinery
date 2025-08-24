import numpy as np
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt

# Parameters
D = 100.0  # Rotor diameter (m)
rho = 1.225  # Air density (kg/m^3)
Cp = 0.4  # Power coefficient
k = 0.075  # Wake decay constant
Ct = 0.8  # Thrust coefficient
U0 = 12.0  # Free stream wind speed (m/s)
farm_size = 2000.0  # Square farm size (m)
min_dist = 5 * D  # Minimum turbine distance (m)
N = 9  # Number of turbines
wind_dir = 0.0  # Wind direction (radians, 0 = from positive x-axis)

# Function to calculate effective wind speed at a turbine considering wakes
def get_wind_speed_at_turbine(turbine_idx, positions):
    pos_i = positions[turbine_idx]
    deficit_sum = 0.0
    wind_vec = np.array([np.cos(wind_dir), np.sin(wind_dir)])
    
    for j in range(N):
        if j == turbine_idx:
            continue
        pos_j = positions[j]
        vec = pos_i - pos_j
        proj = np.dot(vec, wind_vec)  # Downstream projection
        if proj <= 0:
            continue  # Upstream, no wake
        dist = np.linalg.norm(vec)
        cross_dist = np.linalg.norm(vec - proj * wind_vec)
        R = D / 2.0
        wake_radius = R + k * proj
        if cross_dist >= wake_radius:
            continue  # Outside wake
        a = (1 - np.sqrt(1 - Ct)) / 2.0
        deficit = 2 * a / (1 + k * proj / R) ** 2
        deficit_sum += deficit ** 2  # Sum of squares for multiple wakes
    
    U_eff = U0 * (1 - np.sqrt(deficit_sum))
    return max(U_eff, 0.0)

# Objective function: total power (to maximize, return negative for minimization)
def total_power(pos_flat):
    positions = pos_flat.reshape(-1, 2)
    P_total = 0.0
    A = np.pi * (D / 2.0) ** 2
    
    for i in range(N):
        U = get_wind_speed_at_turbine(i, positions)
        P = 0.5 * rho * A * Cp * U ** 3
        P_total += P
    
    # Penalty for violating minimum distance
    penalty = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < min_dist:
                penalty += (min_dist - dist) ** 2
    
    return - (P_total - 1e6 * penalty)  # Large penalty to enforce constraints

# Optimization using differential evolution
bounds = [(0, farm_size)] * (2 * N)
result = differential_evolution(total_power, bounds, popsize=20, maxiter=100, workers=1)
best_pos = result.x.reshape(-1, 2)
best_power = -result.fun  # Convert back to positive power

print(f"Optimized total power: {best_power / 1e6:.2f} MW")

# Plot the optimized layout
def plot_layout(positions):
    fig, ax = plt.subplots()
    ax.scatter(positions[:, 0], positions[:, 1], color='blue', s=100)
    ax.set_xlim(0, farm_size)
    ax.set_ylim(0, farm_size)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Optimized Wind Farm Layout')
    plt.grid(True)
    plt.show()

# Plot wake profiles (velocity field)
def plot_wake(positions):
    x = np.linspace(0, farm_size, 100)
    y = np.linspace(0, farm_size, 100)
    X, Y = np.meshgrid(x, y)
    U_field = np.full_like(X, U0)
    wind_vec = np.array([np.cos(wind_dir), np.sin(wind_dir)])
    
    for j in range(N):
        pos_j = positions[j]
        vec_x = X - pos_j[0]
        vec_y = Y - pos_j[1]
        proj = vec_x * wind_vec[0] + vec_y * wind_vec[1]
        cross_dist = np.sqrt(vec_x**2 + vec_y**2 - proj**2)
        mask = proj > 0
        R = D / 2.0
        wake_radius = R + k * proj
        in_wake = (cross_dist < wake_radius) & mask
        a = (1 - np.sqrt(1 - Ct)) / 2.0
        deficit = np.zeros_like(X)
        deficit[in_wake] = 2 * a / (1 + k * proj[in_wake] / R) ** 2
        U_field[in_wake] -= U0 * deficit[in_wake]  # Approximate linear superposition
    
    fig, ax = plt.subplots()
    contour = ax.contourf(X, Y, U_field, levels=20, cmap='viridis')
    plt.colorbar(contour, ax=ax, label='Wind Speed (m/s)')
    ax.scatter(positions[:, 0], positions[:, 1], color='red', s=50, label='Turbines')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Wind Farm Wake Profiles')
    ax.legend()
    plt.grid(True)
    plt.show()

# Generate plots
plot_layout(best_pos)
plot_wake(best_pos)