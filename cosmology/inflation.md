# GV Inflation (v1): Slow-Roll Observables (n_s, r)

## 1. Goal

We want a GV-driven early-universe phase that:

- produces quasi-de Sitter expansion (inflation)
- ends naturally via relaxation / roll-down
- predicts observable inflation parameters:
  - scalar tilt n_s
  - tensor-to-scalar ratio r
  - (optionally) running and non-Gaussianity

We treat GV as a canonical scalar field in the simplest EFT scaffold.

---

## 2. Slow-Roll Definitions

Potential slow-roll parameters:

\[
\epsilon_V = \frac{M_P^2}{2}\left(\frac{V'}{V}\right)^2
\qquad
\eta_V = M_P^2\left(\frac{V''}{V}\right)
\]

Inflation occurs if:

\[
\epsilon_V \ll 1,\quad |\eta_V| \ll 1
\]

Observables (leading order):

\[
n_s \approx 1 - 6\epsilon_V + 2\eta_V
\qquad
r \approx 16\epsilon_V
\]

Number of e-folds:

\[
N \approx \frac{1}{M_P^2}\int_{GV_{\rm end}}^{GV_*}\frac{V}{V'}\,dGV
\]

---

## 3. Choose a GV Inflation Potential (Pick One)

### Option A (Plateau / “safe” inflation form)
A clean plateau that naturally gives small r:

\[
V(GV)=V_0\left(1-\tanh(\lambda(GV-GV_c))\right)
\]

### Option B (Hilltop / metastable exit)
\[
V(GV)=V_0\left(1-\left(\frac{GV}{\mu}\right)^p\right)
\]

### Option C (Exponential / power-law inflation)
\[
V(GV)=V_0 e^{-\lambda GV}
\]
Note: pure exponential often gives too-large r unless tuned; better for late-time DE than inflation.

---

## 4. Workhorse Example: Hilltop (p=2)

Take:

\[
V(GV)=V_0\left(1-\frac{GV^2}{\mu^2}\right)
\]

Then:

\[
V' = -2V_0\frac{GV}{\mu^2}
\qquad
V'' = -2V_0\frac{1}{\mu^2}
\]

Compute slow-roll:

\[
\epsilon_V = \frac{M_P^2}{2}\left(\frac{-2GV/\mu^2}{1-GV^2/\mu^2}\right)^2
\]

\[
\eta_V = M_P^2\left(\frac{-2/\mu^2}{1-GV^2/\mu^2}\right)
\]

End of inflation is defined by:

\[
\epsilon_V(GV_{\rm end})=1
\]

Field value at horizon crossing GV_* comes from N:

\[
N \approx \frac{1}{M_P^2}\int_{GV_{\rm end}}^{GV_*}\frac{V}{V'}\,dGV
\]

Once GV_* is known:

\[
n_s \approx 1 - 6\epsilon_V(GV_*) + 2\eta_V(GV_*)
\]

\[
r \approx 16\epsilon_V(GV_*)
\]

---

## 5. GV Interpretation

Inflation corresponds to a supercritical GV regime:

- GV sits in a high “constraint potential”
- expansion is driven by V(GV) dominance
- exit occurs via gradient relaxation / roll-down
- reheating can be modeled via coupling terms added later:
  \[
  \mathcal{L}_{int}(GV,\psi)
  \]

This supports the narrative:
Inflation is not an extra inflaton species — it is a GV regime.

---

## 6. Next Deliverable

Create a matching solver (like w(z) solver) to compute:

- GV(t), H(t)
- N, epsilon, eta
- n_s, r for chosen potential

Then compare to Planck constraints.

Status: scaffold ready; needs numerical pass for a chosen V(GV).
