# Wind Turbine Acoustic Analysis

## Overview
This Python tool estimates sound pressure levels (SPL) for wind turbine blades using a simplified Brooks-Pope-Marcolini (BPM) aeroacoustic model, focusing on trailing-edge noise. It takes inputs like blade tip speed, chord length, and wind speed to compute the SPL spectrum and overall SPL, with comparisons for different blade designs. This project demonstrates skills in engineering acoustics, numerical modeling, and Python programming.

**Key Features:**
- Inputs: Blade tip speed, chord length, wind speed.
- Outputs: SPL spectrum (10 Hz to 10 kHz) and overall SPL in dB.
- Visualization: Plots comparing SPL spectra for multiple blade designs.
- Skills Showcased: Aeroacoustics, numerical analysis, Python (NumPy, Matplotlib).

**Author**: [Vimal Athithan G]  
**Date**: August 2025  
**Contact**: [vimalgnani@gmail.com]

## Installation
1. **Clone the Repository** (if part of the `turbomachinery` portfolio):
   ```
   git clone https://github.com/vimal0athithan/turbomachinery.git
   cd turbomachinery/wind-turbine-analysis
   ```
   For a standalone repo, use:
   ```
   git clone https://github.com/vimal0athithan/wind-turbine-acoustic-analysis.git
   cd wind-turbine-acoustic-analysis
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
   python wind_turbine_acoustic_analysis.py
   ```
3. **Output**:
   - Console displays overall SPL for two example blade designs (baseline: 70 m/s tip speed, 2 m chord; alternative: 80 m/s tip speed, 1.5 m chord).
   - A Matplotlib plot compares SPL spectra across frequencies.
   - A comparison table summarizes inputs and results.
4. **Customize**:
   - Edit the `if __name__ == "__main__":` section in `wind_turbine_acoustic_analysis.py` to modify `tip_speed`, `chord`, and `wind_speed` for custom blade designs.

**Example Output**:
```
Design 1 - Overall SPL: 85.23 dB
Design 2 - Overall SPL: 88.45 dB

Comparison Table:
| Design | Tip Speed (m/s) | Chord (m) | Wind Speed (m/s) | Overall SPL (dB) |
|--------|-----------------|-----------|------------------|------------------|
| 1      | 70.0            | 2.0       | 10.0             | 85.23            |
| 2      | 80.0            | 1.5       | 10.0             | 88.45            |
```

## Technical Details
- **Model**: Simplified BPM model for airfoil self-noise, assuming zero angle of attack, tripped boundary layer, and trailing-edge noise dominance.
- **Assumptions**:
  - Observer distance: 100 m.
  - Blade span: 50 m.
  - Speed of sound: 343 m/s.
  - Kinematic viscosity: 1.5e-5 m²/s.
- **Limitations**:
  - Basic model; does not account for turbine arrays, atmospheric effects, or complex blade geometries.
  - Suitable for initial design estimates, not full-scale production analysis.
- **Future Improvements**:
  - Add GUI (e.g., Tkinter) for user-friendly input.
  - Integrate with CFD tools or Siemens’ simulation software for enhanced accuracy.
  - Support multiple blades or variable angles of attack.

## File Structure
- `wind_turbine_acoustic_analysis.py`: Main script for SPL estimation and visualization.
- (Optional) Add output files (e.g., `spl_plot.png`) to the folder and link in README: `![SPL Plot](./spl_plot.png)`.

## Running the Code
- Requires Python 3.13+, `numpy`, and `matplotlib`.
- Tested on Windows; compatible with macOS/Linux with proper dependency setup.
- Example run time: ~1 second on a standard laptop for default parameters.

## For Siemens HR
This project showcases my expertise in aeroacoustic modeling for wind turbines, aligning with Siemens’ focus on renewable energy. The code is modular, well-documented, and extensible for integration with advanced turbine design tools. I’m eager to discuss how my skills can contribute to Siemens’s wind energy initiatives.

## License
MIT License (see [LICENSE](../LICENSE) in the main `turbomachinery` repo, if applicable).

## Contact
For questions or collaboration, reach me at [vimalgnani@gmail.com or https://www.linkedin.com/in/vimal-athithan-g-202460304/]. Fork or contribute to enhance the tool!
