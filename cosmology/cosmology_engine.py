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


# -----------------------------
# GV-modified equation of state
# -----------------------------
def w_GV(z):
    GV = GV0 * np.exp(-kappa * z)
    return -1 + alpha * np.exp(-GV)


# -----------------------------
# Hubble function (flat universe)
# -----------------------------
def H_over_H0(z):
    w = w_GV(z)
    Omega_L = 1 - Omega_m0
    return np.sqrt(
        Omega_m0 * (1 + z) ** 3 +
        Omega_L * np.exp(3 * np.cumsum((1 + w) / (1 + z)) * (z[1] - z[0]))
    )


# -----------------------------
# Growth equation (toy model)
# -----------------------------
def growth_factor(z):
    Hz = H_over_H0(z)
    integrand = (1 + z) / Hz**3
    integral = np.cumsum(integrand) * (z[1] - z[0])
    D = Hz * integral
    return D / D[0]


# -----------------------------
# Run engine
# -----------------------------
z = np.linspace(0, 3, 400)
D = growth_factor(z)

plt.figure()
plt.plot(z, D, label="GV Growth D(z)")
plt.xlabel("Redshift z")
plt.ylabel("Growth Factor D")
plt.title(f"GV Structure Growth (alpha={alpha}, GV0={GV0})")
plt.legend()

if args.out:
    plt.savefig(args.out, dpi=300)
else:
    plt.show()

print("[OK] Growth engine run complete")
print(f"[OK] D(0)={D[0]:.6f}")
