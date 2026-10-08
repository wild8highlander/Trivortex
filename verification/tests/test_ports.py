#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pytest guard for the multi-language verification ports (M1–M3).

The toolchain-agnostic layer of the port contract: the Python CI has no
Rust/C++ toolchains installed, so this suite checks what is checkable
without them —

  1. every planned artifact of the roadmap landed where its stub said it
     would land (Coq/Lean/Isabelle/Agda/Rust/C++/Haskell + the lab);
  2. the committed reference protocols of the executed ports
     (Rust, C++) parse and carry the registered JSON schema;
  3. the reference numbers inside those protocols agree with the Python
     ladder's pins inside the registered tolerance bands — the ports are
     "pinned, not assumed", exactly like the analytic-layer tests of
     test_trivortex.py.

Run from the repository root:
    python -m pytest verification/tests/test_ports.py -v
"""

import importlib.util
import json
import math
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # repository root
VERIFY = os.path.join(ROOT, "verification")

# The Python ladder, for cross-language pinning of the reference numbers.
_spec = importlib.util.spec_from_file_location(
    "trivortex_verify",
    os.path.join(VERIFY, "trivortex", "python", "verify.py"),
)
tv = importlib.util.module_from_spec(_spec)
sys.modules["trivortex_verify"] = tv
_spec.loader.exec_module(tv)


# ---------------------------------------------------------------------------
# 1. Artifact presence — the roadmap stubs' planned artifacts landed
# ---------------------------------------------------------------------------

PLANNED_ARTIFACTS = [
    # Coq (M1): the statement layer
    "coq/Trivortex.v",
    # Lean 4 (M1): the Mathlib formalization + project files
    "lean4/Trivortex.lean",
    "lean4/lakefile.lean",
    "lean4/lean-toolchain",
    # Rust (M1): the numeric twin crate
    "rust/Cargo.toml",
    "rust/src/verify.rs",
    "rust/src/main.rs",
    "rust/src/lib.rs",
    "rust/tests/ladder.rs",
    # Isabelle (M2): the HOL formalization + optional SMT bounds
    "isabelle/Trivortex.thy",
    "isabelle/Trivortex_SMT.thy",
    "isabelle/ROOT",
    # Agda (M2): the constructive angle arithmetic
    "agda/Trivortex.agda",
    # C++ (M3): the CMake/CTest port + benchmark
    "cpp/CMakeLists.txt",
    "cpp/src/verify.hpp",
    "cpp/src/verify.cpp",
    "cpp/src/main.cpp",
    "cpp/src/tests.cpp",
    # Haskell (M3): the Double vs exact-rational dual ladder
    "haskell/trivortex-verify.cabal",
    "haskell/src/Trivortex/Verify.hs",
    "haskell/app/Main.hs",
    "haskell/test/Ladder.hs",
    # the Python scientific laboratory (the M0 bench, extended)
    "trivortex/python/lab.py",
    # committed reference protocols of the executed ports
    "rust/protocol_quick.json",
    "cpp/protocol_quick.json",
]


class TestPortArtifacts:
    @pytest.mark.parametrize("relpath", PLANNED_ARTIFACTS)
    def test_artifact_present(self, relpath):
        path = os.path.join(VERIFY, relpath)
        assert os.path.isfile(path), f"planned port artifact missing: {relpath}"
        assert os.path.getsize(path) > 0, f"planned port artifact empty: {relpath}"

    def test_bilingual_readmes_landed(self):
        for lang in ("coq", "lean4", "rust", "isabelle", "agda", "cpp", "haskell"):
            en = os.path.join(VERIFY, lang, "README.md")
            ru = os.path.join(VERIFY, lang, "README_RU.md")
            assert os.path.isfile(en), f"missing {lang}/README.md"
            assert os.path.isfile(ru), f"missing {lang}/README_RU.md (bilingual contract)"

    def test_spdx_headers_present(self):
        # the acceptance criteria of every stub require SPDX + copyright
        # lines in the artifact headers
        required = {
            "rust/src/verify.rs": "SPDX-License-Identifier",
            "cpp/src/verify.cpp": "SPDX-License-Identifier",
            "haskell/src/Trivortex/Verify.hs": "SPDX-License-Identifier",
            "coq/Trivortex.v": "SPDX-License-Identifier",
            "lean4/Trivortex.lean": "SPDX-License-Identifier",
            "isabelle/Trivortex.thy": "SPDX-License-Identifier",
            "agda/Trivortex.agda": "SPDX-License-Identifier",
        }
        for relpath, marker in required.items():
            with open(os.path.join(VERIFY, relpath), encoding="utf-8") as f:
                head = f.read(4000)
            assert marker in head, f"no SPDX header in {relpath}"
            assert "Isaev Iskhak Khamzatovich" in head, f"no copyright line in {relpath}"


# ---------------------------------------------------------------------------
# 2. Reference protocols — schema of verification/README.md §12
# ---------------------------------------------------------------------------


def load_protocol(lang: str) -> dict:
    with open(os.path.join(VERIFY, lang, "protocol_quick.json"), encoding="utf-8") as f:
        return json.load(f)


class TestPortProtocols:
    @pytest.mark.parametrize("lang", ["rust", "cpp"])
    def test_protocol_schema(self, lang):
        report = load_protocol(lang)
        for key in (
            "suite",
            "version",
            "preset",
            "date_utc",
            "wall_time_s",
            "checks_passed",
            "checks_total",
            "all_passed",
            "checks",
        ):
            assert key in report, f"{lang}: protocol missing field {key}"
        assert report["preset"] == "quick"
        assert report["all_passed"] is True
        assert report["checks_total"] == 4
        assert len(report["checks"]) == 4

    @pytest.mark.parametrize("lang", ["rust", "cpp"])
    def test_protocol_matches_python_verdicts(self, lang):
        report = load_protocol(lang)
        for c in report["checks"]:
            assert c["passed"] is True, f"{lang}: a check failed in the committed protocol"

    @pytest.mark.parametrize("lang", ["rust", "cpp"])
    def test_protocol_matches_python_reference_numbers(self, lang):
        """Cross-language pinning: the ports must agree with the Python
        ladder inside the registered tolerance bands (README §6)."""
        report = load_protocol(lang)
        by_prefix = {}
        for c in report["checks"]:
            by_prefix[c["check"].split()[0]] = c

        # V1 — closed-form residuals inside 1e-12
        v1 = by_prefix["V1"]
        assert v1["angular_separation_error"] <= 1e-12
        assert v1["periodicity_residual"] <= 1e-12

        # V2 — shape 1e-10, omega 1e-6, and the analytic omega pin
        v2 = by_prefix["V2"]
        assert v2["shape_drift"] <= 1e-10
        assert v2["omega_relative_error"] <= 1e-6
        ref_omega = tv.lagrange_omega(1.0, 1.0)
        assert v2["omega_analytic"] == pytest.approx(ref_omega, rel=1e-12)
        assert ref_omega == pytest.approx(0.477464829275686, rel=1e-12)

        # V3/V4 — invariant drifts inside 1e-10
        assert by_prefix["V3"]["worst_drift"] <= 1e-10
        assert by_prefix["V4"]["worst_drift"] <= 1e-10

        # V3 drifts also agree with the Python quick ladder run, loosely:
        # different libm calls give different last bits, so compare against
        # the tolerance, not bit-for-bit (documented in the port READMEs).
        quick_v3 = tv.check_v3_invariants(
            rotations=tv.PRESETS["quick"]["rotations"],
            steps_per_period=tv.PRESETS["quick"]["steps_per_period"],
        )
        assert quick_v3["passed"] is True
        assert by_prefix["V3"]["worst_drift"] <= quick_v3["tolerance"]


# ---------------------------------------------------------------------------
# 3. The Python laboratory — importability and the CI smoke entry
# ---------------------------------------------------------------------------


def load_lab():
    path = os.path.join(VERIFY, "trivortex", "python", "lab.py")
    spec = importlib.util.spec_from_file_location("trivortex_lab", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["trivortex_lab"] = mod
    spec.loader.exec_module(mod)
    return mod


class TestPythonLaboratory:
    def test_lab_imports_and_bilingual_strings(self):
        lab = load_lab()
        for lang in ("en", "ru"):
            s = lab.STRINGS[lang]
            for key in ("title", "menu", "m1", "m0", "result", "bye"):
                assert key in s, f"lab: missing string {key} for {lang}"

    def test_lab_reference_helpers(self):
        lab = load_lab()
        # the convergence study runs end-to-end (mirrors V2 with 2 rotations)
        rows = lab.convergence_study()
        assert [r["steps_per_period"] for r in rows] == [250, 500, 1000, 2000, 4000, 8000]
        for r in rows:
            # the measured omega stays inside its registered band on every grid
            assert r["omega_rel_err"] <= 1e-6
            # the shape band 1e-10 holds from ~1000 steps/period up; the
            # low grids are precisely where the study shows the RK4 error
            # still converging — that is the point of the analysis
            if r["steps_per_period"] >= 1000:
                assert r["shape_drift"] <= 1e-10

    def test_lab_invariant_drift_scan_passes(self):
        lab = load_lab()
        scan = lab.invariant_drift_scan(rotations=2, steps_per_period=1000)
        # every monitored snapshot stays inside the registered band
        for key in ("dH", "dP", "dQ", "dI"):
            assert max(scan[key]) <= 1e-10
