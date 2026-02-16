cat > qft/higgs_engine.py <<'EOF'
import argparse
import numpy as np
import matplotlib.pyplot as plt

def gv_weight(k, alpha=1.0, kc=1.0, p=2.0):
    # W_GV(k) = exp(-alpha * (k/kc)^p)
    x = np.maximum(k / kc, 0.0)
    return np.exp(-alpha * (x ** p))

def delta_m2(lam, mH=0.125, alpha=1.0, kc=1.0, p=2.0, n=20000):
    """
    Toy 1-loop-like integral (dimensionless demo):
      δm^2 ∝ ∫_0^Λ dk [ k^3/(k^2 + mH^2) ] * W_GV(k)

    We return the raw integral value (no prefactors) to visualize scaling.
    """
    k = np.linspace(0.0, lam, n)
    dk = k[1] - k[0]
    integrand = (k**3 / (k**2 + mH**2)) * gv_weight(k, alpha=alpha, kc=kc, p=p)
    return np.sum(integrand) * dk

def scan(lam_min, lam_max, alpha=1.0, kc=1.0, p=2.0, mH=0.125, n_lam=200):
    lams = np.linspace(lam_min, lam_max, n_lam)
    vals = np.array([delta_m2(L, mH=mH, alpha=alpha, kc=kc, p=p) for L in lams])
    return lams, vals

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam-min", type=float, default=0.1)
    ap.add_argument("--lam-max", type=float, default=50.0)
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--kc", type=float, default=5.0)
    ap.add_argument("--p", type=float, default=2.0)
    ap.add_argument("--mH", type=float, default=0.125)
    ap.add_argument("--nlam", type=int, default=250)
    ap.add_argument("--loglog", action="store_true")
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    lams, vals = scan(args.lam_min, args.lam_max, alpha=args.alpha, kc=args.kc, p=args.p, mH=args.mH, n_lam=args.nlam)

    plt.figure()
    if args.loglog:
        plt.loglog(lams, vals)
    else:
        plt.plot(lams, vals)

    plt.xlabel("Cutoff Λ (toy units)")
    plt.ylabel("Toy loop contribution δm_H^2 (arb.)")
    plt.title(f"GV UV-Suppression Saturation (alpha={args.alpha}, kc={args.kc}, p={args.p})")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    if args.out:
        plt.savefig(args.out, dpi=300, bbox_inches="tight")
        print(f"[OK] Saved plot -> {args.out}")
    else:
        plt.show()

    print(f"[OK] δm^2(Λ={lams[-1]:.2f}) = {vals[-1]:.6g}")

if __name__ == "__main__":
    main()
EOF
