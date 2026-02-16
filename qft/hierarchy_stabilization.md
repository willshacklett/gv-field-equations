cat > qft/hierarchy_stabilization.md <<'EOF'
# GV Hierarchy Stabilization (Higgs / EW Scale)

## Problem (standard EFT)
In ordinary QFT, Higgs mass receives quadratically sensitive corrections:
\[
\delta m_H^2 \sim \frac{\Lambda^2}{16\pi^2}
\]
So keeping \(m_H \sim 125\text{ GeV}\) when \(\Lambda\) could be \(M_{\rm Pl}\) requires extreme fine tuning.

## GV Principle
GV introduces a **constraint-gradient suppression** of high-strain (UV) fluctuations.

We model this as a loop-weight damping:
\[
\int d^4k \;\rightarrow\; \int d^4k\; W_{\rm GV}(k),
\quad
W_{\rm GV}(k)=e^{-\alpha\,{\rm GV}(k)}
\]

### Minimal ansatz
Let the “strain” increase with momentum:
\[
{\rm GV}(k)=\left(\frac{k}{k_c}\right)^p
\]
Then
\[
W_{\rm GV}(k)=\exp\!\left[-\alpha\left(\frac{k}{k_c}\right)^p\right]
\]

## Consequence
A representative correction becomes:
\[
\delta m_H^2 \propto \int_0^\Lambda dk\; \frac{k^3}{k^2+m_H^2}\; e^{-\alpha(k/k_c)^p}
\]
Instead of scaling like \(\Lambda^2\), the integral **saturates** once \(k \gtrsim k_c\).

Interpretation:
- EW vacuum sits in a low-GV attractor basin.
- UV fluctuations exist but are “expensive” (high constraint strain) and contribute weakly.
- Hierarchy is stabilized dynamically by constraint flow, not symmetry.

## Observable targets (program)
1) Fit a saturation scale \(k_c\) such that Higgs naturalness improves without violating LHC constraints.
2) Predict small IR deviations (running couplings, precision EW) consistent with “mostly SM” behavior.
3) Tie to the shared GV flow form:
\[
\partial_t {\rm GV} = -\nabla\cdot J_{\rm GV} + S({\rm GV})
\]
where the same suppression mechanism appears as an RG/flow weighting.

## Next: Toy solver
See `qft/higgs_engine.py` for a numerical demonstration of loop saturation vs. cutoff.
EOF
