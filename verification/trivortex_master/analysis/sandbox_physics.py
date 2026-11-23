#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Библиотека готовых физических сил для CustomEngine.

Каждая функция возвращает ускорение (ax, ay, az) по состоянию тела
(x,y,z,vx,vy,vz,t,m,q,G,r). Подключаются строкой-выражением в меню.
"""

DRAG_LINEAR = "-0.05*vx"  # линейное трение
DRAG_QUADRATIC = "-0.01*vx*abs(vx)"  # квадратичное трение
HARMONIC = "-2.0*x"  # гармоническая яма
COULOMB_LIKE = "-0.5*q*x/(r**3)"  # кулоновское отталкивание
YARKOVSKY_LIKE = "0.001*cos(t)*x/r"  # радиационная добавка
PRESET_FORCES = {
    "drag_linear": DRAG_LINEAR,
    "drag_quadratic": DRAG_QUADRATIC,
    "harmonic": HARMONIC,
    "coulomb": COULOMB_LIKE,
    "yarkovsky": YARKOVSKY_LIKE,
}
