import argparse
import numpy as np
import matplotlib.pyplot as plt


def V_eff(GV: np.ndarray, V0: float, alpha: float) -> np.ndarray:
    """
    GV effective potential (toy):
        V(GV) = V0 * exp(-alpha * GV)
    """
    return V0 * np.exp(-alpha * GV)


def slow_roll_params(alpha: float) -> tuple[float, float]:
    """
    For V = V0 e^{-alpha GV} with canonically-normalized GV:
        epsilon = (1/2) (V'/V)^2 = (1/2) alpha^2
        eta     = V''/V       = alpha^2
    """
    eps = 0.5 * alpha**2
    eta = alpha**2
    return eps, eta


def inflation_observables(alpha: float) -> tuple[float, float]:
    """
    Toy predictions:
        n_s ≈ 1 - 2ε - η = 1 - 2α^2
        r   = 16ε = 8α^2
    """
    eps, eta = slow_roll_params(alpha)
    ns = 1.0 - 2.0 * eps - eta
    r = 16.0 * eps
    return ns, r


def gv_relaxation_trajectory(
    GV0: float,
    kappa: float,
    N: int,
    dt: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Minimal attractor dynamics (toy):
        dGV/dt = -kappa * GV
    so GV(t) -> 0.

    We use this as a stand-in for "relaxation toward low-GV attractor".
    """
    t = np.linspace(0.0, dt * (N - 1), N)
    GV = GV0 * np.exp(-kappa * t)
    return t, GV


def main():
    parser = argparse.ArgumentParser(description="GV Cosmology Engine (toy): potential, slow-roll, trajectory")
    parser.add_argument("--alpha", type=float, default=0.10, help="Potential slope alpha in V=V0 exp(-alpha GV)")
    parser.add_argument("--V0", type=float, default=1.0, help="Potential scale V0 (arbitrary units)")
    parser.add_argument("--GV0", type=float, default=5.0, help="Initial GV value")
    parser.add_argument("--kappa", type=float, default=0.15, help="Relaxation rate for toy GV trajectory")
    parser.add_argument("--N", type=int, default=600, help="Number of points in trajectory")
    parser.add_argument("--dt", type=float, default=0.02, help="Step size for trajectory time axis")
    parser.add_argument("--out", type=str, default="out/cosmology_engine.png", help="Output plot path")
    args = parser.parse_args()

    # 1) Slow-roll + observables
    eps, eta = slow_roll_params(args.alpha)
    ns, r = inflation_observables(args.alpha)

    # 2) Relaxation trajectory
    t, GV = gv_relaxation_trajectory(args.GV0, args.kappa, args.N, args.dt)

    # 3) Potential along trajectory
    V = V_eff(GV, args.V0, args.alpha)

    # 4) Print summary (so CI logs are meaningful)
    print("[GV Cosmology Engine]")
    print(f"alpha={args.alpha:.6g}, V0={args.V0:.6g}, GV0={args.GV0:.6g}, kappa={args.kappa:.6g}")
    print(f"slow-roll: epsilon={eps:.6g}, eta={eta:.6g}")
    print(f"observables: n_s={ns:.6g}, r={r:.6g}")
    print(f"final: GV(t_end)={GV[-1]:.6g}, V(t_end)={V[-1]:.6g}")

    # 5) Plot
    plt.figure()
    plt.plot(t, GV, label="GV(t) relax")
    plt.xlabel("t (toy)")
    plt.ylabel("GV")
    plt.title(f"GV Relaxation (alpha={args.alpha})  |  n_s={ns:.4f}, r={r:.4f}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out, dpi=250)
    print(f"[OK] Saved plot -> {args.out}")


if __name__ == "__main__":
    main()
