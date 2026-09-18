# Paradigm 3: Computational Simulation & Physical Modeling

Applicable Domains: Physics, Chemistry, Materials Science, Chemical Engineering, Biophysics, Systems Biology.

---

## 1. Simulation Classes

### A. Deterministic Differential Equations (ODE / PDE)
- **Kinetics & Dynamics**: Chemical reaction networks, enzyme kinetics (Michaelis-Menten), orbital mechanics, heat transfer.
- **Stiffness & Solvers**:
  - Non-stiff systems: Runge-Kutta 4th/5th order (Dormand-Prince, `RK45`).
  - Stiff systems (reaction kinetics with disparate timescales): Implicit multi-step (`Radau`, `BDF`, `Rosenbrock`).
- Tools: Julia (`DifferentialEquations.jl` - gold standard), Python (`scipy.integrate.solve_ivp`).

### B. Stochastic Simulation & Monte Carlo
- Markov Chain Monte Carlo (MCMC), Gillespie stochastic simulation algorithm (chemical master equation), statistical mechanics.
- **Diagnostics**:
  - Autocorrelation time of Markov chains.
  - Gelman-Rubin diagnostic ($\hat{R} < 1.05$).
  - Effective Sample Size (ESS).

### C. Molecular Dynamics & Structural Modeling
- Force fields: AMBER, CHARMM, GROMOS, OPLS.
- Trajectory analysis: Root-Mean-Square Deviation (RMSD), Root-Mean-Square Fluctuation (RMSF), Radius of Gyration ($R_g$), Hydrogen bond dynamics.
- Tools: Python (`MDAnalysis`, `MDTraj`, `RDKit`), OpenMM, GROMACS CLI.

---

## 2. Computational Verification & Validation (V&V)
- **Conservation Laws**: Check conservation of energy, mass, or momentum across timesteps.
- **Convergence Rate Testing**: Double grid resolution or halve time step ($\Delta t / 2$) and verify convergence order against theoretical discretization error $\mathcal{O}(\Delta t^p)$.
