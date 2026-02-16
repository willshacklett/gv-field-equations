import numpy as np
import matplotlib.pyplot as plt

# Constants (toy values)
v = 246  # Higgs vev in GeV
y_nu = 1e-5  # toy Yukawa
M0 = 1e14  # base RH neutrino scale (GeV)
beta = 2.0  # GV coupling strength

# GV range
GV = np.linspace(0, 3, 400)

# Dirac mass
mD = y_nu * v

# GV-modified heavy scale
MR = M0 * np.exp(beta * GV)

# Light neutrino mass (eV scale)
m_nu = (mD**2 / MR) * 1e9  # convert GeV to eV approx

plt.figure()
plt.plot(GV, m_nu)
plt.xlabel("GV")
plt.ylabel("m_ν (eV)")
plt.title("GV-Modified Neutrino Seesaw")
plt.yscale("log")
plt.grid(True)
plt.show()

print(f"m_nu(GV=0) = {m_nu[0]:.3e} eV")
print(f"m_nu(GV=3) = {m_nu[-1]:.3e} eV")
