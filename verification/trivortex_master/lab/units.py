#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Системы единиц лаборатории: СИ, астрономическая, модельная (G=1).

Конверсии между системами для пресетов macro/micro и отчётов.
"""

AU_M = 1.495978707e11
M_SUN = 1.9884e30
M_EARTH = 5.9722e24
DAY_S = 86400.0
YEAR_S = 365.25 * DAY_S


# модельная система: длина = 1 а.е., время = 1 год/N_орбит, масса = M_sun
def si_to_model(pos, vel, mass, time_scale=YEAR_S):
    return (tuple(c / AU_M for c in pos), tuple(v / (AU_M / time_scale) for v in vel), mass / M_SUN)


def model_to_si(pos, vel, mass, time_scale=YEAR_S):
    return (tuple(c * AU_M for c in pos), tuple(v * (AU_M / time_scale) for v in vel), mass * M_SUN)


def to_astronomical_units(meters):
    return meters / AU_M


def format_si(value, unit="м"):
    """Человекочитаемая запись с приставками СИ."""
    steps = [
        (1e24, "Y"),
        (1e21, "Z"),
        (1e18, "E"),
        (1e15, "P"),
        (1e12, "T"),
        (1e9, "G"),
        (1e6, "M"),
        (1e3, "k"),
        (1,),
        (1e-3, "m"),
        (1e-6, "µ"),
        (1e-9, "n"),
        (1e-12, "p"),
    ]
    for factor, *prefix in steps:
        p = prefix[0] if prefix else ""
        if abs(value) >= factor:
            return f"{value/factor:.3g} {p}{unit}"
    return f"{value:.3g} {unit}"
