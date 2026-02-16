import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless-safe for Codespaces/CI
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lam", type=float, default=0.05, help="GV residual drift amplitude (toy)")
    p.add_argument("--zmax", type=float, default=3.0, help="Max redshift")
    p.add_argument("--n", type=int, default=600, help="Number of points")
    p.add_argument("--out", type=str, default="wz.png", help="Output plot filename")
    args = p.parse_args()

    z = np.linspace(0.0, args.zmax, args.n)

    # Toy GV-inspired deviation:
    # w(z) = -1 + lam / (1+z)^2  (small late-time deviation, decays at high z)
    w = -1.0 + args.lam / (1.0 + z)**2

    plt.figure()
    plt.plot(z, w)
    plt.axhline(-1.0, linestyle="--")
    plt.xlabel("Redshift z")
    plt.ylabel("w(z)")
    plt.title(f"GV Dark Energy Toy Model (lam={args.lam})")
    plt.tight_layout()
    plt.savefig(args.out, dpi=180)
    print(f"Saved: {args.out}")

if __name__ == "__main__":
    main()
