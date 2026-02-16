# Effective Action for GV (v0 → v1 bridge)

## 1. Purpose

To move GV from a descriptive scalar into a predictive framework, we need an
effective action that:

1) generates the GV evolution equation (EOM)  
2) defines how GV contributes to energy density and pressure  
3) specifies how GV couples (or decouples) across scales

This is the “engine room” document.

---

## 2. Minimal Covariant Action (Scalar + Gravity)

We start with a standard covariant scalar-field structure:

\[
S = \int d^4x \sqrt{-g}\left[
\frac{M_P^2}{2}R
-\frac{1}{2}K(GV)\,g^{\mu\nu}\partial_\mu GV\,\partial_\nu GV
- V(GV)
+ \mathcal{L}_{m}(g,\psi;GV)
\right]
\]

Where:

- \(M_P\) is the reduced Planck mass
- \(K(GV)\) is a positive kinetic prefactor (“constraint stiffness”)
- \(V(GV)\) is an effective constraint potential
- \(\mathcal{L}_m\) may include GV-dependent couplings (screening/decoupling)

This is not “new force” language; it’s a minimal consistency wrapper.

---

## 3. Equation of Motion (EOM)

Varying w.r.t. \(GV\) yields:

\[
\nabla_\mu\left(K(GV)\nabla^\mu GV\right) - \frac{1}{2}K'(GV)(\nabla GV)^2 + V'(GV)
= \frac{\partial \mathcal{L}_{m}}{\partial GV}
\]

Interpretation:
- diffusion/relaxation comes from the kinetic term
- stability regimes come from \(V(GV)\)
- matter backreaction appears through \(\partial \mathcal{L}_m/\partial GV\)

For a simple “no direct matter coupling” starting point:
\[
\frac{\partial \mathcal{L}_{m}}{\partial GV}=0
\]

---

## 4. Energy Density and Pressure (Cosmology Ready)

In FLRW (homogeneous GV = \(GV(t)\)):

Energy density:
\[
\rho_{GV}=\frac{1}{2}K(GV)\dot{GV}^2 + V(GV)
\]

Pressure:
\[
p_{GV}=\frac{1}{2}K(GV)\dot{GV}^2 - V(GV)
\]

Equation of state:
\[
w_{GV}=\frac{p_{GV}}{\rho_{GV}}
= \frac{\frac{1}{2}K(GV)\dot{GV}^2 - V(GV)}
{\frac{1}{2}K(GV)\dot{GV}^2 + V(GV)}
\]

So:
- inflation / dark energy-like behavior happens when \(V \gg \dot{GV}^2\) → \(w\approx -1\)
- “matter-like” behavior happens when kinetic dominates → \(w\approx +1\) (stiff)
- intermediate regimes can mimic \(w(z)\) deviations

---

## 5. Regimes (How GV Matches the Story)

### (A) Supercritical (Inflation-like)
Define a regime where GV temporarily sits high on a potential plateau:

\[
V(GV)\approx V_0,\quad \dot{GV}^2 \ll V_0
\Rightarrow w\approx -1
\]

Inflation ends when the field rolls/relaxes:
- \(V(GV)\) steepens
- kinetic rises
- energy transfers into matter/radiation (“reheating” coupling)

### (B) Metastable Domains (Dark Matter-like)
Spatial domain structure occurs if \(V(GV)\) permits multiple local minima or
topological defects.

Metastable gradient “lumps” can gravitate via stress-energy without requiring
new particles.

### (C) Undercritical Tail (Dark Energy-like)
Late-time acceleration corresponds to slow residual relaxation:

\[
\dot{GV}\to 0,\quad V(GV)\to V_\infty
\Rightarrow w\to -1
\]

---

## 6. Decoupling / Cross-Scale Suppression (Hierarchy Hook)

We encode “constraint-decoupling” through GV-dependent matter couplings:

Example sketch:
\[
\mathcal{L}_m \supset -\frac{1}{4}Z_i(GV)F_i^{\mu\nu}F_{i\mu\nu}
\]

or effective loop suppression:
\[
\delta m_H^2 \sim \frac{\Lambda^2}{16\pi^2}\,\Sigma(GV)
\quad\text{with}\quad \Sigma'(GV)<0
\]

Meaning:
- large GV reduces sensitivity to UV scales
- fine-tuning becomes “bounded coupling,” not magic cancellation

---

## 7. Minimal v1 Choice (We must choose something)

To become predictive, we pick explicit functional forms.

### Candidate A: Exponential tail (nice for late-time)
\[
V(GV)=V_0\left(1-e^{-\lambda GV}\right)
\]

### Candidate B: Plateau + roll (inflation-friendly)
\[
V(GV)=V_0\left(1-\tanh(\lambda(GV-GV_c))\right)
\]

### Candidate C: Double-well (domains / metastability)
\[
V(GV)=\frac{\lambda}{4}(GV^2-v^2)^2
\]

And simplest kinetic prefactor:
\[
K(GV)=1
\]
(or mild running: \(K(GV)=1+\kappa GV^2\))

---

## 8. What This Enables Next

Once \(K(GV)\) and \(V(GV)\) are chosen, we can derive:

- background evolution \(GV(t)\)
- Hubble history \(H(z)\)
- equation of state \(w(z)\)
- inflation observables \(n_s, r, f_{NL}\)
- stability (no-ghost, no gradient-instability conditions)

This document is the hinge.
Everything else in the repo becomes derivable from it.

---

## 9. Status

This is an **effective field theory (EFT) scaffold**, not a claim of proof.

Validation requires:
- explicit parameter choices
- consistency checks
- fits to cosmological datasets
- comparison to established limits (CMB, BAO, SN Ia, LHC, etc.)
