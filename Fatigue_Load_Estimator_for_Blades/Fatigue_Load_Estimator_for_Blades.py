import numpy as np
import matplotlib.pyplot as plt

# Material constants for S-N curve (simplified for wind turbine blade composite)
m = 10.0  # S-N curve slope
S_ref = 50e6  # Reference stress amplitude in Pa (50 MPa)
N_ref = 1e6   # Cycles to failure at S_ref
C = N_ref * S_ref ** m  # S-N constant (N = C / S^m)

def rainflow(data):
    """
    Simplified rainflow counting algorithm to extract cycles from load time series.
    Returns list of (amplitude, count) where count is 1 for full cycles, 0.5 for half cycles.
    """
    # Extract turning points (peaks and valleys)
    tp = []
    for val in data:
        while len(tp) >= 2 and (val - tp[-1]) * (tp[-1] - tp[-2]) <= 0:
            tp.pop()
        tp.append(val)
    
    # Rainflow cycle extraction
    cycles = []
    i = 0
    while len(tp) - i >= 3:
        S0 = tp[i]
        S1 = tp[i + 1]
        S2 = tp[i + 2]
        r1 = abs(S1 - S0)
        r2 = abs(S2 - S1)
        if r1 <= r2:
            cycles.append((r1 / 2, 1.0))  # Amplitude and full cycle count
            tp.pop(i + 1)
        else:
            i += 1
    
    # Remaining residues as half cycles
    for j in range(i, len(tp) - 1):
        r = abs(tp[j + 1] - tp[j])
        cycles.append((r / 2, 0.5))  # Amplitude and half cycle count
    
    return cycles

# Define wind regimes (mean wind speed m/s, standard deviation for turbulence)
wind_regimes = {
    'Calm': (6.0, 1.5),
    'Normal': (10.0, 2.5),
    'Stormy': (14.0, 4.0)
}

# Simulation parameters
num_segments = 24  # Hours in a day
points_per_segment = 1000  # Data points per hour
segment_duration = 3600  # Seconds per segment (1 hour)

for regime, (mean_wind, std_wind) in wind_regimes.items():
    damage_accum = []
    cum_damage = 0.0
    
    for seg in range(num_segments):
        # Slight hourly variation in mean wind
        current_mean = mean_wind + np.random.normal(0, 0.5)
        
        # Time array for the segment
        t = np.linspace(0, segment_duration, points_per_segment)
        
        # Simulate wind speed with sinusoidal gusts (period ~5 min) and noise
        wind = current_mean + std_wind * np.sin(2 * np.pi * t / 300) + np.random.normal(0, std_wind / 2, points_per_segment)
        
        # Simplified stress calculation (proportional to wind speed squared, scaled to MPa range)
        stress = 0.5e6 * wind ** 2  # Results in stress amplitudes around 50e6 Pa for normal wind
        
        # Apply rainflow counting
        cycles = rainflow(stress)
        
        # Compute damage for the segment using Miner's rule
        segment_damage = 0.0
        for amp, count in cycles:
            if amp > 0:
                N = C / amp ** m
                segment_damage += count / N
        
        cum_damage += segment_damage
        damage_accum.append(cum_damage)
    
    # Plot damage accumulation for this regime
    times = np.arange(1, num_segments + 1)
    plt.plot(times, damage_accum, label=regime)
    
    # Estimate fatigue life (assuming this simulation represents one typical day)
    daily_damage = cum_damage
    if daily_damage > 0:
        life_days = 1.0 / daily_damage
        life_years = life_days / 365.25
    else:
        life_years = float('inf')
    
    print(f"{regime} regime:")
    print(f"  Daily damage: {daily_damage:.2e}")
    print(f"  Estimated fatigue life: {life_years:.2f} years\n")

# Final plot
plt.xlabel('Time (hours)')
plt.ylabel('Cumulative Fatigue Damage')
plt.title('Fatigue Damage Accumulation Over One Day for Different Wind Regimes')
plt.legend()
plt.grid(True)
plt.show()