import numpy as np

def S_amp(GV, GV0=1.0, p=1.0):
    return (GV0 / GV) ** p

def seesaw_mnu(Ynu, MR, GV=1.0, v=246.0, GV0=1.0, p=1.0):
    # mD = v/sqrt(2) * Ynu * S(GV)
    S = S_amp(GV, GV0=GV0, p=p)
    mD = (v / np.sqrt(2.0)) * Ynu * S
    # mnu = - mD MR^{-1} mD^T
    MR_inv = np.linalg.inv(MR)
    return -mD @ MR_inv @ mD.T

if __name__ == "__main__":
    # Simple 3x3 demo: diagonal MR, small Yukawas
    Ynu = np.diag([1e-6, 2e-6, 3e-6])
    MR  = np.diag([1e12, 2e12, 3e12])  # GeV-ish scale toy
    for GV in [0.5, 1.0, 2.0, 5.0]:
        mnu = seesaw_mnu(Ynu, MR, GV=GV, p=1.0)
        evals = np.linalg.eigvalsh(mnu)
        print(f"GV={GV:>4}: eigenvalues ~ {evals}")
