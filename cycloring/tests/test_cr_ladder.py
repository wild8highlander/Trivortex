#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The W-ladder end-to-end: every stage passes on the quick preset and
produces the protocol-shaped dictionary."""

from __future__ import annotations

import math

import pytest

from cycloring import ladder

STAGES = ("W1", "W2", "W3", "W4", "W5", "W6", "W7")


@pytest.mark.parametrize("stage", STAGES)
def test_stage_passes(stage: str) -> None:
    result = ladder.run_stage(stage, "quick")
    assert result["passed"] is True, f"{stage} failed: {result}"


def test_protocol_schema() -> None:
    """Every stage returns the check-dictionary discipline."""
    result = ladder.run_stage("W7", "quick")
    for key in ("check", "params", "passed"):
        assert key in result
    table = result["table"]
    assert len(table) == 4
    assert {row["N"] for row in table} == {7, 9, 15, 30}
    for row in table:
        for key in ("k", "delta", "gamma", "delta_eff", "W", "Delta_Ch", "eps", "nu_ratio", "C_N"):
            assert key in row


def test_registered_level_values() -> None:
    """The registered anchors of the transducer table (bit-pinning)."""
    result = ladder.run_stage("W7", "quick")
    table = {row["N"]: row for row in result["table"]}
    assert table[7]["k"] == 4
    assert table[9]["k"] == 6
    assert table[15]["k"] == 17
    assert table[30]["k"] == 70
    # W_7 to 1e-6: the diagonal period sum of the level
    assert table[7]["W"] == pytest.approx(2.1754436, abs=1e-5)
    # eps_7 = Delta/(1+Delta) with Delta = gamma * W_7 / 6
    assert table[7]["eps"] == pytest.approx(3.664e-3, abs=1e-5)


def test_transport_identity_anchor() -> None:
    """The transport identity at eps = 1/2: (1 - 1/4)^{-3/2} = 8/(3 sqrt(3))."""
    from cycloring import ring as rg

    value = rg.mean_transport_ratio(0.5)
    expected = 8.0 / (3.0 * math.sqrt(3.0))
    assert value == pytest.approx(expected, rel=1e-10)
