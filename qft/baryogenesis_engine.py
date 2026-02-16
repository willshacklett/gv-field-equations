import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--gv-min", type=float, default=0.1)
parser.add_argument("--gv-max", type=float, default=10)
parser.add_argument("--n", type=int, default=400)
parser.add_argument("--alpha", type=float, default=1.0)
parser.add_argument("--T", type=float, default=100)  # temperature scale
parser.add_argument("--out", type=str, default=None)
args = parser.parse_args()

gv_vals = np.linspace(args.gv_min, args.gv_max, args.n)

# Toy free energy landscape
def free_energy(gv, theta):
    return 0.5 * gv * theta**2 + args.alpha * theta**4

def theta_dot(gv, theta):
    # gradient flow relaxation
    dF_dtheta = gv * theta + 4 * args.alpha * theta**3
    return -dF_dtheta

# Assume small initial theta displacement
theta0 = 0.1
theta_rates = np.array([theta_dot(gv, theta0) for gv in gv_vals])

# Toy BAU scaling
eta_B = theta_rates / args.T

plt.figure()
plt.plot(gv_vals, eta_B)
plt.axhline(6e-10, linestyle="--", label="Observed BAU ~6e-10")
plt.xlabel("GV")
plt.ylabel("η_B (toy)")
plt.title("GV-Driven Baryogenesis Toy Model")
plt.legend()

if args.out:
    plt.savefig(args.out)
else:
    plt.show()

print("Sample η_B values:")
print(eta_B[:5])
