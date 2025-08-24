# Wind Farm Layout Optimization Tool

## Overview

This Python tool simulates wind farm layouts to **minimize wake losses**
and **maximize overall power output**. It implements **Jensen's wake
model** to capture wake effects between turbines and applies
**differential evolution optimization** to determine optimal turbine
placements within a defined farm area. The program produces interactive
plots for both the optimized layout and wake velocity profiles.

Developed as part of my turbomachinery portfolio, this project
highlights expertise in **renewable energy systems engineering**,
**numerical modeling**, and **Python scientific computing**.

**Key Features:** - **Wake Modeling**: Jensen's wake model estimates
reduced wind speeds at downstream turbines. - **Optimization**: SciPy's
differential evolution ensures turbines respect spacing constraints
while maximizing farm output. - **Interactive Visualizations**: -
Scatter plot of optimized turbine layout. - Contour plot of wind field
and wake profiles. - **Customizable Parameters**: Number of turbines,
farm size, wind speed, rotor diameter, wind direction, etc.

**Author**: Vimal Athithan\
**Date**: August 2025\
**GitHub**: [vimal0athithan](https://github.com/vimal0athithan)\
**Contact**: <vimalgnani@gmail.com>

------------------------------------------------------------------------

## Installation

1.  **Clone the Repository**

    ``` bash
    git clone https://github.com/vimal0athithan/turbomachinery.git
    cd turbomachinery/wind_farm_optimization
    ```

2.  **Set Up a Virtual Environment (Optional)**

    ``` bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    source venv/bin/activate  # Linux/macOS
    ```

3.  **Install Dependencies**

    ``` bash
    pip install numpy scipy matplotlib
    ```

------------------------------------------------------------------------

## Usage

1.  Run the optimization script:

    ``` bash
    python wind_farm_optimization.py
    ```

2.  **Outputs**:

    -   Console: Optimized total power output in MW.
    -   Plots:
        -   Optimized turbine layout.
        -   Wind velocity contour plot with wake deficits.

3.  **Customization**: Modify parameters in the script:

    -   `N`: Number of turbines (default: 9)
    -   `farm_size`: Farm side length in meters (default: 2000)
    -   `U0`: Free stream wind speed (default: 12 m/s)
    -   `wind_dir`: Wind direction in radians (default: 0.0, along
        x-axis)
    -   `min_dist`: Minimum spacing (default: 5 × rotor diameter)

------------------------------------------------------------------------

## Example Output

-   **Console**:

        Optimized total power: 35.47 MW

-   **Plots**:

    -   Optimized Layout: Scatter plot showing turbine positions within
        a 2000m × 2000m area.
    -   Wake Profiles: Contour plot showing wake zones behind turbines.

------------------------------------------------------------------------

## Limitations

-   Assumes uniform wind speed and direction.
-   Uses simplified Jensen's wake model (suitable for conceptual design,
    not full CFD).
-   Computational cost increases with large turbine counts.

------------------------------------------------------------------------

## Skills Showcased

-   **Numerical methods**: Wake modeling & vectorized computations\
-   **Optimization techniques**: Differential evolution for spatial
    layouts\
-   **Renewable energy engineering**: Wind farm design principles\
-   **Python programming**: NumPy, SciPy, and Matplotlib

------------------------------------------------------------------------

## License

This project is licensed under the MIT License (see
[LICENSE](../LICENSE)).

------------------------------------------------------------------------

## Contact

For collaboration or questions, please reach me at:\
📧 <vimalgnani@gmail.com>\
🔗 [GitHub](https://github.com/vimal0athithan)
