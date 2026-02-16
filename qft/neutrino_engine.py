#!/usr/bin/env python3
"""
GV Neutrino Engine (Toy, but structured)

Implements a GV-modulated Type-I seesaw:
  M_eff(GV) = - mD^T * inv(MR(GV)) * mD

With:
  MR(GV) = MR0 * (1 + alpha * GV)

And optional GV-induced mixing:
  mD(GV) = mD0 + eps * GV * Delta   (small off-diagonal perturbation)

Outputs:
- Prints masses, Δm^2, and mixing angles (θ12, θ13, θ23)
- Optionally sweeps GV range and saves plots + CSV

NOTE:
This is a *real-symmetric* toy model (no CP phase, no complex Takagi factorization).
Great for program scaffolding + trend tests.
"""

import argparse
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def parse_triple(s: str):
    parts = [float(x.strip()) for x in s.split(",")]
    if len(parts) != 3:
        raise ValueError("Expected 3 comma-separated floats, e.g. 1e2,1e2,1e2")
    return np.array(parts, dtype=float)


def build_mD(mD_diag: np.ndarray, eps: float, gv: float, seed: int):
    # baseline Dirac mass (toy): diagonal
    mD0 = np.diag(mD_diag)

    # deterministic perturbation "texture" Delta (off-diagonal only)
    rng = np.random.default_rng(seed)
    Delta = rng.normal(0.0, 1.0, size=(3, 3))
    Delta = (Delta + Delta.T) / 2.0  # symmetric
    np.fill_diagonal(Delta, 0.0)

    # scale texture to be "small" relative to diagonal masses
    # (use geometric mean of diag entries as scale)
    scale = float(np.sqrt(np.mean(mD_diag**2)))
    Delta = Delta * scale

    return mD0 + (eps * gv) * Delta


def build_MR(MR_diag: np.ndarray, alpha: float, gv: float):
    # MR(GV) = MR0 * (1 + alpha*GV) applied to each eigen-scale
    factor = (1.0 + alpha * gv)
    if factor <= 0:
        raise ValueError("MR factor became <= 0. Choose smaller alpha*GV.")
    return np.diag(MR_diag * factor)


def seesaw_effective_mass(mD: np.ndarray, MR: np.ndarray):
    MR_inv = np.linalg.inv(MR)
    return -mD.T @ MR_inv @ mD


def diag_real_symmetric(M: np.ndarray):
    # For real symmetric matrices: eigh gives orthonormal eigenvectors
    evals, evecs = np.linalg.eigh(M)
    # masses are absolute values of eigenvalues (toy Majorana sign ambiguity)
    masses = np.abs(evals)

    # sort by increasing masses (like m1 <= m2 <= m3)
    idx = np.argsort(masses)
    masses = masses[idx]
    evals = evals[idx]
    U = evecs[:, idx]  # columns are eigenvectors

    # enforce a consistent sign convention (optional): make U_e1 positive
    for j in range(3):
        if U[0, j] < 0:
            U[:, j] *= -1.0

    return masses, evals, U


def mixing_angles_from_U(U: np.ndarray):
    # Standard approximations (no CP phase), using absolute values
    Uabs = np.abs(U)

    s13 = float(np.clip(Uabs[0, 2], 0.0, 1.0))
    c13 = math.sqrt(max(1.0 - s13**2, 0.0))

    if c13 < 1e-12:
        # pathological
        s12 = 0.0
        s23 = 0.0
    else:
        s12 = float(np.clip(Uabs[0, 1] / c13, 0.0, 1.0))
        s23 = float(np.clip(Uabs[1, 2] / c13, 0.0, 1.0))

    th13 = math.degrees(math.asin(s13))
    th12 = math.degrees(math.asin(s12))
    th23 = math.degrees(math.asin(s23))
    return th12, th13, th23


def deltam2(masses: np.ndarray):
    m1, m2, m3 = masses
    dm21 = m2**2 - m1**2
    dm31 = m3**2 - m1**2
    dm32 = m3**2 - m2**2
    return float(dm21), float(dm31), float(dm32)


def hierarchy_label(dm31: float):
    # In our sorted-by-mass toy, dm31 is usually >= 0.
    # But if you later choose to keep signed eigenvalues, this helps.
    return "normal-ish" if dm31 >= 0 else "inverted-ish"


def run_one(gv: float, args):
    mD = build_mD(args.mD_diag, args.eps, gv, args.seed)
    MR = build_MR(args.MR_diag, args.alpha, gv)
    Meff = seesaw_effective_mass(mD, MR)

    masses, evals, U = diag_real_symmetric(Meff)
    th12, th13, th23 = mixing_angles_from_U(U)
    dm21, dm31, dm32 = deltam2(masses)

    result = {
        "GV": gv,
        "alpha": args.alpha,
        "eps": args.eps,
        "mD_diag": args.mD_diag.tolist(),
        "MR_diag": args.MR_diag.tolist(),
        "masses": masses.tolist(),
        "eigenvalues_signed": evals.tolist(),
        "dm21": dm21,
        "dm31": dm31,
        "dm32": dm32,
        "theta12_deg": th12,
        "theta13_deg": th13,
        "theta23_deg": th23,
        "hierarchy": hierarchy_label(dm31),
    }
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gv", type=float, default=1.0, help="Single GV value (default 1.0)")
    p.add_argument("--gv-min", type=float, default=None, help="Sweep: GV min")
    p.add_argument("--gv-max", type=float, default=None, help="Sweep: GV max")
    p.add_argument("--n", type=int, default=50, help="Sweep points (default 50)")

    p.add_argument("--alpha", type=float, default=1.0, help="MR scaling strength (default 1.0)")
    p.add_argument("--eps", type=float, default=0.02, help="GV-induced mixing strength (default 0.02)")
    p.add_argument("--seed", type=int, default=7, help="Deterministic texture seed (default 7)")

    p.add_argument("--mD", dest="mD_str", default="1e2,2e2,3e2", help="mD diag (GeV), e.g. 1e2,2e2,3e2")
    p.add_argument("--MR", dest="MR_str", default="1e14,3e14,8e14", help="MR diag (GeV), e.g. 1e14,3e14,8e14")

    p.add_argument("--outdir", default="out", help="Output directory (default out)")
    p.add_argument("--prefix", default="neutrino", help="Output file prefix (default neutrino)")
    p.add_argument("--save", action="store_true", help="Save JSON/CSV/plots")
    args = p.parse_args()

    args.mD_diag = parse_triple(args.mD_str)
    args.MR_diag = parse_triple(args.MR_str)

    ensure_dir(args.outdir)

    # --- single run
    single = run_one(args.gv, args)

    print("\n=== GV Neutrino Engine (single run) ===")
    print(f"GV = {single['GV']:.4g} | alpha={single['alpha']:.4g} | eps={single['eps']:.4g}")
    print(f"masses (arb): {single['masses']}")
    print(f"Δm^2_21: {single['dm21']:.4e} | Δm^2_31: {single['dm31']:.4e} | Δm^2_32: {single['dm32']:.4e}")
    print(f"θ12={single['theta12_deg']:.2f}°, θ13={single['theta13_deg']:.2f}°, θ23={single['theta23_deg']:.2f}°")
    print(f"hierarchy: {single['hierarchy']}")

    # --- sweep if requested
    do_sweep = args.gv_min is not None and args.gv_max is not None
    sweep_rows = []
    if do_sweep:
        gvs = np.linspace(args.gv_min, args.gv_max, args.n)
        for gv in gvs:
            sweep_rows.append(run_one(float(gv), args))

        # arrays for plots
        g = np.array([r["GV"] for r in sweep_rows], dtype=float)
        m = np.array([r["masses"] for r in sweep_rows], dtype=float)  # (N,3)
        t12 = np.array([r["theta12_deg"] for r in sweep_rows], dtype=float)
        t13 = np.array([r["theta13_deg"] for r in sweep_rows], dtype=float)
        t23 = np.array([r["theta23_deg"] for r in sweep_rows], dtype=float)
        dm21 = np.array([r["dm21"] for r in sweep_rows], dtype=float)
        dm31 = np.array([r["dm31"] for r in sweep_rows], dtype=float)

        # Plot masses vs GV
        plt.figure()
        plt.plot(g, m[:, 0], label="m1")
        plt.plot(g, m[:, 1], label="m2")
        plt.plot(g, m[:, 2], label="m3")
        plt.xlabel("GV")
        plt.ylabel("Mass eigenvalues (arb)")
        plt.title("GV-Seesaw: Mass spectrum vs GV")
        plt.legend()
        if args.save:
            path = os.path.join(args.outdir, f"{args.prefix}_masses_vs_gv.png")
            plt.savefig(path, dpi=160, bbox_inches="tight")
            print(f"[OK] saved {path}")
        else:
            plt.show()
        plt.close()

        # Plot angles vs GV
        plt.figure()
        plt.plot(g, t12, label="θ12")
        plt.plot(g, t13, label="θ13")
        plt.plot(g, t23, label="θ23")
        plt.xlabel("GV")
        plt.ylabel("Angle (deg)")
        plt.title("GV-Seesaw: Mixing angles vs GV")
        plt.legend()
        if args.save:
            path = os.path.join(args.outdir, f"{args.prefix}_angles_vs_gv.png")
            plt.savefig(path, dpi=160, bbox_inches="tight")
            print(f"[OK] saved {path}")
        else:
            plt.show()
        plt.close()

        # Plot delta m^2 vs GV
        plt.figure()
        plt.plot(g, dm21, label="Δm^2_21")
        plt.plot(g, dm31, label="Δm^2_31")
        plt.xlabel("GV")
        plt.ylabel("Δm^2 (arb)")
        plt.title("GV-Seesaw: Mass-squared splittings vs GV")
        plt.legend()
        if args.save:
            path = os.path.join(args.outdir, f"{args.prefix}_dm2_vs_gv.png")
            plt.savefig(path, dpi=160, bbox_inches="tight")
            print(f"[OK] saved {path}")
        else:
            plt.show()
        plt.close()

    # save outputs
    if args.save:
        # JSON (single + optional sweep)
        json_path = os.path.join(args.outdir, f"{args.prefix}_single.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(single, f, indent=2)
        print(f"[OK] saved {json_path}")

        if do_sweep:
            json_path = os.path.join(args.outdir, f"{args.prefix}_sweep.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(sweep_rows, f, indent=2)
            print(f"[OK] saved {json_path}")

            # CSV
            csv_path = os.path.join(args.outdir, f"{args.prefix}_sweep.csv")
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("GV,m1,m2,m3,dm21,dm31,theta12,theta13,theta23\n")
                for r in sweep_rows:
                    m1, m2, m3 = r["masses"]
                    f.write(
                        f"{r['GV']},{m1},{m2},{m3},{r['dm21']},{r['dm31']},"
                        f"{r['theta12_deg']},{r['theta13_deg']},{r['theta23_deg']}\n"
                    )
            print(f"[OK] saved {csv_path}")


if __name__ == "__main__":
    main()
