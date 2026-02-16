import numpy as np
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--gv", type=float, default=1.0)
parser.add_argument("--alpha", type=float, default=1.0)
parser.add_argument("--mD", type=float, default=1e2)
parser.add_argument("--M0", type=float, default=1e14)
parser.add_argument("--out", type=str, default=None)
args = parser.parse_args()

gv = args.gv
alpha = args.alpha
mD = args.mD
M0 = args.M0


def heavy_mass(GV):
    """
    GV-controlled Majorana mass suppression
    """
    return M0 * np.exp(-alpha * GV)


def seesaw_mass(GV):
    M = heavy_mass(GV)
    return mD**2 / M


GV_vals = np.linspace(0.1, 10, 200)
m_light = seesaw_mass(GV_vals)

plt.figure()
plt.loglog(GV_vals, m_light)
plt.xlabel("GV")
plt.ylabel("Light Neutrino Mass (eV scale proxy)")
plt.title("GV-Controlled Seesaw Engine")

if args.out:
    plt.savefig(args.out, dpi=300)
    print(f"[OK] Saved {args.out}")
else:
    plt.show()
