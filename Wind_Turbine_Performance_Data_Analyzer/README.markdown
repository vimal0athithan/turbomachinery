# Wind Turbine Performance Data Analyzer

## Overview
This Python script analyzes SCADA (Supervisory Control and Data Acquisition) data for wind turbines, processing metrics such as power output, wind speed, rotor RPM, and pitch angle. Part of my turbomachinery portfolio, this project complements other work like [Rotor Blade Optimization](https://github.com/vimal0athithan/turbomachinery/rotor-blade-optimization) by demonstrating data processing and performance assessment skills. The tool processes real-world SCADA data (e.g., the provided `T1.csv` file) to generate power curves, compare measured vs. theoretical power coefficients (Cp), and visualize efficiency losses due to wind speed variability.

**Key Features:**
- Data cleaning and outlier removal using z-score within wind speed bins.
- Calculation of power curves (measured and theoretical).
- Comparison of measured vs. theoretical power coefficient (Cp).
- Visualization of efficiency losses due to wind speed variability.
- Output includes plots (`cp_comparison.png`, `power_curves_with_variability.png`, `efficiency_losses.png`) and console summaries.

**Author**: Vimal Athithan  
**Date**: August 25, 2025, 12:00 AM IST  
**GitHub**: [vimal0athithan](https://github.com/vimal0athithan)  
**Contact**: [vimalgnani@gmail.com](mailto:vimalgnani@gmail.com)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vimal0athithan/turbomachinery.git
   cd turbomachinery/Wind_Turbine_Performance_Data_Analyzer
   ```
2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install pandas numpy matplotlib scipy
   ```
4. **Verify SCADA Data**:
   - The script uses the included `T1.csv` file (located in the `Wind_Turbine_Performance_Data_Analyzer` directory).
   - Alternatively, replace `T1.csv` with your own SCADA data (CSV format) with columns such as `Date/Time`, `LV ActivePower (kW)`, `Wind Speed (m/s)`, `Theoretical_Power_Curve (KWh)`, `Wind Direction (°)`, and update column names in the script if needed.

## Usage
1. Ensure Python 3.6+ and dependencies (`pandas`, `numpy`, `matplotlib`, `scipy`) are installed.
2. Verify that `T1.csv` is in the `Wind_Turbine_Performance_Data_Analyzer` directory. The script expects columns: `Date/Time`, `LV ActivePower (kW)`, `Wind Speed (m/s)`, `Theoretical_Power_Curve (KWh)`, `Wind Direction (°)` (adjust column renaming in the script if your data differs).
3. Run the script:
   - From `C:\turbomachinery`:
     ```powershell
     python Wind_Turbine_Performance_Data_Analyzer\Wind_Turbine_Performance_Data_Analyzer.py
     ```
   - Or navigate to the directory first:
     ```powershell
     cd Wind_Turbine_Performance_Data_Analyzer
     python Wind_Turbine_Performance_Data_Analyzer.py
     ```
4. **Output**:
   - Console displays the number of cleaned data rows and summary statistics of efficiency losses.
   - Plots saved as:
     - `cp_comparison.png`: Measured vs. theoretical Cp curves.
     - `power_curves_with_variability.png`: Power curves with variability shading.
     - `efficiency_losses.png`: Bar plot of average power losses per wind speed bin.
5. **Troubleshooting**:
   - **FileNotFoundError**: If you see `FileNotFoundError`, ensure `T1.csv` is in the `Wind_Turbine_Performance_Data_Analyzer` directory and the path in the script (`data_file`) matches.
   - Modify column names in the script (line `df.columns = [...]`) if your CSV has different headers.
6. **Customize**:
   - Adjust `cut_in` (3 m/s) and `cut_out` (25 m/s) for specific turbine models.
   - Update `rotor_diameter` (default 117 m) and `rho` (1.225 kg/m³) for turbine-specific calculations.
   - Change bin size (default 0.5 m/s) or z-score threshold (default 3) for outlier detection.

## Simulation Results 
The script successfully processes the `T1.csv` dataset to:
- Clean data by removing missing values, invalid entries (negative power/speed), and outliers using z-score within wind speed bins.
- Calculate power curves by averaging power output per wind speed bin, with variability shown as standard deviation shading.
- Compute measured and theoretical Cp, capped at the Betz limit (0.593), for performance comparison.
- Visualize efficiency losses (theoretical minus measured power) as a bar plot per wind speed bin.
- **Interpretation**: The plots highlight performance deviations due to wind speed variability, mechanical losses, or control strategies, providing valuable insights for turbine diagnostics and optimization.

## Technical Details
- **Data Assumptions**:
  - Input: CSV file (`T1.csv`) with SCADA data.
  - Turbine specs: 117 m rotor diameter, 3.6 MW nominal power (adjustable).
  - Air density: 1.225 kg/m³ (standard sea-level value).
  - Theoretical power curve: Assumed to be in kW (if in KWh, represents 10-min energy; adjust by multiplying by 6 for power in kW).
- **Processing**:
  - Cleaning: Drops NaN, filters negative values, removes outliers via z-score.
  - Binning: Groups wind speeds in 0.5 m/s bins for stable averaging.
  - Cp Calculation: Measured Cp = power / (0.5 * ρ * A * v³), theoretical Cp uses provided theoretical power.
- **Visualizations**:
  - Cp curves (line plot).
  - Power curves with variability (line plot with shaded standard deviation).
  - Efficiency losses (bar plot).
- **Limitations**:
  - Assumes simplified turbine specs (e.g., fixed rotor diameter).
  - Theoretical power curve provided in data; no BEM simulation included (see my [Rotor Blade Optimization](https://github.com/vimal0athithan/turbomachinery/rotor-blade-optimization) for BEM-inspired models).
  - Outlier detection may need tuning for specific datasets.
- **Future Improvements**:
  - Integrate Weibull wind distribution for site-specific analysis.
  - Add rotor RPM and pitch angle analysis for control strategy insights.
  - Incorporate advanced aeroelastic tools (e.g., FAST).
  - Enhance with statistical tests (e.g., ANOVA) for performance comparisons.

## File Structure
- `Wind_Turbine_Performance_Data_Analyzer.py`: Main script for data processing and visualization.
- `T1.csv`: Input SCADA data (CSV file provided).
- `cp_comparison.png`, `power_curves_with_variability.png`, `efficiency_losses.png`: Output plots (generated after running).

## Running the Code
- Requires Python 3.6+, `pandas`, `numpy`, `matplotlib`, `scipy`.
- Tested on Windows; compatible with macOS/Linux with proper setup.
- Run time: ~10-20 seconds on a standard laptop (depends on dataset size).

## Research Context
This project draws from wind turbine performance literature:
- Data cleaning inspired by "Exploratory Analysis of SCADA Data from Wind Turbines Using the K-Means Clustering Algorithm."
- Power curve and Cp analysis based on "Performance Assessment of a Wind Turbine Using SCADA based Gaussian Process Model."
- Methods align with my [Rotor Blade Optimization](https://github.com/vimal0athithan/turbomachinery/rotor-blade-optimization) project, extending data-driven insights to performance analysis.

## For Siemens Review
This project showcases my expertise in Python programming (`pandas`, `matplotlib`), engineering data validation, and renewable energy performance assessment. It complements my turbomachinery portfolio by focusing on data-driven turbine diagnostics, now successfully operational with the `T1.csv` dataset. Feedback is greatly appreciated!

## License
MIT License (see [LICENSE](../LICENSE) in the main `turbomachinery` repo, if applicable).

## Contact
For collaboration or questions, reach me at [vimalgnani@gmail.com](mailto:vimalgnani@gmail.com) or on [GitHub](https://github.com/vimal0athithan).