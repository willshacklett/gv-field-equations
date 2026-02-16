# Strong CP in GV — θ as a Relaxing Strain Coordinate (No Axion)

## Thesis
In the GV framework, the QCD vacuum angle **θ** is not an arbitrary parameter requiring a new particle (axion) to set it to ~0.
Instead, **θ behaves like a strain/topology coordinate** in the constraint field: nonzero θ corresponds to higher constraint tension / higher effective free energy.

The system relaxes dynamically toward the **minimum-energy attractor** at θ → 0.

---

## Minimal dynamical model

Let the effective free energy (coarse-grained) be:

F(θ; GV, T) = A(GV,T) * (1 - cos θ)

Then the relaxation dynamics are:

dθ/dt = -Γ(GV,T) * ∂F/∂θ
      = -Γ(GV,T) * A(GV,T) * sin θ

Small-angle limit (|θ| << 1):

dθ/dt ≈ -k(GV,T) * θ
k(GV,T) = Γ(GV,T) * A(GV,T)

Solution:
θ(t) = θ0 * exp[-k(GV,T) t]

---

## Observable consequences

### 1) nEDM bound as a direct constraint on GV–QCD coupling
The neutron EDM scales with θ_eff:

d_n ∝ θ_eff

Since θ_eff in this model is dynamical:
θ_eff = θ(t_freeze)  (or residual after relaxation)

So experimental bounds on d_n constrain:
- k(GV,T) (relaxation rate)
- the coupling/normalization A(GV,T)

### 2) Early-universe CP bias without new particles
During eras where GV is rapidly changing (e.g., reheating / phase transitions), ∂t GV can modulate k(GV,T),
producing transient CP-odd bias and feeding into baryogenesis channels.

---

## What to test next (quantitative program)

1) Specify A(GV,T) and Γ(GV,T) in a GV-modified EFT.
2) Evolve θ(t) across QCD transition temperatures.
3) Compute implied θ_eff at low energy and compare to nEDM limits.
4) Feed θ(t) into BAU toy models (sphalerons/leptogenesis) for order-of-magnitude viability.

