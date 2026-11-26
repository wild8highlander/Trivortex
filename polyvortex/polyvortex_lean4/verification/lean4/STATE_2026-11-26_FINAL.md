# Polyvortex TW1.b — ФИНАЛЬНОЕ СОСТОЯНИЕ (2026-11-26)

## Результат
`verification/lean4/Polyvortex.lean` — **компилируется с 0 ошибок, 0 sorry**.
`lake env lean Polyvortex.lean` → EXIT=0. Лог: `download/polyvortex/compile55.log`.
#print axioms в конце файла: только [propext, Classical.choice, Quot.sound] —
sorryAx отсутствует для ВСЕХ перечисленных теорем.

## Закрытые разделы (все)
- §1 Theorem A (ring_velocity, ringOrbit_sol, lag_omega_unique, ringOmega_three_eq_lagrange)
- §2 Theorem B (eps_lt_one_iff, rClosed_*, ring_radial_zero)
- §3 Lemma C (lemmaC_pulsation, lemmaC_radius_constant, lemmaC_H1_reduction)
- §4 Lemma D (lemmaD_omega_independent, lemmaD_bridge, poisson_integral, poisson_sq)
- §5 Theorem E statement layer (ring_fixed_point, ring_corotating_constant и др.)

## Ключевые правки последней сессии (compile50→55)
1. htrans-хвост poisson_half: `rw [integral_symm]` + `simp only [smul_eq_mul, inv_neg_one, neg_one_mul, neg_neg]`.
2. Добавлен локальный `sq_neg (a : ℝ) : (-a)^2 = a^2 := by ring` (в Mathlib его нет).
3. add-the-two-halves: bridge-show `1/(1-ε·cos) = 1/(1+(-ε)·cos)` (simp only с ∀-правилом) + ascribed `poisson_cont (by rwa [sq_neg] : (-ε)^2 < 1)`.
4. hcombo: второй сумманд в форме `1+(-ε)·cos`; явный `(f := fun x => poissonG ε x + poissonG (-ε) x)` (higher-order unification не решает ?F);
   `Set.mem_uIcc` даёт дизъюнкцию → паттерн poisson_ftc: `have hxIoo` через constructor+rcases.
5. hz: `show (0:ℝ)/2 = 0` перед tan_zero; h1: один mul_comm; h2: `← Real.sqrt_mul`; hk2 через `eq_inv_of_mul_eq_one_left`.
6. hpair: `Real.arctan_inv_of_pos` (вместо несуществующего `arctan_add_arctan_inv`), второй `mul_one` после hk2, `← mul_add`, congr+ring.
7. poisson_integral: show-bridge интеганда + хвост field_simp.
8. poisson_sq: hg2pi/hg0 haves, `ne_of_gt (Real.sqrt_pos.mpr hc)`, field_simp [hc.ne', hsq0].
9. ring_corotating_constant: hu с goal-формой u, `rw [← Complex.ofReal_mul]` (цель право-вложенная I*(↑ω*↑t)), simp only [kirchhoff_smul γ hu k, ring_velocity ...], ring.

## Окружение
- Toolchain leanprover/lean4:v4.6.0, Mathlib master (v4.6.0-совместимый), lake build ОК.
- Восстановление среды: scripts/setup_lean.sh; ELAN_HOME=/tmp/elan.
- Рабочая копия: /home/z/my-project/work/polyvortex/verification/lean4/ ( lake env lean Polyvortex.lean ).

## Осталось (вне TW1.b)
- lake build + гейты + супер-зип (см. todo) — файл уже чист, это только упаковка.
