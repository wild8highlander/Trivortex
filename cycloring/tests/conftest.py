#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test bootstrap: make the cycloring package importable.

The mini-repository is self-contained: it imports nothing from the parent
framework — the tests exercise only the cycloring modules themselves."""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "python")))
