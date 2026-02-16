#!/usr/bin/env python3
import argparse
import math
import os

import numpy as np
import matplotlib.pyplot as plt


def heavy_mass(GV: np.ndarray, M0: float, alpha: float) -> np.ndarray:
    """
    GV-controlled Majorana mass suppression (toy):
      M_eff(GV) = M0 * exp(-alpha * GV)
    """
    return M0 * np.exp(-alpha * GV)


def seesaw_mass(GV: np.ndarray, mD: float, M0: float, alpha: float) -> np.ndarray:
    """
    Type-I seesaw (toy):
      m_light(GV) ~ mD^2 / M_eff(GV)
    """
    M = heavy_mass(GV, M0=M0, alpha=alpha)
    return (mD ** 2) / M


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="GV-controlled neutrino seesaw toy engine")

    parser.add_argument("--gv", type=float, default=1.0, help="Single GV value (non-scan mode)")
    parser.add_argument("--alpha", type=float, default=1.0, help="Suppression strength in M_eff(GV)")
    parser.add_argument("--mD", type=float, default=1e2, help="Dirac mass scale (toy units)")
    parser.add_argument("--M0", type=float, default=1e14, help="Baseline heavy mass scale (toy units)")

    parser.add_argument("--scan", action="store_true", help="Scan GV range and generate a plot")
    parser.add_argument("--gv-min", type=float, default=0.1, help="Scan lower bound")
    parser.add_argument("--gv-max", type=float, default=10.0, help="Scan upper bound")
    parser.add_argument("-n", type=int, default=400, help="Number of scan points")

    parser.add_argument("--loglog", action="store_true", help="Use log-log axes in scan plot")
    parser.add_argument("--out", type=str, default=None, help="Output image path (e.g., out/neutrino_scan.png)")

    args = parser.parse_args()

    if not args.scan:
        gv = float(args.gv)
        M = float(heavy_mass(np.array([gv]), M0=args.M0, alpha=args.alpha)[0])
        m = float(seesaw_mass(np.array([gv]), mD=args.mD, M0=args.M0, alpha=args.alpha)[0])
        print(f"GV={gv:.6g}, M_eff={M:.6e}, m_light={m:.6e}")
        return

    # Scan mode
    gv_vals = np.linspace(args.gv_min, args.gv_max, int(args.n))
    m_light = seesaw_mass(gv_vals, mD=args.mD, M0=args.M0, alpha=args.alpha)

    plt.figure()
    if args.loglog:
        # Guard against zeros/negatives (shouldn't happen here, but just in case)
        gv_plot = np.clip(gv_vals, 1e-300, None)
        m_plot = np.clip(m_light, 1e-300, None)
        plt.loglog(gv_plot, m_plot)
    else:
        plt.plot(gv_vals, m_light)

    plt.xlabel("GV")
    plt.ylabel("m_light (toy units)")
    plt.title(f"GV Seesaw Scan (alpha={args.alpha}, mD={args.mD:g}, M0={args.M0:g})")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    if args.out:
        ensure_parent_dir(args.out)
        plt.savefig(args.out, dpi=160, bbox_inches="tight")
        print(f"[OK] Saved plot -> {args.out}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
