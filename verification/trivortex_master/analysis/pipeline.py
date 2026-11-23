#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — конвейер анализа данных (пайплайн).

Декларативный конвейер: шаги с зависимостями, кэширование по хэшу
входов, изоляция сбоев и отчёт о происхождении данных (provenance):

  * PipelineStep: имя, функция, входы (имена других шагов), тег
    версии функции (для инвалидации кэша);
  * Pipeline: ориентированный ациклический граф шагов; топологическая
    сортировка ( Кана 1962 ), прогон с мемоизацией результатов;
  * сбой шага не валит конвейер: зависимые шаги помечаются skipped,
    независимые выполняются;
  * provenance: для каждого результата — дерево происхождения
    (какие шаги и с какими версиями участвовали);
  * validate: проверка контрактов (тип результата, схема dict).

Самопроверка: DAG из 5 шагов выполняется в правильном порядке;
кэш даёт второй прогон без вычислений; сбой изолируется; цикл
обнаруживается.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable


# ═══════════════════════════════════════════════════════════════════════════
# Шаг конвейера
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class PipelineStep:
    """Один шаг: функция от словаря результатов входов."""

    name: str
    func: Callable[[dict[str, Any]], Any]
    inputs: tuple[str, ...] = ()
    version: str = "1"  # изменение версии инвалидирует кэш
    validator: Callable[[Any], list[str]] | None = None

    def signature(self) -> str:
        """Хэш имени+версии+входов — ключ кэша."""
        payload = json.dumps(
            dict(name=self.name, v=self.version, inputs=list(self.inputs)), sort_keys=True
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class StepResult:
    """Результат шага: значение или ошибка + происхождение."""

    step: str
    ok: bool
    value: Any = None
    error: str = ""
    duration_s: float = 0.0
    from_cache: bool = False
    provenance: list[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════
# Конвейер
# ═══════════════════════════════════════════════════════════════════════════
class Pipeline:
    """DAG шагов с кэшированием и изоляцией сбоев."""

    def __init__(self, name: str = "pipeline"):
        self.name = name
        self.steps: dict[str, PipelineStep] = {}
        self.results: dict[str, StepResult] = {}
        self._cache: dict[str, Any] = {}

    def add(self, step: PipelineStep) -> Pipeline:
        if step.name in self.steps:
            raise ValueError(f"шаг уже есть: {step.name}")
        self.steps[step.name] = step
        return self

    # ── топология ──
    def topo_order(self) -> list[str]:
        """Сортировка Кана (1962): обнаруживает циклы."""
        indeg = {name: 0 for name in self.steps}
        dependents: dict[str, list[str]] = {name: [] for name in self.steps}
        for name, step in self.steps.items():
            for inp in step.inputs:
                if inp not in self.steps:
                    raise ValueError(f"{name}: вход {inp} не объявлен")
                indeg[name] += 1
                dependents[inp].append(name)
        queue = sorted(n for n, d in indeg.items() if d == 0)
        order = []
        while queue:
            n = queue.pop(0)
            order.append(n)
            for m in dependents[n]:
                indeg[m] -= 1
                if indeg[m] == 0:
                    queue.append(m)
            queue.sort()
        if len(order) != len(self.steps):
            cyclic = sorted(n for n, d in indeg.items() if d > 0)
            raise ValueError(f"цикл в графе шагов: {cyclic}")
        return order

    # ── прогон ──
    def run(self, use_cache: bool = True) -> dict[str, StepResult]:
        """Выполнить все шаги в топологическом порядке."""
        self.results = {}
        for name in self.topo_order():
            step = self.steps[name]
            # входы: значения успешных шагов
            inputs_ok = all(
                self.results.get(i) is not None and self.results[i].ok for i in step.inputs
            )
            if not inputs_ok:
                failed = [
                    i for i in step.inputs if self.results.get(i) is None or not self.results[i].ok
                ]
                self.results[name] = StepResult(
                    step=name, ok=False, error=f"пропущен: входы недоступны ({failed})"
                )
                continue
            key = step.signature()
            if use_cache and key in self._cache:
                self.results[name] = StepResult(
                    step=name,
                    ok=True,
                    value=self._cache[key],
                    from_cache=True,
                    provenance=self._provenance_of(name),
                )
                continue
            args = {i: self.results[i].value for i in step.inputs}
            t0 = time.perf_counter()
            try:
                value = step.func(args)
                errors = []
                if step.validator is not None:
                    errors = step.validator(value) or []
                if errors:
                    self.results[name] = StepResult(
                        step=name, ok=False, error=f"контракт нарушен: {errors}"
                    )
                    continue
                duration = time.perf_counter() - t0
                self.results[name] = StepResult(
                    step=name,
                    ok=True,
                    value=value,
                    duration_s=duration,
                    provenance=self._provenance_of(name),
                )
                self._cache[key] = value
            except Exception as exc:
                self.results[name] = StepResult(
                    step=name, ok=False, error=f"{type(exc).__name__}: {exc}"
                )

        return self.results

    def _provenance_of(self, name: str) -> list[str]:
        """Цепочка происхождения: версии всех транзитивных входов."""
        step = self.steps[name]
        chain = [f"{name}@{step.version}"]
        for inp in step.inputs:
            res = self.results.get(inp)
            if res is not None:
                chain.extend(res.provenance)
        return sorted(set(chain))

    # ── сводка ──
    def summary(self) -> dict:
        ok_n = sum(1 for r in self.results.values() if r.ok)
        cached_n = sum(1 for r in self.results.values() if r.from_cache)
        return dict(
            name=self.name,
            steps=len(self.results),
            ok=ok_n,
            failed=len(self.results) - ok_n,
            cached=cached_n,
            total_s=sum(r.duration_s for r in self.results.values()),
            failed_steps=[r.step for r in self.results.values() if not r.ok],
        )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """DAG 5 шагов: порядок, кэш-хит, изоляция сбоя, цикл ловится,
    контракт-валидатор работает, provenance транзитивен."""
    # ── построение ──
    calls: list[str] = []
    pipe = Pipeline("test")

    def make_raw(_):
        calls.append("raw")
        return list(range(10))

    def clean(args):
        calls.append("clean")
        return [v * 2 for v in args["raw"]]

    def stats(args):
        calls.append("stats")
        data = args["clean"]
        return dict(mean=sum(data) / len(data), n=len(data))

    def report(args):
        calls.append("report")
        return f"mean={args['stats']['mean']:.1f}"

    pipe.add(PipelineStep("raw", make_raw))
    pipe.add(PipelineStep("clean", clean, inputs=("raw",)))
    pipe.add(PipelineStep("stats", stats, inputs=("clean",)))
    pipe.add(
        PipelineStep(
            "report",
            report,
            inputs=("stats",),
            validator=lambda v: [] if isinstance(v, str) and len(v) > 0 else ["не строка/пусто"],
        )
    )
    # порядок
    order = pipe.topo_order()
    order_ok = (
        order.index("raw") < order.index("clean") < order.index("stats") < order.index("report")
    )
    # первый прогон: все вычислены
    res1 = pipe.run(use_cache=True)
    first_ok = all(r.ok for r in res1.values())
    computed_n = len(calls)
    # второй прогон: всё из кэша
    calls.clear()
    res2 = pipe.run(use_cache=True)
    cache_ok = len(calls) == 0 and all(r.from_cache for r in res2.values())
    # сбой изолируется: чистка падает, отчёт скипается, сырьё живёт
    pipe2 = Pipeline("fail")
    pipe2.add(PipelineStep("raw", make_raw))
    pipe2.add(PipelineStep("bad", lambda a: 1 / 0, inputs=("raw",)))
    pipe2.add(PipelineStep("independent", lambda a: 42))
    res3 = pipe2.run(use_cache=False)
    isolation_ok = (
        res3["raw"].ok
        and not res3["bad"].ok
        and res3["independent"].ok
        and "ZeroDivisionError" in res3["bad"].error
    )
    # цикл ловится
    pipe3 = Pipeline("cycle")
    pipe3.add(PipelineStep("a", lambda x: 1, inputs=("b",)))
    pipe3.add(PipelineStep("b", lambda x: 1, inputs=("a",)))
    try:
        pipe3.topo_order()
        cycle_ok = False
    except ValueError as exc:
        cycle_ok = "цикл" in str(exc)
    # provenance транзитивен
    prov = res1["report"].provenance
    prov_ok = any("raw@" in p for p in prov) and any("stats@" in p for p in prov)
    # валидатор отвергает мусор
    pipe4 = Pipeline("contract")
    pipe4.add(PipelineStep("bad_out", lambda a: "", validator=lambda v: ["пусто"]))
    res4 = pipe4.run(use_cache=False)
    contract_ok = not res4["bad_out"].ok and "контракт" in res4["bad_out"].error
    summ = pipe.summary()
    return dict(
        order_ok=order_ok,
        first_run_ok=first_ok,
        computed_first=computed_n,
        cache_ok=cache_ok,
        isolation_ok=isolation_ok,
        cycle_detected=cycle_ok,
        provenance_ok=prov_ok,
        contract_ok=contract_ok,
        summary=dict(ok=summ["ok"], total=summ["steps"]),
        all_ok=order_ok
        and first_ok
        and cache_ok
        and isolation_ok
        and cycle_ok
        and prov_ok
        and contract_ok,
        note="топология Кана 1962; кэш по sha256(имя,версия,входы); "
        "сбой шага изолируется, зависимые скипаются",
    )
