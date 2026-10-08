# TRIVORTEX — формализация в Lean 4 + Mathlib (веха M1)

> Русскоязычный обзор. Полный документ — в [README.md](README.md).

**Статус: реализовано — v1.1.** Артефакт `Trivortex.lean` — те же три
объекта над `ℝ` средствами Mathlib: замкнутая форма Теоремы 3.1,
интеграл Чаплыгина, вихревые интегралы.

## Что доказано

- `theta_separation` — хореография: разделение ровно `2π/3`;
- `r_periodic`, `theta_periodic` — периодичность с `T_r = 2π/ω`
  (через `Real.cos_period`);
- `chaplygin_shape` — алгебраическая форма `C_Ch = r²θ̇ − q·r`;
- `side1..side3`, `H_equilateral`, `P_equilateral`, `Q_equilateral`,
  `I_equilateral` — точные якоря равностороннего состояния;
- `omega_ne_zero`, `omega_pos` — физический режим `C_Ch > 0, T > 0`.

В конце файла — `#print axioms` для всех теорем: след только на
классические основания Mathlib (propext, Classical.choice, Quot.sound).

## Проект

- `lean-toolchain` — пин `leanprover/lean4:v4.4.0`;
- `lakefile.lean` — пакет с зависимостью от Mathlib (образ Docker
  резолвит и кэширует Mathlib при сборке; для полной воспроизводимости
  закрепите ревизию коммитом — см. README.md).

## Сборка

```bash
docker build -t trivortex-lean verification/docker/lean4
docker run --rm trivortex-lean lake build
```

CI: `verification-ports.yml`, задание *formal-lean4* (non-blocking).
