#!/usr/bin/env python3
"""
GV Gradient-Seesaw Toy Model

Core idea:
  M(GV) = M0 * GV^alpha
  m_nu(GV) ~ mD^2 / M(GV)

This is a toy (not a full neutrino-phenomenology fit). It provides a clean,
visual suppression curve showing how increasing GV stiffens the heavy scale
and suppresses the light mass scale.

Usage examples:
  python3 qft/neutrino_seesaw_toy.py
  python3 qft/neutrino_seesaw_toy.py --mD 1e11 --M0 1e14 --alpha 2.0
  python3 qft/neutrino_seesaw_toy.py --gv-min 0.2 --gv-max 10 --n 300 --out out/seesaw.png
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


EV_PER_GEV = 1.0e9  # 1 GeV = 1e9 eV


def heavy_scale_M(GV: np.ndarray, M0: float, alpha: float) -> np.ndarray:
    """Heavy (seesaw) scale in GeV."""
    return M0 * np.power(GV, alpha)


def light_mass_mnu(GV: np.ndarray, mD: float, M0: float, alpha: float) -> np.ndarray:
    """
    Light neutrino mass scale in eV (toy).
    m_nu ~ mD^2 / M(GV)
    where mD, M0 are in GeV.
    """
    M = heavy_scale_M(GV, M0=M0, alpha=alpha)  # GeV
    mnu_gev = (mD**2) / M                      # GeV
    return mnu_gev * EV_PER_GEV                # eV


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--M0", type=float, default=1e14, help="Baseline heavy scale M0 (GeV). Default: 1e14")
    p.add_argument("--mD", type=float, default=1e2, help="Dirac scale mD (GeV). Default: 1e2 (EW-ish)")
    p.add_argument("--alpha", type=float, default=1.0, help="GV scaling exponent alpha. Default: 1.0")
    p.add_argument("--gv-min", type=float, default=0.2, help="Min GV for sweep. Default: 0.2")
    p.add_argument("--gv-max", type=float, default=10.0, help="Max GV for sweep. Default: 10.0")
    p.add_argument("--n", type=int, default=250, help="Number of points. Default: 250")
    p.add_argument("--out", type=str, default="", help="Optional output PNG path (e.g., out/seesaw.png)")
    args = p.parse_args()

    if args.gv_min <= 0 or args.gv_max <= 0:
        raise ValueError("GV range must be > 0 for log plotting.")
    if args.gv_max <= args.gv_min:
        raise ValueError("gv-max must be > gv-min.")
    if args.M0 <= 0 or args.mD <= 0:
        raise ValueError("M0 and mD must be > 0.")

    GV = np.logspace(np.log10(args.gv_min), np.log10(args.gv_max), args.n)
    mnu = light_mass_mnu(GV, mD=args.mD, M0=args.M0, alpha=args.alpha)

    # Print a few checkpoints (nice for terminal receipts)
    for gv_check in [0.5, 1.0, 2.0, 5.0, 10.0]:
        if args.gv_min <= gv_check <= args.gv_max:
            val = float(light_mass_mnu(np.array([gv_check]), mD=args.mD, M0=args.M0, alpha=args.alpha)[0])
            print(f"GV={gv_check:>4}:  m_nu ~ {val:.3e} eV")

    # Plot
    plt.figure()
    plt.plot(GV, mnu)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("GV")
    plt.ylabel("Toy light neutrino mass scale  mν(GV)  [eV]")
    plt.title(f"GV Gradient-Seesaw:  M(GV)=M0·GV^α  |  M0={args.M0:.1e} GeV, mD={args.mD:.1e} GeV, α={args.alpha}")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    # A couple reference bands (optional visual anchors)
    # Typical neutrino mass scale ~ 0.01–0.1 eV
    plt.axhline(1e-1, linestyle=":", linewidth=1)
    plt.axhline(1e-2, linestyle=":", linewidth=1)

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        plt.savefig(args.out, dpi=180, bbox_inches="tight")
        print(f"[OK] Saved plot -> {args.out}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
