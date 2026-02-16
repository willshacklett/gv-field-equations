import argparse
import numpy as np
import matplotlib.pyplot as plt


def heavy_masses(GV: float, M0: float, alpha: float, ratios=(1.0, 3.0, 10.0)) -> np.ndarray:
    """
    Toy GV-controlled heavy Majorana masses.
    M_i(GV) = (M0 * ratio_i) * exp(-alpha * GV)
    """
    ratios = np.array(ratios, dtype=float)
    return (M0 * ratios) * np.exp(-alpha * GV)


def build_dirac_matrix(mD: float, eps: float, seed: int) -> np.ndarray:
    """
    Toy Dirac mass matrix with a simple texture + small random perturbations.
    Symmetry isn't sacred here — this is a controllable sandbox.
    """
    rng = np.random.default_rng(seed)

    # Simple "texture" (order-1 entries) scaled by mD
    base = np.array([
        [1.00, 0.30, 0.10],
        [0.30, 0.90, 0.20],
        [0.10, 0.20, 0.80],
    ], dtype=float) * mD

    # Small perturbation (relative to mD)
    perturb = rng.normal(0.0, 1.0, size=(3, 3)) * (eps * mD)

    return base + perturb


def seesaw_light_mass_matrix(mD_mat: np.ndarray, M_heavy: np.ndarray) -> np.ndarray:
    """
    Type-I seesaw (toy):
      m_nu = - mD * M_R^{-1} * mD^T
    where M_R is diagonal with entries M_heavy.
    """
    MR_inv = np.diag(1.0 / M_heavy)
    mnu = -mD_mat @ MR_inv @ mD_mat.T
    # ensure symmetry numerically
    return 0.5 * (mnu + mnu.T)


def diag_symmetric(mat: np.ndarray):
    """
    Diagonalize real symmetric matrix:
      mat = U diag(evals) U^T
    """
    evals, U = np.linalg.eigh(mat)
    # sort by ascending mass (absolute scale)
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]
    U = U[:, idx]
    return evals, U


def main():
    parser = argparse.ArgumentParser(description="GV-controlled neutrino seesaw engine (3x3 toy).")

    parser.add_argument("--gv", type=float, default=1.0, help="GV value (scalar control).")
    parser.add_argument("--alpha", type=float, default=1.0, help="GV coupling strength in heavy mass suppression.")
    parser.add_argument("--M0", type=float, default=1e14, help="Baseline heavy scale.")
    parser.add_argument("--mD", type=float, default=1e2, help="Dirac scale (toy).")
    parser.add_argument("--ratios", type=str, default="1,3,10", help="Comma list for heavy mass ratios.")
    parser.add_argument("--eps", type=float, default=0.03, help="Relative perturbation size for Dirac texture.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for texture perturbations.")

    parser.add_argument("--scan", action="store_true", help="Scan GV range and plot eigen-masses vs GV.")
    parser.add_argument("--gv-min", type=float, default=0.1)
    parser.add_argument("--gv-max", type=float, default=10.0)
    parser.add_argument("--n", type=int, default=200)

    parser.add_argument("--out", type=str, default=None, help="Output PNG path (for scan plot).")
    args = parser.parse_args()

    ratios = tuple(float(x.strip()) for x in args.ratios.split(",") if x.strip())

    # Build one Dirac matrix (fixed across scan so GV is the only knob)
    mD_mat = build_dirac_matrix(mD=args.mD, eps=args.eps, seed=args.seed)

    def solve_at_gv(gv_val: float):
        M_heavy = heavy_masses(gv_val, M0=args.M0, alpha=args.alpha, ratios=ratios)
        mnu = seesaw_light_mass_matrix(mD_mat, M_heavy)
        evals, U = diag_symmetric(mnu)
        # masses are |eigenvalues| in this toy (sign is convention)
        masses = np.abs(evals)
        return M_heavy, mnu, masses, U

    if not args.scan:
        M_heavy, mnu, masses, U = solve_at_gv(args.gv)

        print(f"GV = {args.gv}")
        print(f"Heavy masses M_i(GV) = {M_heavy}")
        print("Light mass matrix m_nu (toy) =")
        np.set_printoptions(precision=3, suppress=True)
        print(mnu)
        print(f"Light eigen-masses |m_i| (toy units) = {masses}")
        print("Toy mixing matrix U (columns = mass eigenstates) =")
        print(U)

        # quick “mixing angles” proxies (not physical unless you define conventions carefully)
        # still useful for iteration + sanity checks
        s13 = abs(U[0, 2])
        s12 = abs(U[0, 1]) / max(1e-12, np.sqrt(1 - s13**2))
        s23 = abs(U[1, 2]) / max(1e-12, np.sqrt(1 - s13**2))
        print(f"Proxy angles: sinθ13≈{s13:.3f}, sinθ12≈{s12:.3f}, sinθ23≈{s23:.3f}")
        return

    # Scan mode: eigen-masses vs GV
    GV_vals = np.linspace(args.gv_min, args.gv_max, args.n)
    m1, m2, m3 = [], [], []

    for gv_val in GV_vals:
        _, _, masses, _ = solve_at_gv(gv_val)
        m1.append(masses[0])
        m2.append(masses[1])
        m3.append(masses[2])

    plt.figure()
    plt.semilogy(GV_vals, m1, label="m1")
    plt.semilogy(GV_vals, m2, label="m2")
    plt.semilogy(GV_vals, m3, label="m3")
    plt.xlabel("GV")
    plt.ylabel("Light eigen-masses |m_i| (toy units)")
    plt.title(f"GV Seesaw Eigen-masses (alpha={args.alpha}, M0={args.M0:.1e}, mD={args.mD:.1e})")
    plt.legend()

    if args.out:
        plt.savefig(args.out, dpi=200, bbox_inches="tight")
        print(f"[OK] saved: {args.out}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
