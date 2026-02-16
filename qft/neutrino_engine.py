#!/usr/bin/env python3
"""
GV Neutrino Engine (toy model)

Idea:
- Heavy scale M(GV) is suppressed by GV (constraint decoupling)
- Light neutrino mass m_light ~ mD^2 / M(GV)
- Optionally add a "gradient-seesaw" variant: m_light ~ mD^2 / (M0 * (1 + alpha*GV))

This is not a physical neutrino fit — it's a controlled sandbox to generate testable curves.
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


def heavy_mass_exp(GV: np.ndarray, M0: float, alpha: float) -> np.ndarray:
    """Exponential GV suppression of heavy scale."""
    return M0 * np.exp(-alpha * GV)


def seesaw_mass(mD: float, M: np.ndarray) -> np.ndarray:
    """Type-I seesaw scaling."""
    return (mD ** 2) / M


def heavy_mass_grad(GV: np.ndarray, M0: float, alpha: float) -> np.ndarray:
    """Gradient-stabilized heavy scale (so it doesn't crash too fast)."""
    return M0 * (1.0 + alpha * GV)


def ensure_out_path(out_path: str | None) -> str | None:
    if out_path is None:
        return None
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    return out_path


def plot_and_save(x, y, xlabel, ylabel, title, out_path: str | None):
    plt.figure()
    plt.loglog(x, np.abs(y))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", alpha=0.3)

    if out_path:
        ensure_out_path(out_path)
        plt.savefig(out_path, dpi=200, bbox_inches="tight")
        print(f"[OK] saved -> {out_path}")
        plt.close()
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="GV neutrino seesaw engine (toy)")
    parser.add_argument("--gv", type=float, default=1.0, help="single GV value (single-point mode)")
    parser.add_argument("--alpha", type=float, default=1.0, help="GV coupling strength")
    parser.add_argument("--mD", type=float, default=1e2, help="Dirac mass scale (toy, in eV-ish units)")
    parser.add_argument("--M0", type=float, default=1e14, help="baseline heavy scale (toy units)")
    parser.add_argument("--out", type=str, default=None, help="output image path (png). If omitted, shows plot")

    # scan mode
    parser.add_argument("--scan", action="store_true", help="scan GV range and plot curves")
    parser.add_argument("--gv-min", type=float, default=0.1, help="scan GV minimum")
    parser.add_argument("--gv-max", type=float, default=10.0, help="scan GV maximum")
    parser.add_argument("--n", type=int, default=300, help="number of scan points")

    args = parser.parse_args()

    alpha = float(args.alpha)
    mD = float(args.mD)
    M0 = float(args.M0)

    if args.scan:
        GV = np.linspace(float(args.gv_min), float(args.gv_max), int(args.n))

        # Model A: exponential decoupling
        M_exp = heavy_mass_exp(GV, M0=M0, alpha=alpha)
        m_light_exp = seesaw_mass(mD=mD, M=M_exp)

        # Model B: gradient-stabilized variant
        M_grad = heavy_mass_grad(GV, M0=M0, alpha=alpha)
        m_light_grad = seesaw_mass(mD=mD, M=M_grad)

        # Save ONE plot that compares both (still a single figure)
        plt.figure()
        plt.loglog(GV, np.abs(m_light_exp), label="seesaw: M0*exp(-alpha*GV)")
        plt.loglog(GV, np.abs(m_light_grad), label="seesaw: M0*(1+alpha*GV)")
        plt.xlabel("GV")
        plt.ylabel("|m_light| (toy units)")
        plt.title(f"GV Neutrino Engine (scan)  alpha={alpha}, mD={mD}, M0={M0}")
        plt.grid(True, which="both", linestyle="--", alpha=0.3)
        plt.legend()

        if args.out:
            out_path = ensure_out_path(args.out)
            plt.savefig(out_path, dpi=200, bbox_inches="tight")
            print(f"[OK] saved -> {out_path}")
            plt.close()
        else:
            plt.show()

        # Print a few sample values for sanity
        for gv_test in [0.2, 0.5, 1.0, 2.0, 5.0]:
            M_t = heavy_mass_exp(np.array([gv_test]), M0=M0, alpha=alpha)[0]
            m_t = seesaw_mass(mD=mD, M=np.array([M_t]))[0]
            print(f"GV={gv_test:>4}:  M_exp={M_t:.3e}  m_light_exp={m_t:.3e}")

        return

    # single-point mode
    gv = float(args.gv)
    M = heavy_mass_exp(np.array([gv]), M0=M0, alpha=alpha)[0]
    m_light = seesaw_mass(mD=mD, M=np.array([M]))[0]
    print(f"GV={gv}: M_exp={M:.6e}, m_light_exp={m_light:.6e}")

    # also plot a tiny local neighborhood curve (so single point still produces a meaningful figure)
    GV_local = np.linspace(max(1e-6, gv * 0.2), gv * 3.0, 200)
    M_local = heavy_mass_exp(GV_local, M0=M0, alpha=alpha)
    m_local = seesaw_mass(mD=mD, M=M_local)
    plot_and_save(
        GV_local,
        m_local,
        xlabel="GV",
        ylabel="|m_light| (toy units)",
        title=f"GV Neutrino Engine (local)  GV={gv}, alpha={alpha}",
        out_path=args.out,
    )


if __name__ == "__main__":
    main()
