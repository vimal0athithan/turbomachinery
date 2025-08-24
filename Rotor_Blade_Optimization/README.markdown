# Rotor Blade Optimization (Simplified MDO)

## Overview
This Python script implements a multi-objective optimization for a simplified wind turbine rotor blade, developed as part of my turbomachinery portfolio. The project optimizes three objectives:
- **Maximize Annual Energy Production (AEP)**: Enhances energy capture efficiency.
- **Minimize Blade Mass**: Reduces material costs and structural loads.
- **Minimize Fatigue Loads**: Improves blade longevity by reducing cyclic stresses.

The optimization combines two approaches:
- **Genetic Algorithm (GA)**: Uses the DEAP library with NSGA-II for global exploration of the Pareto front.
- **Gradient-based Method**: Employs SciPy's SLSQP with a normalized weighted sum for local exploitation.

The output includes **Figure 1**, a 3D scatter plot visualizing the Pareto front (AEP vs. Mass vs. Fatigue), and a CSV file with results, showcasing trade-offs between objectives. This project demonstrates skills in multi-disciplinary optimization (MDO), Python programming, and wind turbine design.

**Key Features:**
- Multi-objective optimization with NSGA-II and SLSQP.
- Simplified models for AEP, mass, and fatigue, inspired by Blade Element Momentum (BEM) and structural analysis.
- 3D Pareto front visualization using Matplotlib (**Figure 1**).
- Data export to CSV for further analysis.

**Author**: Vimal Athithan  
**Date**: August 24, 2025, 11:35 PM IST  
**GitHub**: [vimal0athithan](https://github.com/vimal0athithan)  
**Contact**: [vimalgnani@gmail.com](mailto:vimalgnani@gmail.com)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vimal0athithan/turbomachinery.git
   cd turbomachinery/rotor-blade-optimization
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
   pip install numpy matplotlib scipy deap pandas
   ```

## Usage
1. Ensure Python 3.6+ and dependencies (`numpy`, `matplotlib`, `scipy`, `deap`, `pandas`) are installed.
2. Run the script:
   ```bash
   python rotor_blade_optimization.py
   ```
3. **Output**:
   - Console displays progress for GA (NSGA-II) and gradient-based optimization.
   - **Figure 1**: A 3D Matplotlib scatter plot shows the Pareto front, comparing GA (blue circles) and gradient-based (red crosses) results.
   - Results are saved to `pareto_front.csv` with columns: `AEP`, `Mass`, `Fatigue`, and `Method` (GA or Gradient).
4. **Customize**:
   - Modify `LOW` and `UP` in the script to adjust design variable bounds (blade length, chord, twist).
   - Tune evaluation function coefficients (e.g., AEP, mass, fatigue) for specific turbine models.
   - Adjust GA parameters (`n=200`, `ngen=100`) or gradient points (`num_points=20`) for different trade-off resolutions.

## Output Structure
- **`pareto_front.csv`**:
  - **Description**: Contains the Pareto front data points from both GA (NSGA-II) and gradient-based (SLSQP) optimizations.
  - **Columns**:
    - `AEP`: Annual Energy Production (MWh, maximized).
    - `Mass`: Blade mass (kg, minimized).
    - `Fatigue`: Fatigue loads (arbitrary units, minimized).
    - `Method`: Optimization method (`GA` or `Gradient`).
  - **Usage**: Use for post-processing, e.g., filtering trade-offs or comparing with other designs.
- **Figure 1 (3D Pareto Front Plot)**:
  - **Description**: A 3D scatter plot visualizing the trade-offs between AEP, mass, and fatigue.
  - **Details**:
    - Blue circles: Solutions from GA (NSGA-II), showing global exploration.
    - Red crosses: Solutions from gradient-based method (SLSQP), showing local refinement.
    - Axes: AEP (x, maximize), Mass (y, minimize), Fatigue (z, minimize).
  - **Purpose**: Illustrates the trade-off surface, where higher AEP typically increases mass and fatigue.

## Simulation Results (August 24, 2025)
The script generates a Pareto front with trade-offs between AEP, mass, and fatigue:
- **Genetic Algorithm (NSGA-II)**: Produces a diverse Pareto front, capturing global trade-offs across the design space.
- **Gradient-based (SLSQP)**: Generates additional points via normalized weighted sum, focusing on local optima.
- **Interpretation**: **Figure 1** shows higher AEP correlates with increased mass and fatigue, with GA providing broader exploration and SLSQP refining specific regions.
- **Note**: Results are based on simplified models (polynomial AEP, proportional mass, bending moment fatigue proxy). Real-world calibration with BEM (e.g., QBlade) or aeroelastic tools (e.g., FAST) is recommended.

## Technical Details
- **Design Variables**:
  - `blade_length`: 20–50 meters
  - `max_chord`: 1–5 meters
  - `twist_angle`: 0–20 degrees
- **Objective Functions**:
  - **AEP**: Polynomial proxy for BEM, increasing with length² and chord, modulated by twist.
  - **Mass**: Proportional to length × chord, approximating composite layup integration.
  - **Fatigue**: Proportional to length³/chord, proxy for root bending moment and Damage Equivalent Loads (DEL).
- **Optimization**:
  - **GA**: NSGA-II with 200 individuals, 100 generations, crossover/mutation probabilities of 0.7/0.3.
  - **Gradient**: SLSQP with 20 points, using Dirichlet-distributed weights for normalized weighted sum (normalization factors: AEP ~200, Mass ~5000, Fatigue ~100).
- **Assumptions**:
  - Simplified models for computational efficiency.
  - Fatigue as a direct objective (in practice, often a constraint via stress/frequency limits).
- **Limitations**:
  - Lacks full BEM or aeroelastic simulations (e.g., FAST, PreComp).
  - Simplified fatigue model omits S-N curves or rainflow counting (see my [Fatigue Load Estimator](https://github.com/vimal0athithan/turbomachinery/fatigue-load-estimator)).
  - Limited to three design variables; real designs use spline-based chord/twist distributions.
- **Future Improvements**:
  - Integrate BEM (e.g., QBlade) for accurate AEP.
  - Add constraints (stress, deflection, natural frequency) per IEC 61400-1.
  - Implement hybrid GA-gradient optimization for faster convergence.
  - Incorporate Weibull wind distribution or real turbine data.

## File Structure
- `rotor_blade_optimization.py`: Main script for optimization and visualization.
- `pareto_front.csv`: Output file with Pareto front data (generated after running).

## Running the Code
- Requires Python 3.6+, `numpy`, `matplotlib`, `scipy`, `deap`, `pandas`.
- Tested on Windows; compatible with macOS/Linux with proper setup.
- Run time: ~1-2 minutes on a standard laptop (due to GA's 100 generations).

## Research Context
This project draws from wind turbine optimization literature:
- AEP modeled as a BEM proxy, inspired by tools like WT-Perf.
- Mass and fatigue models approximate sectional integration and aeroelastic constraints (e.g., Co-Blade, FAST).
- NSGA-II and weighted sum methods are standard for multi-objective blade design.
- Future extensions could include spline-based parameterization or stress constraints, as seen in advanced MDO frameworks.

## For Reviewers
This project showcases my expertise in multi-objective optimization, Python programming, and wind turbine engineering principles. The combination of global (GA) and local (gradient) optimization methods demonstrates versatility in tackling complex design problems. I’m eager to enhance this tool with advanced simulation tools or real turbine data. Please review the code, **Figure 1**, and results—feedback is greatly appreciated!

## License
MIT License (see [LICENSE](../LICENSE) in the main `turbomachinery` repo, if applicable).

## Contact
For collaboration or questions, reach me at [vimalgnani@gmail.com](mailto:vimalgnani@gmail.com) or on [GitHub](https://github.com/vimal0athithan).
