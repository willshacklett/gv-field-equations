import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--gv", type=float, default=1.0)
parser.add_argument("--alpha", type=float, default=1.0)
parser.add_argument("--mD", type=float, default=1e2)
parser.add_argument("--M0", type=float, default=1e14)
parser.add_argument("--gv-min", type=float, default=0.1)
parser.add_argument("--gv-max", type=float, default=10.0)
parser.add_argument("--scan", action="store_true")
parser.add_argument("--out", type=str, default=None)

args = parser.parse_args()

alpha = args.alpha
mD = args.mD
M0 = args.M0


# -----------------------------
# GV-controlled heavy mass
# -----------------------------
def heavy_mass(GV):
    """
    Heavy Majorana mass suppressed by gradient strain.
    Includes asymptotic stabilization floor.
    """
    suppression = np.exp(-alpha * GV)
    floor = 1e10  # prevent collapse to zero
    return M0 * suppression + floor


# -----------------------------
# Light neutrino seesaw mass
# -----------------------------
def light_mass(GV):
    M = heavy_mass(GV)
    return mD**2 / M


# -----------------------------
# Single-point evaluation
# -----------------------------
if not args.scan:
    GV = args.gv
    m_light = light_mass(GV)
    m_heavy = heavy_mass(GV)

    print(f"GV = {GV}")
    print(f"Heavy mass M ≈ {m_heavy:.3e}")
    print(f"Light mass mν ≈ {m_light:.3e}")

# -----------------------------
# Scan mode
# -----------------------------
else:
    GV_vals = np.linspace(args.gv_min, args.gv_max, 300)
    m_light_vals = light_mass(GV_vals)
    m_heavy_vals = heavy_mass(GV_vals)

    plt.figure(figsize=(8,6))

    plt.loglog(GV_vals, m_light_vals, label="Light ν mass")
    plt.loglog(GV_vals, m_heavy_vals, linestyle="--", label="Heavy mass M")

    plt.xlabel("GV")
    plt.ylabel("Mass scale")
    plt.title("GV-Controlled Gradient Seesaw")
    plt.legend()
    plt.grid(True, which="both")

    if args.out:
        plt.savefig(args.out, dpi=150)
        print(f"[OK] Saved plot → {args.out}")
    else:
        plt.show()
