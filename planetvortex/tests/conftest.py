#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test bootstrap: make the planetvortex package importable, plus the
sibling polyvortex package as the cross-validation oracle. The sibling
is imported ONLY by the cross-pin tests — the mini-repository never
imports it at runtime (the independence discipline of the framework)."""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "python")))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "polyvortex", "python")))
