#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE GAMMA-PERIOD RING LABORATORY
============================================================================
A self-contained mini-research program: the regular N-vortex ring is
algebraized (the ring IS the root system of z^N = sigma(t)), its angular
phases live on the cyclotomic lattice mu_N, and the radial modulation is
produced from Gamma-periods

    Omega_{a,b} = Gamma(a/N) Gamma(b/N) / Gamma((a+b)/N)

through the defect chain

    delta = pi/N,  k = ceil(B*lambda_0/Gamma^2),  gamma = delta^4/k,
    delta_eff = delta^5/k,  Delta_Ch = gamma * W_N / (N - 1),

and the transducer map

    eps = Delta/(1 + Delta),   nu = omega_L ((1 + Delta)/(1 + 2 Delta))^{3/2},
    C_N = ln(1 + 1/Delta) = -ln(eps).

Modules
-------
periods   the Gamma-period core: Omega, the reflection register, the sine
          product, the normalized periods P(a, b) and the witness W_N
chain     the defect chain and the period transducer (the modulation map)
ring      the root system of the ring, character modes, the pumped
          synchronous-breathing program and its rosettes
dynamics  the Kirchhoff point-vortex layer (RK4, H/P/Q/I, Jacobian)
ladder    the verification-and-research ladder W1..W7
runner    the JSON protocol CLI
figures   the publication figure factory (protocol-bound)

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from . import chain, dynamics, periods, ring

__all__ = ["periods", "chain", "ring", "dynamics"]
__version__ = "1.0.0"
