import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

# -----------------------------
# Argument parser
# -----------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--alpha", type=float, default=0.1)
parser.add_argument("--GV0", type=float, default=6.0)
parser.add_argument("--kappa", type=float, default=0.2)
parser.add_argument("--Omega_m0", type=float, default=0.3)
parser.add_argument("--out", type=str, default=None)

args = parser.parse_args()

alpha = args.alpha
GV0 = args.GV0
kappa = args.kappa
Omega_m0 = args.Omega_m0

# -----------------------------
# Redshift grid
# -----------------------------
z = np.linspace(0, 3, 400)

# -----------------------------
# GV evolution model
# -----------------------------
def GV_z(z):
    return GV0 * np.exp(-kappa * z)

# -----------------------------
# Effective dark energy
# -----------------------------
def Lambda_eff(GV):
    return np.exp(-alpha * GV)

# -----------------------------
# Equation of state w(z)
# -----------------------------
def w_z(GV):
    # Slight deviation from -1
    return -1 + 0.03 * np.exp(-alpha * GV)

# -----------------------------
# Structure growth toy model
# -----------------------------
def growth_factor(z, w):
    return np.exp(-z * (1 + w))

# -----------------------------
# Compute quantities
# -----------------------------
GV_vals = GV_z(z)
Lambda_vals = Lambda_eff(GV_vals)
w_vals = w_z(GV_vals)
D_vals = growth_factor(z, w_vals)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8,6))

plt.plot(z, w_vals, label="w(z)")
plt.plot(z, D_vals, label="Growth D(z)")
plt.axhline(-1, linestyle="--", label="LCDM w=-1")

plt.xlabel("Redshift z")
plt.ylabel("Value")
plt.title(f"GV Cosmology Engine (alpha={alpha}, GV0={GV0}, kappa={kappa})")
plt.legend()

if args.out:
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    plt.savefig(args.out, dpi=300)
    print(f"[OK] Plot saved to {args.out}")
else:
    plt.show()

print(f"[OK] w(0) = {w_vals[0]:.6f}")
print(f"[OK] Lambda_eff(0) = {Lambda_vals[0]:.6f}")
print(f"[OK] Growth D(0) = {D_vals[0]:.6f}")
