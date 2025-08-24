# Fatigue Load Estimator for Blades

## Overview
This Python script estimates the fatigue life of wind turbine blades under varying wind conditions using a simplified S-N curve approach and a rainflow counting algorithm. It simulates fatigue damage accumulation over time for different wind regimes (Calm, Normal, and Stormy) and plots the results. Developed as part of my turbomachinery portfolio, this tool showcases skills in structural engineering, fatigue analysis, and Python programming, prepared for Siemens HR review on August, 2025.

**Key Features:**
- Implements S-N curve with rainflow cycle counting.
- Simulates wind-induced stress for Calm (6 m/s), Normal (10 m/s), and Stormy (14 m/s) regimes.
- Plots cumulative fatigue damage over 24 hours.
- Estimates blade fatigue life based on Miner's rule.

**Author**: Vimal Athithan  
**Date**: August 24, 2025, 10:06 PM IST  
**GitHub**: [vimal0athithan](https://github.com/vimal0athithan)  
**Contact**: [vimalgnani@gmail.com](mailto:vimalgnani@gmail.com)

## Installation
1. **Clone the Repository**:
   ```
   git clone https://github.com/vimal0athithan/turbomachinery.git
   cd turbomachinery/fatigue-load-estimator
   ```
2. **Set Up a Virtual Environment** (recommended):
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```
   pip install numpy matplotlib
   ```

## Usage
1. Ensure Python 3.13+ and dependencies (`numpy`, `matplotlib`) are installed.
2. Run the script:
   ```
   python fatigue_load_estimator.py
   ```
3. **Output**:
   - Console displays average hourly damage and estimated fatigue life for each regime.
   - A Matplotlib plot shows cumulative fatigue damage over 24 hours for all regimes.
4. **Customize**:
   - Modify `wind_regimes` in the script to adjust mean wind speeds or turbulence intensity.
   - Adjust material constants (`m`, `S_ult`, `C`) in the S-N curve for different blade materials.

## Simulation Results (August 24, 2025)
The script was run with the following outputs, indicating fatigue damage and life estimates:

- **Calm Regime (6 m/s mean wind, low turbulence):**
  - Average hourly damage: 1.31e-12
  - Estimated fatigue life: 87,086,611.19 years
  - *Interpretation*: Negligible damage due to low wind speeds, suggesting an unrealistically long life. Likely indicates underestimation of stress or overestimation of material strength.

- **Normal Regime (10 m/s mean wind, moderate turbulence):**
  - Average hourly damage: 4.75e+06
  - Estimated fatigue life: 0.00 years
  - *Interpretation*: Excessive damage predicts immediate failure, indicating overestimation of stress or misalignment with material fatigue properties.

- **Stormy Regime (14 m/s mean wind, high turbulence):**
  - Average hourly damage: 3.81e+01
  - Estimated fatigue life: 0.00 years
  - *Interpretation*: High damage under stormy conditions also predicts instant failure, reinforcing the need for model calibration.

**Note**: These results suggest the model requires calibration (e.g., stress scaling, S-N curve parameters) to align with realistic blade life (20-30 years). Current estimates range from overly optimistic (Calm) to catastrophic (Normal, Stormy).

## Technical Details
- **Model**: Simplified S-N curve with `m = 10`, `S_ult = 100e6 Pa`, and derived `C`. Rainflow counting follows ASTM E1049-85 principles.
- **Assumptions**:
  - Stress proportional to wind speed squared (scaled by 1e6).
  - One-day simulation extrapolated to years.
  - Turbulence modeled with Gaussian noise and low-frequency gusts.
- **Limitations**:
  - Overestimates stress in Normal and Stormy regimes.
  - Underestimates damage in Calm regime.
  - Lacks real-world wind distribution (e.g., Weibull) and blade geometry effects.
- **Future Improvements**:
  - Calibrate with IEC 61400-1 standards or blade material data.
  - Implement Weibull wind distribution and aerodynamic load models.
  - Add GUI for interactive parameter adjustment.

## File Structure
- `fatigue_load_estimator.py`: Main script for fatigue estimation and visualization.

## Running the Code
- Requires Python 3.13+, `numpy`, and `matplotlib`.
- Tested on Windows; compatible with macOS/Linux with proper setup.
- Run time: ~5-10 seconds on a standard laptop.

## For Siemens HR
This project demonstrates my skills in fatigue analysis and wind turbine engineering. The current model highlights areas for improvement, and I’m eager to refine it using Siemens’ advanced simulation tools or real-world data. Please explore the code and results—feedback is welcome!

## License
MIT License (see [LICENSE](../LICENSE) in the main `turbomachinery` repo, if applicable).

## Contact
For collaboration or questions, reach me at [vimalgnani@gmail.com](mailto:vimalgnani@gmail.com) or on [GitHub](https://github.com/vimal0athithan).