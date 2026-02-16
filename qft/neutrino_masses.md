# Neutrino Masses in GV (Type-I Seesaw with Constraint Decoupling)

This module proposes a minimal GV-modification of the standard Type-I seesaw,
where GV suppresses cross-scale coupling (UV→IR feedback) between the SM lepton
doublets and heavy sterile neutrinos.

## Baseline Type-I Seesaw

Lagrangian:
\[
\mathcal{L} \supset -\, \overline{L}\, Y_\nu \,\tilde{H}\, N_R
\;-\; \frac{1}{2}\,\overline{N_R^c}\, M_R \, N_R + h.c.
\]

After EWSB: \( m_D = \frac{v}{\sqrt{2}} Y_\nu \)

Mass matrix in basis \((\nu_L, N_R^c)\):
\[
\mathcal{M}_\nu =
\begin{pmatrix}
0 & m_D \\
m_D^T & M_R
\end{pmatrix}
\]

Seesaw limit \(M_R \gg m_D\):
\[
m_\nu \approx -m_D M_R^{-1} m_D^T
\]

## GV Modification (Constraint Decoupling)

Introduce a GV-dependent suppression on the portal coupling:
\[
Y_\nu \rightarrow Y_\nu^{\text{eff}}(GV) = Y_\nu \, \mathcal{S}(GV)
\]

Toy closures for \(\mathcal{S}(GV)\):
1) Amplitude-only:
\[
\mathcal{S}(GV)=\left(\frac{GV_0}{GV}\right)^p
\]

2) Gradient-driven:
\[
\mathcal{S}(GV)=\exp\left(-\beta |\nabla GV|^2\right)
\]

Then:
\[
m_D(GV)=\frac{v}{\sqrt{2}} Y_\nu \mathcal{S}(GV)
\]

GV-modified seesaw mass:
\[
m_\nu(GV)\approx -m_D(GV) M_R^{-1} m_D^T(GV)
\]

If \(\mathcal{S}\) is scalar:
\[
m_\nu(GV)\approx \mathcal{S}^2(GV)\, m_\nu^{(0)}
\]

## GV-Seesaw Matrix (final form)

\[
\mathcal{M}_\nu(GV)=
\begin{pmatrix}
0 & m_D\,\mathcal{S}(GV) \\
\mathcal{S}^T(GV)\, m_D^T & M_R
\end{pmatrix}
\]

## Program / Tests

- Choose \(\mathcal{S}(GV)\) closure and define typical scales for \(GV\) and \(|\nabla GV|\).
- Compute implied \(\Sigma m_\nu\) and compare to cosmological bounds.
- Extend \(\mathcal{S}\) to a flavor-dependent structure to generate PMNS mixing.
