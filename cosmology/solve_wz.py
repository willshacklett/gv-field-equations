#!/usr/bin/env python3
"""
GV w(z) numerical solver (toy v1)

Model: canonical scalar GV with exponential potential V = V0 * exp(-lambda * GV)
Flat universe with matter + radiation + GV.
Integrate in N = ln(a). Output w(z), H(z) (dimensionless), Omega's.

Units:
- Use reduced Planck units with 8*pi*G = 1 (so M_pl = 1/sqrt(8*pi*G) = 1).
- Then Friedmann: H^2 = (1/3) * rho_total.
"""

import math
import argparse

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def V(phi, V0, lam):
    return V0 * math.exp(-lam * phi)


def dV_dphi(phi, V0, lam):
    return -lam * V(phi, V0, lam)


def deriv(N, y, params):
    """
    State y = [phi, pi, rho_m, rho_r]
    where pi = dphi/dt, N = ln a

    d/dN = (1/H) d/dt
    """
    phi, pi, rho_m, rho_r = y
    V0, lam = params["V0"], params["lam"]

    Vphi = V(phi, V0, lam)
    rho_phi = 0.5 * pi * pi + Vphi

    rho_tot = rho_m + rho_r + rho_phi
    H = math.sqrt(rho_tot / 3.0)

    # Equations:
    # dphi/dt = pi
    # dpi/dt = -3H pi - dV/dphi
    # drho_m/dt = -3H rho_m
    # drho_r/dt = -4H rho_r
    #
    # Convert to d/dN = (1/H) d/dt:
    dphi_dN = pi / H
    dpi_dN = (-3.0 * H * pi - dV_dphi(phi, V0, lam)) / H
    drho_m_dN = (-3.0 * H * rho_m) / H
    drho_r_dN = (-4.0 * H * rho_r) / H

    return [dphi_dN, dpi_dN, drho_m_dN, drho_r_dN]


def rk4_step(f, x, y, h, params):
    k1 = f(x, y, params)
    y2 = [yi + 0.5 * h * k1i for yi, k1i in zip(y, k1)]
    k2 = f(x + 0.5 * h, y2, params)
    y3 = [yi + 0.5 * h * k2i for yi, k2i in zip(y, k2)]
    k3 = f(x + 0.5 * h, y3, params)
    y4 = [yi + h * k3i for yi, k3i in zip(y, k3)]
    k4 = f(x + h, y4, params)

    return [yi + (h / 6.0) * (k1i + 2*k2i + 2*k3i + k4i)
            for yi, k1i, k2i, k3i, k4i in zip(y, k1, k2, k3, k4)]


def run_solver(
    lam=0.2,
    V0=0.7,
    phi0=0.0,
    pi0=0.0,
    Omega_m0=0.3,
    Omega_r0=9e-5,
    N_min=-7.0,
    N_max=0.0,
    dN=1e-3,
):
    """
    Initialize at N=0 (today) and integrate backward to N_min, then reverse arrays
    for clean plotting in increasing time (increasing N).
    """

    # In our units: H0^2 = rho0/3. Choose H0=1 => rho0 = 3.
    # Then set present-day densities:
    rho0 = 3.0
    rho_m0 = Omega_m0 * rho0
    rho_r0 = Omega_r0 * rho0
    # GV gets the remainder:
    rho_phi0 = rho0 - rho_m0 - rho_r0
    if rho_phi0 <= 0:
        raise ValueError("Omega_m0 + Omega_r0 must be < 1.")

    # If pi0 given, V(phi0) must match rho_phi0 - 0.5 pi0^2
    V_needed = rho_phi0 - 0.5 * pi0 * pi0
    if V_needed <= 0:
        raise ValueError("pi0 too large; leaves negative potential energy.")

    # Override V0 so that V(phi0) matches V_needed:
    # V(phi0) = V0 * exp(-lam*phi0) => V0 = V_needed * exp(lam*phi0)
    V0 = V_needed * math.exp(lam * phi0)

    params = {"lam": lam, "V0": V0}

    # Integrate BACKWARD in N from 0 down to N_min
    N = 0.0
    y = [phi0, pi0, rho_m0, rho_r0]

    Ns = [N]
    phis = [y[0]]
    pis = [y[1]]
    rhos_m = [y[2]]
    rhos_r = [y[3]]
    wvals = []
    Hvals = []
    Omegas_phi = []
    Omegas_m = []
    Omegas_r = []

    def record(N, y):
        phi, pi, rho_m, rho_r = y
        Vphi = V(phi, params["V0"], params["lam"])
        rho_phi = 0.5*pi*pi + Vphi
        p_phi = 0.5*pi*pi - Vphi
        w = p_phi / rho_phi
        rho_tot = rho_m + rho_r + rho_phi
        H = math.sqrt(rho_tot/3.0)
        Om_phi = rho_phi / rho_tot
        Om_m = rho_m / rho_tot
        Om_r = rho_r / rho_tot
        wvals.append(w)
        Hvals.append(H)
        Omegas_phi.append(Om_phi)
        Omegas_m.append(Om_m)
        Omegas_r.append(Om_r)

    record(N, y)

    steps = int(abs((N_min - N_max) / dN)) if dN > 0 else 0
    h = -abs(dN)  # backward
    for _ in range(steps):
        if N + h < N_min:
            break
        y = rk4_step(deriv, N, y, h, params)
        N += h

        Ns.append(N)
        phis.append(y[0])
        pis.append(y[1])
        rhos_m.append(y[2])
        rhos_r.append(y[3])
        record(N, y)

    # Reverse to increasing N (early -> now)
    Ns = Ns[::-1]
    phis = phis[::-1]
    pis = pis[::-1]
    rhos_m = rhos_m[::-1]
    rhos_r = rhos_r[::-1]
    wvals = wvals[::-1]
    Hvals = Hvals[::-1]
    Omegas_phi = Omegas_phi[::-1]
    Omegas_m = Omegas_m[::-1]
    Omegas_r = Omegas_r[::-1]

    # Convert N to redshift z: a = e^N, z = 1/a - 1
    zs = [(math.exp(-N) - 1.0) for N in Ns]

    return {
        "params": params,
        "N": Ns,
        "z": zs,
        "phi": phis,
        "pi": pis,
        "w": wvals,
        "H": Hvals,
        "Omega_phi": Omegas_phi,
        "Omega_m": Omegas_m,
        "Omega_r": Omegas_r,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam", type=float, default=0.2, help="lambda in V=V0 exp(-lam GV)")
    ap.add_argument("--phi0", type=float, default=0.0, help="GV today")
    ap.add_argument("--pi0", type=float, default=0.0, help="dGV/dt today")
    ap.add_argument("--Omega_m0", type=float, default=0.3, help="matter fraction today")
    ap.add_argument("--Omega_r0", type=float, default=9e-5, help="radiation fraction today")
    ap.add_argument("--N_min", type=float, default=-7.0, help="start ln(a)")
    ap.add_argument("--dN", type=float, default=1e-3, help="step in ln(a)")
    ap.add_argument("--no_plot", action="store_true")
    args = ap.parse_args()

    out = run_solver(
        lam=args.lam,
        phi0=args.phi0,
        pi0=args.pi0,
        Omega_m0=args.Omega_m0,
        Omega_r0=args.Omega_r0,
        N_min=args.N_min,
        N_max=0.0,
        dN=args.dN,
    )

    p = out["params"]
    print("=== GV w(z) toy solver ===")
    print(f"lambda = {p['lam']}")
    print(f"V0     = {p['V0']}  (set to match Omega_phi0)")
    print("Sample points (z, w, Omega_phi):")
    for z_target in [0, 0.5, 1, 2, 5, 10]:
        # find nearest
        idx = min(range(len(out["z"])), key=lambda i: abs(out["z"][i] - z_target))
        print(f"  z~{out['z'][idx]:.3f}:  w={out['w'][idx]:.4f},  Om_phi={out['Omega_phi'][idx]:.4f}")

    if args.no_plot:
        return

    if plt is None:
        print("matplotlib not available; rerun with --no_plot or install matplotlib.")
        return

    # Plot w(z)
    plt.figure()
    plt.plot(out["z"], out["w"])
    plt.gca().invert_xaxis()  # show early universe on left if you like; comment out if not
    plt.xlabel("z")
    plt.ylabel("w(z)")
    plt.title("GV Dark Energy: w(z) (toy)")
    plt.grid(True)

    # Plot Omegas
    plt.figure()
    plt.plot(out["z"], out["Omega_m"], label="Omega_m")
    plt.plot(out["z"], out["Omega_r"], label="Omega_r")
    plt.plot(out["z"], out["Omega_phi"], label="Omega_GV")
    plt.gca().invert_xaxis()
    plt.xlabel("z")
    plt.ylabel("Omega_i(z)")
    plt.title("Energy Budget vs Redshift (toy)")
    plt.grid(True)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()
