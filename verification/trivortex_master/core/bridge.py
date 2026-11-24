#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — мост к ядру репозитория Trivortex.

Изолирует все касания code/ + verification/ + research/, чтобы при изменении
API правился только этот файл. Если копия репозитория не найдена — мастер
работает в автономном режиме (CoreStatus.available = False).
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field

# Эталонные значения Теоремы 3.1 при C_Ch = 1, T = 2π.
# Формулы — из кода репозитория (verification/trivortex/python/verify.py,
# analytical_frequency/analytical_amplitude; тест test_trivortex.py пинит
# самосогласованность с ними). Примечание: табличное значение ε в README
# репозитория исправлено 2026-11-23 на 2.6680737914285615 (ранее стояло
# 0.7276…, что не согласовалось с формулой) — мастер следует коду.
THEOREM31_REF = {
    "omega": 1.3748022274393588,  # ω = (2π/T)·e^(1/π)
    "epsilon": 2.6680737914285615,  # ε = 1/(e^(1/π) − 1)
    "angular_separation_tol": 1e-12,  # V1: разделение 2π/3
    "periodicity_tol": 1e-12,  # V1: периодичность
    "readme_eps_erratum": "README §11: ε исправлено 2026-11-23 на "
    "2.6680737914285615 (ранее 0.7276379117656014)",
}

# Порог Хавелока (POLYVORTEX, стадия W4)
HAVelock_REF = {
    "stable_max": 7,
    "unstable_min": 8,
    "lambda_max_N8": 0.4502,
}

LADDER_LEVELS = ["V1", "V2", "V3", "V4"]

_TRIVORTEX_CANDIDATES = [
    os.environ.get("TRIVORTEX_HOME", ""),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Trivortex"),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".trivortex"),
    os.path.expanduser("~/Trivortex"),
]


@dataclass
class CoreStatus:
    """Снимок доступности ядра."""

    available: bool = False
    core_path: str | None = None
    verification_path: str | None = None
    research_path: str | None = None
    theorem31_refs: dict = field(default_factory=lambda: dict(THEOREM31_REF))
    ladder_levels: list[str] = field(default_factory=lambda: list(LADDER_LEVELS))
    havelock: dict = field(default_factory=lambda: dict(HAVelock_REF))
    errors: list[str] = field(default_factory=list)
    autonomous: bool = True


@dataclass
class VerificationResult:
    """Результат прогона лестницы verify.py."""

    level: str = ""
    passed: bool = False
    metrics: dict = field(default_factory=dict)
    log: str = ""
    preset: str = "default"
    protocol_path: str | None = None


def find_trivortex() -> str | None:
    """Поиск локальной копии репозитория Trivortex."""
    for cand in _TRIVORTEX_CANDIDATES:
        if not cand:
            continue
        if os.path.isfile(os.path.join(cand, "code", "trivortex_core_en.py")) or os.path.isfile(
            os.path.join(cand, "code", "trivortex_core.py")
        ):
            return os.path.abspath(cand)
    return None


_CORE_MODULE = None


def load_core():
    """Импорт code/trivortex_core_en.py (или ru/общей версии) как модуля."""
    global _CORE_MODULE
    if _CORE_MODULE is not None:
        return _CORE_MODULE
    root = find_trivortex()
    if root is None:
        raise ImportError(
            "локальная копия Trivortex не найдена; "
            "задайте TRIVORTEX_HOME или склонируйте репозиторий "
            "рядом с trivortex_master/"
        )
    for name in ("trivortex_core_en.py", "trivortex_core.py", "trivortex_core_ru.py"):
        path = os.path.join(root, "code", name)
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location("trv_core", path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules["trv_core"] = mod
            try:
                spec.loader.exec_module(mod)
            except Exception as exc:  # ядро тянет numpy/scipy — их может не быть
                raise ImportError(f"ядро Trivortex не импортировалось: {exc}")
            _CORE_MODULE = mod
            return mod
    raise ImportError("в code/ нет trivortex_core*.py")


def get_theorem31_reference() -> dict:
    """Эталонные значения (ω, ε) для валидации планировщика Теоремы 3.1."""
    return dict(THEOREM31_REF)


def get_havelock_reference() -> dict:
    """Return the pinned Havelock reference: N<=7 stable, N=8 max Re lambda = +0.4502."""
    return dict(HAVelock_REF)


def get_ladder_levels() -> list[str]:
    """Return the verification-ladder levels V1-V4 with their tolerances."""
    return list(LADDER_LEVELS)


def health_check() -> CoreStatus:
    """Целостность ядра: пути, лестница, исследовательские протоколы."""
    st = CoreStatus()
    root = find_trivortex()
    if root is None:
        st.errors.append("копия Trivortex не найдена (автономный режим)")
        return st
    st.core_path = root
    st.available = True
    st.autonomous = False

    verif = os.path.join(root, "verification", "trivortex", "python", "verify.py")
    st.verification_path = verif if os.path.isfile(verif) else None
    if st.verification_path is None:
        st.errors.append("verify.py не найден — лестница V1–V4 недоступна")

    research = os.path.join(root, "research")
    st.research_path = research if os.path.isdir(research) else None
    if st.research_path is None:
        st.errors.append("каталог research/ не найден")

    try:
        load_core()
    except ImportError as exc:
        st.errors.append(str(exc))
    return st


def run_verification(mode: str = "quick", timeout: float = 300.0) -> VerificationResult:
    """
    Прогон verification/trivortex/python/verify.py с парсингом JSON-протокола.

    mode: quick (≈0.5 с) | default (≈2 с) | full (≈35 с)
    """
    root = find_trivortex()
    if root is None:
        return VerificationResult(
            passed=False,
            log="репозиторий Trivortex не найден — " "верификация недоступна в автономном режиме",
        )
    script = os.path.join(root, "verification", "trivortex", "python", "verify.py")
    if not os.path.isfile(script):
        return VerificationResult(passed=False, log=f"verify.py не найден: {script}")
    cmd = [sys.executable, script, "--preset", mode]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=os.path.dirname(script)
        )
    except subprocess.TimeoutExpired:
        return VerificationResult(passed=False, log=f"таймаут {timeout:.0f} с")
    except OSError as exc:
        return VerificationResult(passed=False, log=str(exc))

    result = VerificationResult(level="V1-V4", preset=mode, log=(proc.stdout or "")[-4000:])
    # парсинг JSON-протокола из вывода (последний {...}-блок)
    if proc.returncode == 0:
        result.passed = True
    try:
        start = (proc.stdout or "").rfind("{")
        if start >= 0:
            proto = json.loads(proc.stdout[start:])
            result.metrics = proto.get("checks", proto)
            if "passed" in proto:
                result.passed = bool(proto["passed"])
            result.protocol_path = proto.get("protocol_path")
    except (ValueError, json.JSONDecodeError):
        pass
    if proc.returncode != 0:
        result.passed = False
        result.log += "\nSTDERR:" + (proc.stderr or "")[-2000:]
    return result


def list_research_protocols() -> list[str]:
    """Список протоколов research/TRX-*/."""
    root = find_trivortex()
    if root is None:
        return []
    research = os.path.join(root, "research")
    out = []
    try:
        for name in sorted(os.listdir(research)):
            if name.startswith("TRX-") and os.path.isdir(os.path.join(research, name)):
                out.append(name)
    except OSError:
        pass
    return out


def load_research_protocol(trx_id: str) -> dict | None:
    """Чтение протокола: README.md первых строк + список файлов."""
    root = find_trivortex()
    if root is None:
        return None
    path = os.path.join(root, "research", trx_id)
    if not os.path.isdir(path):
        return None
    info = {"id": trx_id, "path": path, "files": []}
    for base, _dirs, files in os.walk(path):
        for f in files:
            info["files"].append(os.path.relpath(os.path.join(base, f), path))
    info["files"] = sorted(info["files"])[:100]
    readme = os.path.join(path, "README.md")
    if os.path.isfile(readme):
        try:
            with open(readme, encoding="utf-8") as fh:
                info["readme_head"] = fh.read(2000)
        except OSError:
            pass
    return info


def theorem31_series(
    n_points: int = 200, C_Ch: float = 1.0, T: float = 2 * 3.141592653589793
) -> list[dict]:
    """
    Замкнутая форма Теоремы 3.1 — собственная реализация моста
    (используется планировщиком AnalyticPlanner без импорта ядра):

        r_k(t)   = √C_Ch · (1 + ε·cos(ωt + 2πk/3))
        θ_k(t)   = ωt + 2πk/3
        ω        = (2π/T)·e^(C_Ch/π),  ε = 1/(e^(C_Ch/π) − 1)
    """
    import math

    ratio = math.exp(C_Ch / math.pi)
    omega = (2 * math.pi / T) * ratio
    # guard ядра: при C_Ch <= 0.01 амплитуда фиксируется на 1
    eps = 1.0 / (ratio - 1.0) if C_Ch > 0.01 else 1.0
    series = []
    for i in range(n_points):
        t = T * i / max(n_points - 1, 1)
        frame = []
        for k in range(3):
            phase = omega * t + 2 * math.pi * k / 3
            r = math.sqrt(C_Ch) * (1 + eps * math.cos(phase))
            theta = omega * t + 2 * math.pi * k / 3
            frame.append((r * math.cos(theta), r * math.sin(theta)))
        series.append({"t": t, "positions": frame})
    series[-1]["omega"] = omega
    series[-1]["epsilon"] = eps
    return series
