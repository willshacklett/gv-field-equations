# FLRW Embedding of GV — Dark Energy Sector (w(z))

## 1. Setup

We embed GV into standard flat FLRW cosmology:

Metric:
\[
ds^2 = -dt^2 + a(t)^2 d\vec{x}^2
\]

Friedmann equation:
\[
H^2 = \frac{8\pi G}{3}(\rho_m + \rho_r + \rho_{GV})
\]

GV energy density:
\[
\rho_{GV} = \frac{1}{2}\dot{GV}^2 + V(GV)
\]

Pressure:
\[
p_{GV} = \frac{1}{2}\dot{GV}^2 - V(GV)
\]

Equation of state:
\[
w(z) = \frac{p_{GV}}{\rho_{GV}}
\]

---

## 2. Choose a Minimal Late-Time Potential

To model dark energy, we want:

- Slow-roll at late times
- Stable asymptotic value
- Small deviation from Λ

We choose an exponential tail:

\[
V(GV) = V_0 e^{-\lambda GV}
\]

Assume canonical kinetic term:
\[
K(GV) = 1
\]

---

## 3. Background Field Equation

In FLRW:

\[
\ddot{GV} + 3H\dot{GV} + V'(GV) = 0
\]

For the exponential potential:

\[
V'(GV) = -\lambda V_0 e^{-\lambda GV}
\]

So:

\[
\ddot{GV} + 3H\dot{GV} - \lambda V(GV) = 0
\]

---

## 4. Late-Time Slow-Roll Approximation

If:

\[
\dot{GV}^2 \ll V(GV)
\]

then:

\[
w(z) \approx -1 + \frac{\dot{GV}^2}{V(GV)}
\]

Under slow roll:

\[
3H\dot{GV} \approx \lambda V(GV)
\]

So:

\[
\dot{GV} \approx \frac{\lambda V}{3H}
\]

Plug into w:

\[
w(z) \approx -1 + \frac{\lambda^2 V(GV)}{9H^2}
\]

Since:

\[
H^2 \approx \frac{8\pi G}{3}V(GV)
\]

we get:

\[
w(z) \approx -1 + \frac{\lambda^2}{24\pi G}
\]

---

## 5. Interpretation

Key result:

\[
w \approx -1 + \epsilon
\]

Where:

\[
\epsilon = \frac{\lambda^2}{24\pi G}
\]

So:

- Small λ → w extremely close to -1 (ΛCDM-like)
- Nonzero λ → small positive deviation
- Testable against DESI / Euclid / SN data

---

## 6. Observational Constraint Mapping

Planck constraint:

\[
w = -1 \pm 0.03
\]

Implies:

\[
\lambda^2 < 24\pi G \times 0.03
\]

Thus λ must be small in Planck units.

This becomes directly testable.

---

## 7. Next Step: Numerical Integration

To fully specify w(z):

1. Integrate coupled system:
   - Friedmann equation
   - GV evolution equation

2. Fit parameters:
   - λ
   - V₀

3. Compare:
   - H(z)
   - Structure growth
   - CMB distance ladder

---

## 8. Why This Matters

This shows:

GV dark energy is not hand-waving.

It produces:

- An equation of state
- A deviation parameter
- A direct observable

Dark energy becomes a residual slow constraint relaxation,
not a bare cosmological constant.

---

Status: v1 working dark-energy sector.
