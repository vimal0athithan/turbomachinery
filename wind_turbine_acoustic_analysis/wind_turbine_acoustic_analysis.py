import numpy as np
import matplotlib.pyplot as plt

# Constants
C0 = 343.0  # speed of sound in m/s
NU = 1.5e-5  # kinematic viscosity in m^2/s
R = 100.0  # observer distance in m
L = 50.0  # blade span in m (assumed for a typical wind turbine blade)
D_H = 1.0  # approximate directivity (simplified)

def get_A(a):
    """Spectral shape function A (using A_min for high Re approximation)"""
    if a < 0.204:
        return np.sqrt(67.552 - 886.788 * a**2) - 8.219
    elif a <= 0.244:
        return -32.665 * a + 3.981
    else:
        return -142.795 * a**3 + 103.656 * a**2 - 57.757 * a + 6.006

def get_K1(Re):
    """Approximate K1 as a piece-wise linear function of log10(Re) based on BPM model"""
    logRe = np.log10(Re)
    if logRe <= 4.7:
        return -4.0
    elif logRe <= 5.3:
        return -4.0 + ((-9.0 + 4.0) / (5.3 - 4.7)) * (logRe - 4.7)
    elif logRe <= 5.9:
        return -9.0 + ((-12.5 + 9.0) / (5.9 - 5.3)) * (logRe - 5.3)
    else:
        return -12.5

def estimate_spl(tip_speed, chord, wind_speed):
    """
    Estimate the sound pressure level (SPL) spectrum and overall SPL using a simplified BPM model for airfoil self-noise.
    Assumptions: Zero angle of attack, tripped boundary layer, trailing edge noise dominant.
    Inputs:
    - tip_speed: blade tip speed in m/s
    - chord: blade chord length in m
    - wind_speed: wind speed in m/s (used to compute effective velocity)
    Returns:
    - f: frequency array
    - SPL: SPL spectrum in dB
    - overall_SPL: overall SPL in dB
    """
    # Effective velocity (relative speed at blade)
    U = np.sqrt(tip_speed**2 + wind_speed**2)
    Re = U * chord / NU
    M = U / C0
    # Displacement thickness (tripped, zero alpha)
    delta_star = 0.0306 * Re**(-0.117) * chord
    St1 = 0.02 * M**(-0.6)
    K1 = get_K1(Re)
    # Frequency range
    f = np.logspace(1, 4, 100)  # 10 Hz to 10 kHz
    St = f * delta_star / U
    a = np.abs(np.log10(St / St1))
    A = np.vectorize(get_A)(a)
    # SPL spectrum (simplified for zero alpha)
    SPL = 10 * np.log10(delta_star * M**5 * L * D_H / R**2) + A + K1
    # Overall SPL
    overall_SPL = 10 * np.log10(np.sum(10**(SPL / 10)))
    return f, SPL, overall_SPL

# Example usage to compare different blade designs
if __name__ == "__main__":
    # Design 1: Baseline
    tip_speed1 = 70.0  # m/s
    chord1 = 2.0  # m
    wind_speed1 = 10.0  # m/s
    f1, SPL1, overall1 = estimate_spl(tip_speed1, chord1, wind_speed1)
    print(f"Design 1 - Overall SPL: {overall1:.2f} dB")

    # Design 2: Alternative (faster tip, smaller chord)
    tip_speed2 = 80.0  # m/s
    chord2 = 1.5  # m
    wind_speed2 = 10.0  # m/s
    f2, SPL2, overall2 = estimate_spl(tip_speed2, chord2, wind_speed2)
    print(f"Design 2 - Overall SPL: {overall2:.2f} dB")

    # Plot comparison
    plt.figure(figsize=(10, 6))
    plt.semilogx(f1, SPL1, label='Design 1')
    plt.semilogx(f2, SPL2, label='Design 2')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SPL (dB)')
    plt.title('SPL Spectrum Comparison for Different Blade Designs')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Table for comparison
    print("\nComparison Table:")
    print("| Design | Tip Speed (m/s) | Chord (m) | Wind Speed (m/s) | Overall SPL (dB) |")
    print("|--------|-----------------|-----------|------------------|------------------|")
    print(f"| 1      | {tip_speed1}            | {chord1}       | {wind_speed1}             | {overall1:.2f}           |")
    print(f"| 2      | {tip_speed2}            | {chord2}       | {wind_speed2}             | {overall2:.2f}           |")