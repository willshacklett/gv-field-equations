import numpy as np
import matplotlib.pyplot as plt
import argparse

# ----------------------------
# Argument parser
# ----------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--alpha", type=float, default=0.1, help="Gradient strength")
parser.add_argument("--GV0", type=float, default=5.0, help="Initial GV value")
parser.add_argument("--kappa", type=float, default=0.2, help="Relaxation rate")
parser.add_argument("--zmax", type=float, default=6.0, help="Max redshift")
parser.add_argument("--n", type=int, default=400, help="Resolution")
parser.add_argument("--out", type=str, default=None)

args = parser.parse_args()

alpha = args.alpha
GV0 = args.GV0
kappa = args.kappa

# ----------------------------
# GV potential
# ----------------------------

def V(GV):
    return np.exp(-alpha * GV)

def dV_dGV(GV):
    return -alpha * np.exp(-alpha * GV)

# ----------------------------
# Simple GV evolution vs redshift
# dGV/dz = -kappa * dV/dGV
# ----------------------------

z_vals = np.linspace(0, args.zmax, args.n)
GV_vals = np.zeros_like(z_vals)
GV_vals[0] = GV0

dz = z_vals[1] - z_vals[0]

for i in range(1, len(z_vals)):
    GV_vals[i] = GV_vals[i-1] - kappa * dV_dGV(GV_vals[i-1]) * dz

# Effective dark energy equation of state
w_eff = -1 + 0.1 * dV_dGV(GV_vals)

# ----------------------------
# Plot
# ----------------------------

plt.figure(figsize=(8,5))
plt.plot(z_vals, w_eff, label="w_eff(z)")
plt.axhline(-1, linestyle="--", label="ΛCDM")
plt.xlabel("Redshift z")
plt.ylabel("w_eff")
plt.title("GV Cosmology Engine")
plt.legend()

if args.out:
    plt.savefig(args.out, dpi=300)
else:
    plt.show()

print(f"[OK] alpha={alpha}, GV0={GV0}, kappa={kappa}")
print(f"[OK] w(z=0) ≈ {w_eff[0]:.5f}")
print(f"[OK] w(z_max) ≈ {w_eff[-1]:.5f}")
