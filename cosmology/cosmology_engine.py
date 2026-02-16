import numpy as np
import matplotlib.pyplot as plt
import argparse
import os


# ------------------------------------------------------------
# Argument Parser
# ------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument("--alpha", type=float, default=0.1)
parser.add_argument("--GV0", type=float, default=6.0)
parser.add_argument("--kappa", type=float, default=0.2)

parser.add_argument("--H0", type=float, default=70.0)
parser.add_argument("--Omega_m", type=float, default=0.3)
parser.add_argument("--Omega_gv", type=float, default=0.7)

parser.add_argument("--zmax", type=float, default=3.0)
parser.add_argument("--n", type=int, default=400)

parser.add_argument("--out", type=str, default=None)

args = parser.parse_args()


# ------------------------------------------------------------
# GV Dark Energy Model
# ------------------------------------------------------------

def w_of_z(z, alpha, GV0, kappa):
    """
    Toy GV equation of state.
    Approaches -1 at high z.
    """
    GV_z = GV0 * np.exp(-kappa * z)
    return -1.0 + alpha * np.exp(-GV_z)


def lambda_eff(z, alpha, GV0, kappa):
    """
    Effective vacuum energy density scaling.
    """
    GV_z = GV0 * np.exp(-kappa * z)
    return np.exp(-alpha * GV_z)


# ------------------------------------------------------------
# H(z) from dynamic w(z)
# ------------------------------------------------------------

def compute_Hz(z_vals, w_vals, H0, Omega_m, Omega_gv):
    """
    H^2(z) = H0^2 [ Ωm(1+z)^3 + Ωgv * exp(3∫(1+w)/(1+z) dz ) ]
    """

    integral = np.zeros_like(z_vals)

    for i in range(1, len(z_vals)):
        dz = z_vals[i] - z_vals[i-1]
        integrand = (1.0 + w_vals[i]) / (1.0 + z_vals[i])
        integral[i] = integral[i-1] + integrand * dz

    dark_energy_term = Omega_gv * np.exp(3.0 * integral)
    matter_term = Omega_m * (1.0 + z_vals)**3

    Hz = H0 * np.sqrt(matter_term + dark_energy_term)

    return Hz


# ------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------

z_vals = np.linspace(0.0, args.zmax, args.n)

w_vals = w_of_z(z_vals, args.alpha, args.GV0, args.kappa)
Hz_vals = compute_Hz(z_vals, w_vals, args.H0, args.Omega_m, args.Omega_gv)

# LCDM baseline
Hz_LCDM = args.H0 * np.sqrt(
    args.Omega_m * (1 + z_vals)**3 + args.Omega_gv
)


# ------------------------------------------------------------
# Plot 1 — w(z)
# ------------------------------------------------------------

plt.figure()
plt.plot(z_vals, w_vals, label="GV w(z)")
plt.axhline(-1.0, linestyle="--", label="ΛCDM w=-1")
plt.xlabel("Redshift z")
plt.ylabel("w(z)")
plt.title(
    f"GV Cosmology Engine: w(z)\n"
    f"(alpha={args.alpha}, GV0={args.GV0}, kappa={args.kappa})"
)
plt.legend()

os.makedirs("out", exist_ok=True)
plt.savefig("out/cosmology_wz.png", dpi=300)


# ------------------------------------------------------------
# Plot 2 — H(z)
# ------------------------------------------------------------

plt.figure()
plt.plot(z_vals, Hz_vals, label="GV H(z)")
plt.plot(z_vals, Hz_LCDM, "--", label="ΛCDM")
plt.xlabel("Redshift z")
plt.ylabel("H(z) [km/s/Mpc]")
plt.title("GV Cosmology Engine: Expansion History")
plt.legend()

plt.savefig("out/cosmology_Hz.png", dpi=300)


# ------------------------------------------------------------
# Optional Custom Output
# ------------------------------------------------------------

if args.out:
    plt.figure()
    plt.plot(z_vals, w_vals, label="GV w(z)")
    plt.plot(z_vals, Hz_vals / args.H0, label="H(z)/H0")
    plt.legend()
    plt.xlabel("Redshift z")
    plt.title("GV Cosmology Combined Output")
    plt.savefig(args.out, dpi=300)


# ------------------------------------------------------------
# Console Output
# ------------------------------------------------------------

print("\n[OK] Cosmology Engine Complete")
print(f"w(0) = {w_vals[0]:.6f}")
print(f"H(0) = {Hz_vals[0]:.6f} km/s/Mpc")
print("Saved:")
print("  out/cosmology_wz.png")
print("  out/cosmology_Hz.png")
