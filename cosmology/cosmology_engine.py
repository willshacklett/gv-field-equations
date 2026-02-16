import numpy as np
import matplotlib.pyplot as plt
import argparse

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

# --- Effective dark energy equation of state ---
def w_z(z):
    return -1 + kappa * np.exp(-alpha * GV0) * np.exp(-z)

# --- Hubble parameter squared (flat universe) ---
def H2(z):
    Omega_DE0 = 1 - Omega_m0
    return Omega_m0 * (1 + z)**3 + Omega_DE0 * np.exp(3 * np.cumsum((1 + w_z(z_grid)) / (1 + z_grid)) * dz)

# --- Growth equation (simple approximation) ---
def growth_factor(z_vals):
    D = np.zeros_like(z_vals)
    D[0] = 1.0

    for i in range(1, len(z_vals)):
        a = 1 / (1 + z_vals[i])
        D[i] = D[i-1] * a  # toy scaling for prototype

    return D

# --- Grid ---
z_grid = np.linspace(0, 3, 400)
dz = z_grid[1] - z_grid[0]

D_vals = growth_factor(z_grid)

plt.figure()
plt.plot(z_grid, D_vals, label="GV Growth D(z)")
plt.xlabel("Redshift z")
plt.ylabel("Growth Factor D")
plt.title(f"GV Structure Growth (alpha={alpha}, GV0={GV0})")
plt.legend()

if args.out:
    plt.savefig(args.out, dpi=300)
else:
    plt.show()

print(f"[OK] Growth engine run complete")
