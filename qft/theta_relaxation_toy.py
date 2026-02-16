import argparse
import numpy as np

def simulate(theta0, k0, beta, tmax, n):
    """
    Toy model: dθ/dt = -k(t)*sinθ, with k(t) = k0*(1 + beta*exp(-t))
    beta mimics a transient early-time GV-driven enhancement of relaxation.
    """
    t = np.linspace(0, tmax, n)
    dt = t[1] - t[0]
    theta = np.zeros_like(t)
    theta[0] = theta0

    for i in range(1, n):
        k = k0 * (1.0 + beta * np.exp(-t[i-1]))
        theta[i] = theta[i-1] - dt * (k * np.sin(theta[i-1]))

        # keep theta in [-pi, pi] for readability
        if theta[i] > np.pi:
            theta[i] -= 2*np.pi
        elif theta[i] < -np.pi:
            theta[i] += 2*np.pi

    return t, theta

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta0", type=float, default=1.0, help="Initial theta (radians)")
    ap.add_argument("--k0", type=float, default=0.5, help="Baseline relaxation rate")
    ap.add_argument("--beta", type=float, default=2.0, help="Transient boost strength")
    ap.add_argument("--tmax", type=float, default=10.0, help="Max time")
    ap.add_argument("--n", type=int, default=2000, help="Steps")
    args = ap.parse_args()

    t, theta = simulate(args.theta0, args.k0, args.beta, args.tmax, args.n)

    print(f"[OK] theta0={args.theta0}, k0={args.k0}, beta={args.beta}")
    print(f"[OK] theta(tmax)={theta[-1]:.6f}")

    # simple scalar proxy: "EDM ~ theta"
    edm0 = abs(args.theta0)
    edmf = abs(theta[-1])
    print(f"[OK] EDM proxy reduction factor ~ {edmf/edm0:.6e}")

if __name__ == "__main__":
    main()
