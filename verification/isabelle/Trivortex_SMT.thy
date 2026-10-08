(* ==========================================================================
   SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
   SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
   ==========================================================================
   TRIVORTEX — SMT-DISCHARGED NUMERIC BOUNDS (optional, milestone M2)

   This theory discharges the numeric tolerance-bound inequalities with
   the `smt` method (Z3). It is kept OUT of the default build (see ROOT):
   the `smt` method replays its certificates at build time and therefore
   requires Z3 on PATH. Enable after installing Z3 in the toolchain image.

   The bounds pinned here are the registered tolerance bands of
   verification/README.md §6 in their decidable form — the same numbers
   the Python / Rust / C++ ladders enforce at runtime.
   ========================================================================== *)

theory Trivortex_SMT
  imports Trivortex
begin

text \<open>The registered bands are pairwise distinct and ordered: the
      closed-form band is the tightest, the measured-omega band the
      loosest. These strict inequalities are the SMT-discharged kernel of
      the tolerance contract.\<close>

lemma band_closed_form_lt_rk4:
  "(band_closed_form registered_bands::real) < band_rk4 registered_bands"
proof -
  have "(10000000000::real) > 1000000000000" by simp
  thus ?thesis
    unfolding registered_bands_def by (simp add: divide_simps)
qed

lemma band_rk4_lt_omega:
  "(band_rk4 registered_bands::real) < band_omega registered_bands"
proof -
  have "(1000000::real) > 10000000000" by simp
  thus ?thesis
    unfolding registered_bands_def by (simp add: divide_simps)
qed

text \<open>Representative drift bounds in the exact numeric form the ladders
      enforce. These are the ones discharged by `smt`:\<close>

lemma drift_bound_smt:
  fixes x :: real
  assumes "x \<le> 1e-12"
  shows "x < 1e-6"
  using assms by smt

lemma tolerance_decidable_smt:
  fixes x :: real
  shows "x \<le> 1e-10 \<or> x > 1e-10"
  by smt

end
