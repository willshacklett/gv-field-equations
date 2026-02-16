import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

# -----------------------------
# Argument parsing
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
# GV Dark Energy Model
# -----------------------------

def w_z(z):
    """
    Toy GV equation of state.
    Approaches -1 at high z.
    """
    return -1.0 + kappa * np.exp(-alpha * z) * np.exp(-GV0 * 0.1)

def Lambda_eff(z):
    """
    Effective vacuum energy scaling.
    """
    return np.exp(-alpha * GV0) * np.exp(-0.2 * z)

def H_z(z, H0=70.0):
    """
    Flat universe approximation.
    H^2 = H0^2 [ Ωm(1+z)^3 + ΩΛ_eff(z) ]
    """
    Omega_L = 1.0 - Omega_m0
    return H0 * np.sqrt(
        Omega_m0 * (1 + z)**3 +
        Omega_L * Lambda_eff(z)
    )

# -----------------------------
# Luminosity Distance + SN μ(z)
# -----------------------------

def luminosity_distance(z, H0=70.0):
    """
    Numeric integral of 1/H(z).
    Toy flat universe.
    """
    z_vals = np.linspace(0, z, 400)
    dz = z_vals[1] - z_vals[0]
    Hz = H_z(z_vals, H0)
    integral = np.sum(1.0 / Hz) * dz
    return (1 + z) * integral * 3000.0  # ~ c/H0 in Mpc

def distance_modulus(z):
    dL = luminosity_distance(z)
    return 5 * np.log10(dL * 1e6) - 5

# -----------------------------
# Generate z grid
# -----------------------------

z_vals = np.linspace(0.001, 3.0, 300)

w_vals = w_z(z_vals)
mu_vals = np.array([distance_modulus(z) for z in z_vals])

# -----------------------------
# Plot w(z)
# -----------------------------

plt.figure(figsize=(8,6))
plt.plot(z_vals, w_vals, label="GV w(z)")
plt.axhline(-1, linestyle="--", label="ΛCDM w=-1")
plt.xlabel("Redshift z")
plt.ylabel("w(z)")
plt.title(f"GV Cosmology Engine (alpha={alpha}, GV0={GV0}, kappa={kappa})")
plt.legend()

if args.out:
    os.makedirs("out", exist_ok=True)
    plt.savefig(args.out, dpi=300)
else:
    plt.show()

# -----------------------------
# Save SN distance modulus CSV
# -----------------------------

os.makedirs("out", exist_ok=True)

np.savetxt(
    "out/sn_mu.csv",
    np.column_stack([z_vals, mu_vals]),
    delimiter=",",
    header="z,mu",
    comments=""
)

print("[OK] Cosmology engine run complete")
print(f"[OK] w(0)={w_vals[0]:.6f}")
print(f"[OK] Lambda_eff(0)={Lambda_eff(0):.6f}")
print("[OK] SN μ(z) saved to out/sn_mu.csv")
