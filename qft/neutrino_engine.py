import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path


def heavy_mass(GV: np.ndarray, M0: float, alpha: float) -> np.ndarray:
    """
    GV-controlled Majorana mass scale.
    Toy model: M(GV) = M0 * exp(-alpha * GV)
    """
    return M0 * np.exp(-alpha * GV)


def seesaw_mass(GV: np.ndarray, mD: float, M0: float, alpha: float) -> np.ndarray:
    """
    Light neutrino mass via toy seesaw:
      m_light ~ mD^2 / M(GV)
    """
    M = heavy_mass(GV, M0=M0, alpha=alpha)
    return (mD ** 2) / M


def ensure_parent(path_str: str | None):
    if not path_str:
        return
    p = Path(path_str)
    if p.parent and str(p.parent) != ".":
        p.parent.mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="GV-controlled neutrino seesaw toy engine")
    parser.add_argument("--gv", type=float, default=1.0, help="Single GV value (if not scanning)")
    parser.add_argument("--alpha", type=float, default=1.0, help="Suppression strength in M(GV)")
    parser.add_argument("--mD", type=float, default=1e2, help="Dirac scale proxy (same units as M0^(1/2))")
    parser.add_argument("--M0", type=float, default=1e14, help="Baseline Majorana scale")
    parser.add_argument("--out", type=str, default=None, help="Output plot path (png). If omitted, no plot saved.")
    parser.add_argument("--scan", action="store_true", help="Scan GV range and plot m_light(GV)")
    parser.add_argument("--gv-min", type=float, default=0.1, help="Scan minimum GV")
    parser.add_argument("--gv-max", type=float, default=10.0, help="Scan maximum GV")
    parser.add_argument("--n", type=int, default=300, help="Number of scan points")

    # plotting controls
    parser.add_argument("--loglog", action="store_true", help="Use log-log axes for scan plot")
    parser.add_argument("--semilogx", action="store_true", help="Use log x-axis for scan plot")
    parser.add_argument("--semilogy", action="store_true", help="Use log y-axis for scan plot")

    args = parser.parse_args()

    if args.scan:
        GV_vals = np.linspace(args.gv_min, args.gv_max, args.n)
        m_light = seesaw_mass(GV_vals, mD=args.mD, M0=args.M0, alpha=args.alpha)

        # Print a quick sanity snapshot
        print(f"[scan] alpha={args.alpha}, mD={args.mD:.3g}, M0={args.M0:.3g}")
        print(f"[scan] GV in [{args.gv_min}, {args.gv_max}], n={args.n}")
        print(f"[scan] m_light(GV_min)={m_light[0]:.6e}, m_light(GV_max)={m_light[-1]:.6e}")

        plt.figure()

        if args.loglog:
            plt.loglog(GV_vals, m_light)
        elif args.semilogx:
            plt.semilogx(GV_vals, m_light)
        elif args.semilogy:
            plt.semilogy(GV_vals, m_light)
        else:
            plt.plot(GV_vals, m_light)

        plt.xlabel("GV")
        plt.ylabel("m_light (toy units)")
        plt.title(f"GV-Controlled Seesaw Scan (alpha={args.alpha})")
        plt.grid(True)

        if args.out:
            ensure_parent(args.out)
            plt.savefig(args.out, dpi=200, bbox_inches="tight")
            print(f"[OK] Saved plot -> {args.out}")
        else:
            plt.show()

    else:
        # single-point mode
        GV = float(args.gv)
        M = float(heavy_mass(np.array([GV]), M0=args.M0, alpha=args.alpha)[0])
        m_light = float(seesaw_mass(np.array([GV]), mD=args.mD, M0=args.M0, alpha=args.alpha)[0])

        print(f"GV={GV:.4g}: M(GV)={M:.6e}, m_light={m_light:.6e}")

        if args.out:
            ensure_parent(args.out)
            # simple 1-point “marker” plot for convenience
            plt.figure()
            plt.scatter([GV], [m_light])
            plt.xlabel("GV")
            plt.ylabel("m_light (toy units)")
            plt.title(f"Single GV Neutrino Point (alpha={args.alpha})")
            plt.grid(True)
            plt.savefig(args.out, dpi=200, bbox_inches="tight")
            print(f"[OK] Saved plot -> {args.out}")


if __name__ == "__main__":
    main()
