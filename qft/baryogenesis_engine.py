import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--gv", type=float, default=1.0)
parser.add_argument("--alpha", type=float, default=1.0)
parser.add_argument("--epsilon0", type=float, default=1e-6)
parser.add_argument("--Tscale", type=float, default=100.0)
parser.add_argument("--out", type=str, default=None)

args = parser.parse_args()

GV = args.gv
alpha = args.alpha
epsilon0 = args.epsilon0
Tscale = args.Tscale


def cp_asymmetry(GV, T):
    """
    Transient CP bias from GV relaxation
    ε(GV,T) = ε0 * exp(-alpha*GV) * exp(-T/Tscale)
    """
    return epsilon0 * np.exp(-alpha * GV) * np.exp(-T / Tscale)


# temperature range (GeV scale proxy)
T_vals = np.linspace(0, 500, 400)
epsilon_vals = cp_asymmetry(GV, T_vals)

plt.figure()
plt.plot(T_vals, epsilon_vals)
plt.xlabel("Temperature (GeV proxy)")
plt.ylabel("CP Asymmetry ε")
plt.title(f"GV Baryogenesis Toy Model (GV={GV}, α={alpha})")

if args.out:
    plt.savefig(args.out, dpi=300)
else:
    plt.show()

print(f"[OK] GV={GV}, alpha={alpha}")
print(f"[OK] Peak CP asymmetry ~ {epsilon_vals.max():.3e}")
