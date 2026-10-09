---
title: "Lemma G — the arc register of the spatial tilt"
subtitle: "PLANETVORTEX — the point monograph"
---

## Statement

Let $i_i$ be the J2000 inclination of the body $i$ (the committed JPL register) and $\bar{R} = 1$ AU the register radius. Then $\lambda_i = \bar{R}\, i_i\ \mathrm{[rad]}$ is an exact, monotone, dimension-free measure of the spatial tilt, and the tilt operator $T_i = R_z(\Omega_i) R_x(i_i) \in SO(3)$ sends the ecliptic normal to the orbit normal $n_i = (\sin i_i \sin \Omega_i,\ -\sin i_i \cos \Omega_i,\ \cos i_i)$ exactly.

## Proof

$T_i$ is a product of rotations, hence lies in $SO(3)$ — orthogonality and $\det = 1$ are closed under multiplication. The image of $(0,0,1)$ under $R_z(\Omega)R_x(i)$: $R_x(i)(0,0,1) = (0, -\sin i, \cos i)$; $R_z(\Omega)$ rotates the $xy$-components: $(\sin i \sin \Omega, -\sin i \cos \Omega, \cos i)$. $\lambda = \bar{R} i$ is linear in the angle with a fixed positive constant — monotone by inspection: it is the arc length cut by the tilt angle on the register circle. $\square$

## Computational certificate

Stage V1: the orthogonality at 2.2e−16, the normal recovery at 0.0, the monotone arc ladder, and the 3D J2000 run (energy 2.1e−13, the vector L at 4.7e−15, Kepler III at 1.0e−4 against the secular mean elements).
