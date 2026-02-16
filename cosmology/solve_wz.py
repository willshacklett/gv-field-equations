import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless-safe for Codespaces
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lam", type=float, default=0.05, help="GV residual drift amplitude (lambda)")
    parser.add_argument("--zmax", type=float, default=3.0, help="Max redshift")
    parser.add_argument("--n", type=int, default=500, help="Number of samples")
    args = parser.parse_args()

    lam = args.lam
    z = np.linspace(0.0, args.zmax, args.n)

    # Toy GV-inspired w(z) deviation model (keeps w -> -1 at high z)
    w = -1.0 + lam / (1.0 + z)**2

    out_dir = Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"wz_lam_{lam:.3f}_zmax_{args.zmax:.1f}.png"

    plt.figure()
    plt.plot(z, w)
    plt.xlabel("Redshift z")
    plt.ylabel("w(z)")
    plt.title(f"GV Dark Energy Toy Model (λ={lam})")
    plt.axhline(-1.0, linestyle="--")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)

    # Also print a few values so you *see* it ran
    print(f"[OK] Saved plot -> {out_path}")
    print(f"[OK] w(0)={w[0]:.6f}, w(1)={(-1.0 + lam/(1.0+1.0)**2):.6f}, w(zmax)={w[-1]:.6f}")

if __name__ == "__main__":
    main()
