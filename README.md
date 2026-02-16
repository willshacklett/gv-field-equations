# GV Field Equations

**Gradient Variable (GV)** is a constraint-based scalar field framework exploring how exponential gradient suppression can regulate high-energy phenomena.

This repository implements toy QFT-scale modules to explore:

- Neutrino mass generation
- Baryogenesis (CP asymmetry)
- Higgs hierarchy stabilization
- Constraint-driven suppression of UV divergences

The goal is not full UV completion — this is a structured sandbox for testing GV-controlled scaling behavior.

---

# Core Idea

GV acts as a constraint-gradient field that modifies effective masses and couplings:

General structure:

Effective parameter ~ Base scale × exp(-α · GV)

This produces:

- Suppressed heavy masses in high-GV regimes
- Natural hierarchies without fine tuning
- IR freedom with UV regulation
- Exponential damping of quadratic divergences

---

# Repository Structure

```
qft/
 ├── neutrino_engine.py
 ├── baryogenesis_engine.py
 ├── higgs_engine.py
 ├── hierarchy_stabilization.md
 ├── neutrino_flavor_hierarchy.py
 ├── neutrino_seesaw_toy.py
 ├── strong_cp_theta_dynamics.md
 ├── theta_relaxation_toy.py
```

Outputs are written to:

```
out/
```

---

# 1️⃣ Neutrino Engine

GV-controlled seesaw mechanism.

Seesaw structure:

m_ν ≈ m_D² / M_eff  
M_eff = M0 · exp(-α · GV)

Behavior:

- Increasing GV suppresses heavy sterile mass
- Light neutrino mass scales with gradient
- Hierarchies emerge naturally

### Run Single Point

```bash
python3 qft/neutrino_engine.py --gv 1.0
```

### Run GV Scan

```bash
python3 qft/neutrino_engine.py \
  --scan \
  --gv-min 0.1 \
  --gv-max 10 \
  --n 400 \
  --alpha 1.0 \
  --mD 1e2 \
  --M0 1e14 \
  --out out/neutrino_scan.png
```

Optional CSV output is generated during scans.

---

# 2️⃣ Baryogenesis Engine

Toy CP asymmetry model driven by GV.

Generic structure:

ε(GV, T) ~ α · GV · exp(-T / scale)

Toy BAU scaling:

η_B ~ θ̇(GV) / T

This module visualizes:

- CP asymmetry vs temperature
- BAU scaling trends
- GV dependence of asymmetry

### Run

```bash
python3 qft/baryogenesis_engine.py \
  --gv 1.0 \
  --alpha 1.0 \
  --out out/baryogenesis.png
```

Example alternate parameters:

```bash
python3 qft/baryogenesis_engine.py \
  --gv 3.0 \
  --alpha 2.0 \
  --out out/baryogenesis_gv3.png
```

---

# 3️⃣ Higgs Hierarchy Stabilization

Hierarchy problem addressed via exponential gradient suppression.

Quadratic correction structure:

Δm_H² ~ Λ² · exp(-β · GV)

Instead of fine tuning:

- Large UV scale Λ is exponentially damped
- Effective Higgs mass emerges from gradient control
- Hierarchy becomes constraint-driven, not accidental

See:

```
qft/hierarchy_stabilization.md
```

Run Higgs engine:

```bash
python3 qft/higgs_engine.py --gv 1.0 --beta 1.0
```

---

# 4️⃣ Strong CP / Theta Relaxation

Theta relaxation dynamics explored via GV-modified potential:

V(θ, GV) ~ Λ_QCD⁴ (1 − cos θ) · exp(-γ · GV)

Goal:

- Model dynamic suppression of CP violation
- Explore gradient-controlled vacuum alignment

See:

```
qft/theta_relaxation_toy.py
```

---

# Conceptual Summary

GV introduces exponential constraint suppression into QFT-scale systems:

| Phenomenon | Standard Issue | GV Interpretation |
|------------|---------------|------------------|
| Neutrino Mass | Seesaw hierarchy | Gradient-regulated heavy mass |
| BAU | CP asymmetry tuning | Gradient-amplified CP sector |
| Higgs | Quadratic divergence | Exponential UV damping |
| Strong CP | Small θ unexplained | Gradient vacuum stabilization |

---

# Philosophy

This is a structured sandbox.

It does not claim:

- Complete renormalizable UV completion
- Full EFT derivation
- Cosmological parameter fitting

It does explore:

- Gradient-driven exponential suppression
- Hierarchy emergence without fine tuning
- Constraint-flow interpretation of field dynamics

---

# Future Directions

- Full 3×3 GV seesaw matrix
- One-loop GV-EFT corrections
- Δm² fits to oscillation data
- CMB/Planck scaling checks
- Muon g−2 loop extension
- Flavor gradient mixing

---

# Status

Active development.

This repository is evolving toward a unified GV-QFT gradient suppression framework.
