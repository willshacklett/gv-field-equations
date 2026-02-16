import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--gv", type=float, default=1.0)
parser.add_argument("--gv-min", type=float, default=0.1)
parser.add_argument("--gv-max", type=float, default=10.0)
parser.add_argument("--alpha", type=float, default=1.0)
parser.add_argument("--mD", type=float, default=1e2)      # Dirac scale (GeV proxy)
parser.add_argument("--M0", type=float, default=1e14)     # Baseline heavy scale
parser.add_argument("--scan", action="store_true")
parser.add_argument("--out", type=str, default=None)

args = parser.parse_args()

alpha = args.alpha
mD = args.mD
M0 = args.M0


def heavy_mass(GV):
    """GV-controlled heavy Majorana scale"""
    return M0 * np.exp(-alpha * GV)


def seesaw_mass(GV):
    """Light neutrino mass via type-I seesaw"""
    M = heavy_mass(GV)
    return mD**2 / M


if args.scan:
    GV_vals = np.linspace(args.gv_min, args.gv_max, 400)
    m_light = seesaw_mass(GV_vals)
    M_heavy = heavy_mass(GV_vals)

    plt.figure(figsize=(7,5))
    plt.loglog(GV_vals, m_light, label="Light mass")
    plt.loglog(GV_vals, M_heavy, linestyle="--", label="Heavy mass")
    plt.xlabel("GV")
    plt.ylabel("Mass scale (proxy)")
    plt.title("GV-Controlled Seesaw Dynamics")
    plt.legend()
    plt.grid(True, which="both", ls=":")

    if args.out:
        plt.savefig(args.out, dpi=300)
    else:
        plt.show()

else:
    GV = args.gv
    m_light = seesaw_mass(GV)
    M_heavy = heavy_mass(GV)

    print(f"GV = {GV}")
    print(f"Heavy Majorana mass M = {M_heavy:.3e}")
    print(f"Light neutrino mass mν = {m_light:.3e}")
