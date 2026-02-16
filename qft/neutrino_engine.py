#!/usr/bin/env python3
"""
GV Neutrino Engine (toy)

Idea:
- Heavy Majorana scale is suppressed by GV:
    M_eff(GV) = M0 * exp(-alpha * GV)

- Light neutrino mass from seesaw:
    m_nu(GV) = mD^2 / M_eff(GV)

This is a toy "GV-controlled seesaw" used for qualitative scans + plots.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def heavy_mass(gv: np.ndarray, alpha: float, M0: float) -> np.ndarray:
    return M0 * np.exp(-alpha * gv)


def light_mass(gv: np.ndarray, alpha: float, mD: float, M0: float) -> np.ndarray:
    M = heavy_mass(gv, alpha, M0)
    return (mD**2) / M


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gv", type=float, default=1.0, help="Single GV value to evaluate")
    p.add_argument("--alpha", type=float, default=1.0, help="GV suppression strength")
    p.add_argument("--mD", type=float, default=1e2, help="Dirac mass scale (toy units)")
    p.add_argument("--M0", type=float, default=1e14, help="Base heavy Majorana scale (toy units)")

    # Scan mode
    p.add_argument("--scan", action="store_true", help="Scan GV range and plot m_nu(GV)")
    p.add_argument("--gv-min", type=float, default=0.1, help="Scan min GV")
    p.add_argument("--gv-max", type=float, default=10.0, help="Scan max GV")
    p.add_argument("--n", type=int, default=200, help="Number of scan points")

    # Output controls
    p.add_argument("--out", type=str, default=None, help="Output PNG path (e.g., out/neutrino_scan.png)")
    p.add_argument("--csv", type=str, default=None, help="Optional CSV output path for scan (GV,M_eff,m_nu)")
    p.add_argument("--loglog", action="store_true", help="Use log-log plot for scan")

    args = p.parse_args()

    if not args.scan:
        gv = float(args.gv)
        M = heavy_mass(np.array([gv]), args.alpha, args.M0)[0]
        m = light_mass(np.array([gv]), args.alpha, args.mD, args.M0)[0]
        print(f"GV={gv:g} | M_eff={M:.6e} | m_light={m:.6e}")
        return

    # Scan
    gv_vals = np.linspace(args.gv_min, args.gv_max, int(args.n))
    M_vals = heavy_mass(gv_vals, args.alpha, args.M0)
    m_vals = light_mass(gv_vals, args.alpha, args.mD, args.M0)

    # Optional CSV
    if args.csv:
        csv_path = Path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("GV,M_eff,m_light\n")
            for gv, M, m in zip(gv_vals, M_vals, m_vals):
                f.write(f"{gv},{M},{m}\n")
        print(f"[OK] Wrote CSV -> {csv_path}")

    # Plot
    plt.figure()
    if args.loglog:
        plt.loglog(gv_vals, m_vals)
    else:
        plt.plot(gv_vals, m_vals)

    plt.xlabel("GV")
    plt.ylabel("Light neutrino mass (toy units)")
    plt.title(f"GV-controlled seesaw (alpha={args.alpha}, mD={args.mD:.2e}, M0={args.M0:.2e})")
    plt.grid(True, which="both", alpha=0.25)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, dpi=160, bbox_inches="tight")
        print(f"[OK] Saved plot -> {out_path}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
