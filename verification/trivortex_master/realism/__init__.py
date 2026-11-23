#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
realism — слой реальных движков и данных NASA.

Пакет инжектирует адаптеры REBOUND/Dedalus/Custom в диспетчер lab.physics
при своём импорте (register_engine), сохраняя однонаправленность графа:
realism → lab, и никогда обратно.
"""


def _inject_engines() -> None:
    """Регистрация адаптеров в lab.physics (best-effort)."""
    try:
        from lab.physics import register_engine
    except ImportError:
        return
    try:
        from realism.adapters.rebound_adapter import REBOUNDAdapter

        register_engine("rebound", REBOUNDAdapter)
    except Exception:
        pass
    try:
        from realism.adapters.dedalus_adapter import DedalusAdapter

        register_engine("dedalus", DedalusAdapter)
    except Exception:
        pass
    try:
        from realism.adapters.custom_adapter import CustomEngine

        register_engine("custom", CustomEngine)
    except Exception:
        pass


_inject_engines()
