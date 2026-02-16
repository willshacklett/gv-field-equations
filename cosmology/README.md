# Cosmology Module — GV

This folder contains the first quantitative tests of the God Variable (GV)
in a cosmological setting.

It currently includes:

- `flrw_embedding.md` — analytical derivation of w(z)
- `solve_wz.py` — numerical toy solver for w(z)
- `inflation.md` — slow-roll framework for n_s and r

This is not a full Boltzmann solver.  
It is a controlled, minimal dynamical model.

---

# 1. Dark Energy: w(z) Solver

## Model

We treat GV as a canonical scalar field with potential:

\[
V(GV) = V_0 e^{-\lambda GV}
\]

Flat universe with matter + radiation + GV.

Friedmann:
\[
H^2 = \frac{1}{3}\rho_{total}
\]

Energy density:
\[
\rho_{GV} = \frac{1}{2}\dot{GV}^2 + V(GV)
\]

Equation of state:
\[
w(z) = \frac{p_{GV}}{\rho_{GV}}
\]

---

## Run the Solver

From repo root:

```bash
python3 cosmology/solve_wz.py
