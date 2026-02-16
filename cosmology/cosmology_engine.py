import argparse
import numpy as np
import matplotlib.pyplot as plt

def w_of_z(z: np.ndarray, alpha: float, GV0: float, kappa: float) -> np.ndarray:
    """
    Toy GV-driven dark energy relaxation:
      - w(z) -> -1 at high z
      - w(0) = -1 + alpha * exp(-kappa * GV0)
    """
    return -1.0 + (alpha * np.exp(-kappa * GV0)) / (1.0 + z) ** 2

def lambda_eff(z: np.ndarray, alpha: float, GV0: float, kappa: float, Lambda0: float) -> np.ndarray:
    """
    Toy effective cosmological constant (dimensionless scaling):
      Lambda_eff(z) = Lambda0 * exp(-alpha * GV(z))
    with GV(z) = GV0 / (1+z)^kappa (toy relaxation).
    """
    GV_z = GV0 / (1.0 + z) ** kappa
    return Lambda0 * np.exp(-alpha * GV_z)

def main():
    p = argparse.ArgumentParser(description="GV Cosmology Engine (toy): w(z) + Lambda_eff(z)")
    p.add_argument("--alpha", type=float, default=0.10, help="GV coupling strength")
    p.add_argument("--GV0", type=float, default=6.0, help="GV at z=0 (today)")
    p.add_argument("--kappa", type=float, default=0.20, help="GV relaxation exponent vs redshift")
    p.add_argument("--Lambda0", type=float, default=1.0, help="Baseline Lambda scaling (dimensionless)")
    p.add_argument("--zmax", type=float, default=3.0, help="Max redshift")
    p.add_argument("--n", type=int, default=500, help="Number of samples")
    p.add_argument("--out", type=str, default=None, help="Output PNG path (optional)")
    p.add_argument("--csv", type=str, default=None, help="Output CSV path (optional)")
    args = p.parse_args()

    z = np.linspace(0.0, args.zmax, args.n)
    w = w_of_z(z, args.alpha, args.GV0, args.kappa)
    Leff = lambda_eff(z, args.alpha, args.GV0, args.kappa, args.Lambda0)

    # Save CSV if requested
    if args.csv:
        header = "z,w,Lambda_eff"
        data = np.column_stack([z, w, Leff])
        np.savetxt(args.csv, data, delimiter=",", header=header, comments="")
        print(f"[OK] Wrote CSV -> {args.csv}")

    # Plot
    plt.figure()
    plt.plot(z, w, label="w(z)")
    plt.axhline(-1.0, linestyle="--", label="LCDM w=-1")
    plt.xlabel("Redshift z")
    plt.ylabel("w(z)")
    plt.title(f"GV Cosmology Engine: w(z)  (alpha={args.alpha}, GV0={args.GV0}, kappa={args.kappa})")
    plt.legend()

    if args.out:
        plt.savefig(args.out, dpi=300)
        print(f"[OK] Saved plot -> {args.out}")
    else:
        plt.show()

    print(f"[OK] w(0)={w[0]:.6f}, w(zmax)={w[-1]:.6f}, Lambda_eff(0)={Leff[0]:.6f}")

if __name__ == "__main__":
    main()
