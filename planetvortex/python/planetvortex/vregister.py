#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE V-REGISTER: THE SPATIAL AND KLEIN LAYERS (V1..V2)
============================================================================
The verification ladder of the roadmap's spatial turn. Where the
P-ladder registers the planar science and the X-register attacks it,
the V-register lifts the bench onto the roadmap's two remaining posts:

    V1  the spatial registers: the SO(3) tilt algebra of the 11-body
        inclination register, the arc registers lambda = R_bar * i,
        the mutual-inclination matrix, and the full 3D Newtonian Sun +
        8-planets run from the real J2000 sky (spatial.py)
    V2  the closed gravifigure: the full 24-heptagon tessellation
        {7,3}_8 of the Klein quartic as the coset geometry of the
        certified PSL(2,7), the PGL(2,7) flag certificate, the
        chamber-grown disk patch, the 12-body gravimetric register
        with its EXACT budget closure sum(alpha_i) = 8*pi (klein.py)

The same house discipline as everywhere in the repository: a
tolerance committed before the recorded run and a deterministic JSON
protocol after it.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

from typing import Any, Dict

from . import klein as kl
from . import spatial as sp

CHECK_FUNCS = {
    "V1": lambda cfg: sp.check_v1_inclined(
        years=cfg["v1"]["years"],
        dt=cfg["v1"]["dt"],
        sample_every=cfg["v1"]["sample_every"],
    ),
    "V2": lambda cfg: kl.check_v2_klein_tiling(
        dps=cfg["v2"]["dps"],
        ceiling_margin=cfg["v2"]["ceiling_margin"],
    ),
}

PRESETS: Dict[str, Dict[str, Any]] = {
    "quick": {
        **sp.V1_PRESETS["quick"],
        **kl.V2_PRESETS["quick"],
        "v1": sp.V1_PRESETS["quick"],
        "v2": kl.V2_PRESETS["quick"],
    },
    "default": {
        **sp.V1_PRESETS["default"],
        **kl.V2_PRESETS["default"],
        "v1": sp.V1_PRESETS["default"],
        "v2": kl.V2_PRESETS["default"],
    },
    "full": {
        **sp.V1_PRESETS["full"],
        **kl.V2_PRESETS["full"],
        "v1": sp.V1_PRESETS["full"],
        "v2": kl.V2_PRESETS["full"],
    },
}


def run_v_register(preset: str = "default") -> Dict[str, Any]:
    """Run the whole V-register with the given preset (in-process)."""
    cfg = PRESETS[preset]
    v1 = sp.check_v1_inclined(**cfg["v1"])
    v2 = kl.check_v2_klein_tiling(**cfg["v2"])
    return {
        "preset": preset,
        "V1": v1,
        "V2": v2,
        "all_passed": bool(v1["passed"] and v2["passed"]),
    }
