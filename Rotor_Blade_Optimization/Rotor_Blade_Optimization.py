# Rotor Blade Optimization (Simplified MDO)
# Description: Multi-objective optimization for a wind turbine rotor blade.
# Objectives: Maximize AEP, Minimize blade mass, Minimize fatigue loads.
# Techniques: Genetic Algorithm (DEAP for exploration) vs. Gradient-based (SciPy for exploitation via normalized weighted sum).
# Outcome: Visualize Pareto front trade-offs.
# Corrections: Fixed dynamic scaling in gradient obj with fixed norms; improved weighted sum for true multi-obj; tuned eval funcs per research insights.
# Research Insights: AEP via BEM proxy; mass via sectional integration proxy; fatigue via stress/frequency constraints proxy.

# Note: Requires DEAP (pip install deap), numpy, matplotlib, scipy.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.optimize import minimize

try:
    from deap import base, creator, tools, algorithms
except ImportError:
    print("DEAP library is required for Genetic Algorithm. Install it using: pip install deap")
    raise

# Design variable bounds (blade_length in m, max_chord in m, twist_angle in degrees)
LOW = [20.0, 1.0, 0.0]  # Lower bounds
UP = [50.0, 5.0, 20.0]  # Upper bounds
NDIM = 3  # Number of design variables

# Fixed normalization factors (based on typical ranges from eval func and literature)
NORM_AEP = 200.0
NORM_MASS = 5000.0
NORM_FATIGUE = 100.0

# Evaluation function (simplified models, tuned per papers: AEP ~ BEM proxy, mass ~ sectional, fatigue ~ root moment)
def evaluate(individual):
    length, chord, twist = individual
    # Annual Energy Production (MWh, maximize): Polynomial proxy for BEM, increases with length^2 and chord, modulated by twist
    AEP = 0.05 * length**2 * (1 + 0.15 * chord) * (1 + 0.08 * twist / 20.0)  # Tuned coefficients for realism
    # Blade Mass (kg, minimize): Proportional to length * avg chord (proxy for composite layup integration)
    mass = 40.0 * length * chord  # Reduced coeff to align with lit (e.g., ~20-30 ton blades)
    # Fatigue Load (arbitrary units, minimize): Proxy for DEL/root bending ~ length^3 / chord
    fatigue = 0.005 * length**3 / max(chord, 0.1)  # Tuned; in lit, often constrained via freq/stress
    return AEP, mass, fatigue

# Part 1: Genetic Algorithm (Exploration) using DEAP for multi-objective (NSGA-II)
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, -1.0))  # Max AEP, Min mass, Min fatigue
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("attr_length", random.uniform, LOW[0], UP[0])
toolbox.register("attr_chord", random.uniform, LOW[1], UP[1])
toolbox.register("attr_twist", random.uniform, LOW[2], UP[2])
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_length, toolbox.attr_chord, toolbox.attr_twist), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=LOW, up=UP, eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=LOW, up=UP, eta=20.0, indpb=1.0/NDIM)
toolbox.register("select", tools.selNSGA2)

def run_ga():
    pop = toolbox.population(n=200)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)
    
    algorithms.eaMuPlusLambda(pop, toolbox, mu=200, lambda_=200, cxpb=0.7, mutpb=0.3, ngen=100, 
                              stats=stats, halloffame=hof, verbose=True)
    
    return hof

# Part 2: Gradient-based (Exploitation) using SciPy with normalized weighted sum
# Generates Pareto points by varying normalized weights (w1 for -AEP, w2 for mass, w3 for fatigue; sum w=1)
def run_gradient(num_points=10):
    pareto_points = []
    bounds = list(zip(LOW, UP))
    x0 = [(l + u)/2 for l, u in bounds]
    
    # Generate random weights (Dirichlet dist for sum=1, >0)
    weights_list = np.random.dirichlet((1,1,1), num_points)  # [w_aep, w_mass, w_fatigue]
    
    for w in weights_list:
        def obj_weighted(x):
            AEP, mass, fatigue = evaluate(x)
            # Normalized weighted sum: min w_aep*(-AEP/norm) + w_mass*(mass/norm) + w_fatigue*(fatigue/norm)
            return w[0] * (-AEP / NORM_AEP) + w[1] * (mass / NORM_MASS) + w[2] * (fatigue / NORM_FATIGUE)
        
        res = minimize(obj_weighted, x0, bounds=bounds, method='SLSQP', tol=1e-6)
        if res.success:
            pareto_points.append(evaluate(res.x))
    
    return pareto_points

# Main execution
if __name__ == "__main__":
    # Run Genetic Algorithm
    print("Running Genetic Algorithm (NSGA-II)...")
    hof = run_ga()
    
    # Extract Pareto front from GA
    ga_aeps = [ind.fitness.values[0] for ind in hof]
    ga_masses = [ind.fitness.values[1] for ind in hof]
    ga_fatigues = [ind.fitness.values[2] for ind in hof]
    
    # Run Gradient-based for comparison
    print("\nRunning Gradient-based optimization (normalized weighted sum)...")
    grad_points = run_gradient(num_points=20)  # More points for better Pareto approx
    
    grad_aeps = [p[0] for p in grad_points]
    grad_masses = [p[1] for p in grad_points]
    grad_fatigues = [p[2] for p in grad_points]
    
    # Visualize Pareto front trade-offs (3D scatter)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(ga_aeps, ga_masses, ga_fatigues, c='b', marker='o', label='GA (NSGA-II) Pareto Front')
    ax.scatter(grad_aeps, grad_masses, grad_fatigues, c='r', marker='x', label='Gradient-based Points')
    ax.set_xlabel('Annual Energy Production (AEP) [Maximize]')
    ax.set_ylabel('Blade Mass [Minimize]')
    ax.set_zlabel('Fatigue Loads [Minimize]')
    ax.set_title('Pareto Front Trade-offs: AEP vs. Mass vs. Fatigue')
    ax.legend()
    plt.show()
    
    # Save Pareto front data to CSV
    import pandas as pd
    ga_df = pd.DataFrame({'AEP': ga_aeps, 'Mass': ga_masses, 'Fatigue': ga_fatigues, 'Method': 'GA'})
    grad_df = pd.DataFrame({'AEP': grad_aeps, 'Mass': grad_masses, 'Fatigue': grad_fatigues, 'Method': 'Gradient'})
    df = pd.concat([ga_df, grad_df])
    df.to_csv('pareto_front.csv', index=False)
    print("Pareto front data saved to 'pareto_front.csv'")