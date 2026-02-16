import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.integrate import cumulative_trapezoid

# -----------------------------
# Argument parser
# -----------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--alpha", type=float, default=0.1)
parser.add_argument("--GV0", type=float, default=6.0)
parser.add_argument("--kappa", type=float, default=0.2)

parser.add_argument("--Omega_m", type=float, default=0.3)
parser.add_argument("--H0", type=float, default=70.0)

parser.add_argument("--zmax", type=float, default=3.0)
parser.add_argument("--n", type=int, default=400)

parser.add_argument("--out", type=str, default=None)
parser.add_argument("--csv", type=str, default=None)

args = parser.parse_args()

# -----------------------------
# Redshift grid
# -----------------------------
z = np.linspace(0, args.zmax, args.n)

# -----------------------------
# GV equation of state
# w(z) toy model
# -----------------------------
def w_gv(z):
    return -1 + args.kappa * np.exp(-args.alpha * args.GV0) / (1 + z)

# -----------------------------
# Effective Lambda(z)
# -----------------------------
def lambda_eff(z):
    return np.exp(-args.alpha * args.GV0) * (1 + z)**(-args.kappa)

# -----------------------------
# Hubble parameter
# -----------------------------
def H_gv(z):
    w = w_gv(z)
    Omega_L = lambda_eff(z)
    return args.H0 * np.sqrt(args.Omega_m * (1 + z)**3 + Omega_L)

def H_lcdm(z):
    return args.H0 * np.sqrt(args.Omega_m * (1 + z)**3 + (1 - args.Omega_m))

# -----------------------------
# Luminosity distance
# -----------------------------
c = 299792.458  # km/s

def luminosity_distance(z, H_func):
    integrand = c / H_func(z)
    integral = cumulative_trapezoid(integrand, z, initial=0)
    return (1 + z) * integral

dL_gv = luminosity_distance(z, H_gv)
dL_lcdm = luminosity_distance(z, H_lcdm)

# -----------------------------
# Distance modulus
# -----------------------------
def distance_modulus(dL):
    return 5 * np.log10(dL * 1e6) - 5  # Mpc to pc

mu_gv = distance_modulus(dL_gv)
mu_lcdm = distance_modulus(dL_lcdm)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8,6))
plt.plot(z, mu_gv, label="GV Cosmology")
plt.plot(z, mu_lcdm, "--", label="ΛCDM")
plt.xlabel("Redshift z")
plt.ylabel("Distance Modulus μ(z)")
plt.title("GV Cosmology Engine — SN Ia Test")
plt.legend()

if args.out:
    plt.savefig(args.out, dpi=300)
else:
    plt.show()

# -----------------------------
# Optional CSV output
# -----------------------------
if args.csv:
    data = np.column_stack([z, mu_gv, mu_lcdm])
    np.savetxt(args.csv, data,
               header="z, mu_gv, mu_lcdm",
               delimiter=",")
    print("[OK] CSV saved:", args.csv)

print("[OK] Run complete.")
