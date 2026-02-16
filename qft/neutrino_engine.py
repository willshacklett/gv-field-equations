#!/usr/bin/env python3
"""
GV Neutrino Engine (toy)

Goal:
- Make the seesaw idea "quantitative enough to test" as a toy model.
- Provide:
  (A) single-point evaluation at a chosen GV
  (B) scan over GV and plot light neutrino mass vs GV
  (C) "gradient seesaw" variant: mD depends on GV too

Physics (toy, not a full model):
- Heavy Majorana scale:    M(GV)  = M0 * exp(-alpha * GV)
- Dirac scale options:
    * constant:            mD(GV) = mD0
    * gradient seesaw:     mD(GV) = mD0 * (1 + beta * GV)
- Light mass scale proxy:  m_nu(GV) ~ mD(GV)^2 / M(GV)

All units are arbitrary "eV-like" proxies. The point is shape + scaling.
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


def heavy_mass(GV: np.ndarray, M0: float, alpha: float) -> np.ndarray:
    return M0 * np.exp(-alpha * GV)


def dirac_mass(GV: np.ndarray, mD0: float, beta: float, gradient: bool) -> np.ndarray:
    if gradient:
        return mD0 * (1.0 + beta * GV)
    return np.full_like(GV, mD0, dtype=float)


def light_mass(GV: np.ndarray, M0: float, alpha: float, mD0: float, beta: float, gradient: bool) -> np.ndarray:
    M = heavy_mass(GV, M0=M0, alpha=alpha)
    mD = dirac_mass(GV, mD0=mD0, beta=beta, gradient=gradient)
    return (mD ** 2) / M


def ensure_parent_dir(path: str) -> None:
    if not path:
        return
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)


def main() -> None:
    p = argparse.ArgumentParser(description="GV Neutrino Engine (toy): seesaw + scan + plots")
    p.add_argument("--gv", type=float, default=1.0, help="Single GV value (when not scanning)")
    p.add_argument("--scan", action="store_true", help="Scan GV over a range and plot")
    p.add_argument("--gv-min", type=float, default=0.1, help="Scan min GV")
    p.add_argument("--gv-max", type=float, default=10.0, help="Scan max GV")
    p.add_argument("--n", type=int, default=250, help="Number of scan points")

    p.add_argument("--alpha", type=float, default=1.0, help="Suppression strength in M(GV)=M0*exp(-alpha*GV)")
    p.add_argument("--M0", type=float, default=1e14, help="Baseline heavy scale")
    p.add_argument("--mD", type=float, default=1e2, help="Baseline Dirac scale mD0")

    p.add_argument("--gradient", action="store_true", help="Enable gradient seesaw: mD(GV)=mD0*(1+beta*GV)")
    p.add_argument("--beta", type=float, default=0.0, help="Gradient coupling beta for mD(GV)")

    p.add_argument("--out", type=str, default=None, help="Output PNG path (e.g., out/neutrino_scan.png)")
    p.add_argument("--loglog", action="store_true", help="Use log-log plot for scan")
    args = p.parse_args()

    if args.scan:
        GV = np.linspace(args.gv_min, args.gv_max, args.n)
        mnu = light_mass(GV, M0=args.M0, alpha=args.alpha, mD0=args.mD, beta=args.beta, gradient=args.gradient)
        M = heavy_mass(GV, M0=args.M0, alpha=args.alpha)
        mD = dirac_mass(GV, mD0=args.mD, beta=args.beta, gradient=args.gradient)

        plt.figure()
        if args.loglog:
            plt.loglog(GV, mnu)
        else:
            plt.plot(GV, mnu)

        title_bits = [f"alpha={args.alpha}", f"M0={args.M0:.2e}", f"mD0={args.mD:.2e}"]
        if args.gradient:
            title_bits.append(f"beta={args.beta}")
        plt.title("GV Neutrino Engine (toy): mν(GV) ~ mD(GV)^2 / M(GV)\n" + ", ".join(title_bits))
        plt.xlabel("GV")
        plt.ylabel("Light neutrino mass proxy mν (arb units)")
        plt.grid(True, which="both", linestyle="--", alpha=0.4)

        # Print quick endpoints to terminal for sanity
        print(f"[scan] GV in [{GV[0]:.3g}, {GV[-1]:.3g}] n={args.n}")
        print(f"[scan] M(GV0)={M[0]:.3e}  M(GVend)={M[-1]:.3e}")
        print(f"[scan] mD(GV0)={mD[0]:.3e} mD(GVend)={mD[-1]:.3e}")
        print(f"[scan] mν(GV0)={mnu[0]:.3e} mν(GVend)={mnu[-1]:.3e}")

        if args.out:
            ensure_parent_dir(args.out)
            plt.savefig(args.out, dpi=160, bbox_inches="tight")
            print(f"[OK] wrote {args.out}")
        else:
            plt.show()
    else:
        GV = np.array([args.gv], dtype=float)
        mnu = light_mass(GV, M0=args.M0, alpha=args.alpha, mD0=args.mD, beta=args.beta, gradient=args.gradient)[0]
        M = heavy_mass(GV, M0=args.M0, alpha=args.alpha)[0]
        mD = dirac_mass(GV, mD0=args.mD, beta=args.beta, gradient=args.gradient)[0]

        print(f"[single] GV={args.gv}")
        print(f"[single] M(GV)  = {M:.6e}")
        print(f"[single] mD(GV) = {mD:.6e}")
        print(f"[single] mν(GV) = {mnu:.6e}")

        # Optional quick plot at a single GV (just a point) if out is provided:
        if args.out:
            plt.figure()
            plt.scatter([args.gv], [mnu])
            plt.title("GV Neutrino Engine (toy): single-point mν(GV)")
            plt.xlabel("GV")
            plt.ylabel("mν (arb units)")
            plt.grid(True, linestyle="--", alpha=0.4)
            ensure_parent_dir(args.out)
            plt.savefig(args.out, dpi=160, bbox_inches="tight")
            print(f"[OK] wrote {args.out}")


if __name__ == "__main__":
    main()
