#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test bootstrap: make the polyvortex package and the parent Trivortex
ladder importable. The parent ladder is imported ONLY by the
cross-validation tests — the mini-repository never imports it at
runtime (independence discipline, see docs/monograph.md Section 1)."""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "python")))
sys.path.insert(
    0,
    os.path.normpath(os.path.join(HERE, "..", "..", "verification", "trivortex", "python")),
)
