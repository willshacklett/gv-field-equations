cat > qft/neutrino_flavor_hierarchy.py <<'EOF'
import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt

def gv_weight(GV, alpha=1.0):
    # simple suppression factor
    return np.exp(-alpha * GV)

def toy_yukawa_texture(GV, eps0=0.2, alpha=1.0):
    """
    A toy 3x3 Yukawa matrix where GV increases hierarchy by suppressing
    off-diagonal mixing terms (constraint-stabilized flavor structure).
    """
    w = gv_weight(GV, alpha=alpha)
    eps = eps0 * w  # mixing suppressed as GV grows
    # diagonal entries represent a baseline hierarchy (toy)
    Y = np.array([
        [1e-6,  eps*1e-4, eps*1e-5],
        [eps*1e-4, 1e-3,  eps*1e-2],
        [eps*1e-5, eps*1e-2, 1.0]
    ], dtype=float)
    return Y

def seesaw_light_masses(Y, v=246.0, M0=1e14, GV=1.0, beta=0.5):
    """
    Toy type-I seesaw:
      m_nu ~ (v^2 / M_eff) * eig(Y Y^T)
    with a GV-modified heavy scale:
      M_eff = M0 * exp(+beta*GV)  (heavier with higher GV -> lighter neutrinos)
    """
    Meff = M0 * np.exp(beta * GV)
    M = (v**2 / Meff) * (Y @ Y.T)
    evals = np.linalg.eigvalsh(M)
    evals = np.sort(np.abs(evals))
    return evals, Meff

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gv-min", type=float, default=0.1)
    ap.add_argument("--gv-max", type=float, default=10.0)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--alpha", type=float, default=1.0, help="GV suppression strength (mixing damp)")
    ap.add_argument("--beta", type=float, default=0.5, help="GV scaling of heavy mass")
    ap.add_argument("--M0", type=float, default=1e14)
    ap.add_argument("--eps0", type=float, default=0.2)
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--csv", type=str, default=None)
    args = ap.parse_args()

    GV_vals = np.linspace(args.gv_min, args.gv_max, args.n)

    m1, m2, m3 = [], [], []
    Meffs = []

    for GV in GV_vals:
        Y = toy_yukawa_texture(GV, eps0=args.eps0, alpha=args.alpha)
        evals, Meff = seesaw_light_masses(Y, M0=args.M0, GV=GV, beta=args.beta)
        m1.append(evals[0]); m2.append(evals[1]); m3.append(evals[2])
        Meffs.append(Meff)

    m1 = np.array(m1); m2 = np.array(m2); m3 = np.array(m3)
    Meffs = np.array(Meffs)

    plt.figure()
    plt.loglog(GV_vals, m1, label="m1 (toy)")
    plt.loglog(GV_vals, m2, label="m2 (toy)")
    plt.loglog(GV_vals, m3, label="m3 (toy)")
    plt.xlabel("GV")
    plt.ylabel("Light neutrino masses (arb., log scale)")
    plt.title(f"GV Flavor/Hierarchy Toy (alpha={args.alpha}, beta={args.beta})")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    if args.out:
        plt.savefig(args.out, dpi=300, bbox_inches="tight")
        print(f"[OK] Saved plot -> {args.out}")
    else:
        plt.show()

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["GV", "m1", "m2", "m3", "M_eff"])
            for i in range(len(GV_vals)):
                w.writerow([GV_vals[i], m1[i], m2[i], m3[i], Meffs[i]])
        print(f"[OK] Saved CSV -> {args.csv}")

    print(f"[OK] Example @ GV={GV_vals[-1]:.2f}: m=[{m1[-1]:.3e},{m2[-1]:.3e},{m3[-1]:.3e}]  M_eff={Meffs[-1]:.3e}")

if __name__ == "__main__":
    main()
EOF
