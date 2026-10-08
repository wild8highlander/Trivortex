# TRIVORTEX — формализация в Isabelle/HOL (веха M2)

> Русскоязычный обзор. Полный документ — в [README.md](README.md).

**Статус: реализовано — v1.1.** Артефакт `Trivortex.thy` — слой
формулировок над `Complex_Main`, в стиле M2: перекрёстная проверка
формулировок, доказанных в Coq и Lean, плюс численные границы.

## Что доказано

- `theta_separation`, `theta_three_step` — хореография;
- `r_periodic`, `theta_periodic` — периодичность (через `cos_periodic`);
- `chaplygin_shape`, `gauge_inverse` — форма интеграла Чаплыгина;
- точные якоря: `H_equilateral`, `P_equilateral`, `Q_equilateral`,
  `I_equilateral` и стороны ровно 1 (`rdist_eq1..3`);
- `registered_bands` — запись полос допусков с проверяемым порядком
  (`bands_positive`, `band_ordering`).

## SMT-границы (опционально)

`Trivortex_SMT.thy` содержит SMT-разряженные численные неравенства
(метод `smt`, Z3). По умолчанию сессия отключена в `ROOT`: метод `smt`
перепроигрывает сертификаты при сборке и требует Z3 в образе.
Инструкция включения — в комментариях `ROOT`.

## Сборка

```bash
docker build -t trivortex-isabelle verification/docker/isabelle
docker run --rm trivortex-isabelle isabelle build -D /app/isabelle
```

CI: `verification-ports.yml`, задание *formal-isabelle* (non-blocking).
