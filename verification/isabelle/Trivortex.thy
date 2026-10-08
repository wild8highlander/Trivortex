(* ==========================================================================
   SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
   SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
   ==========================================================================
   TRIVORTEX — ISABELLE/HOL FORMALIZATION OF THE VERIFICATION STATEMENT LAYER
   ==========================================================================
   Milestone M2 artifact: `verification/isabelle/Trivortex.thy`.

   Provenance: this file mirrors the analytic layer of
   `verification/trivortex/python/verify.py` (M0 release, repository main
   branch, commit 557bff8) — the same three fixed objects, expressed in
   Isabelle/HOL over the reals of Complex_Main:

     1. Theorem 3.1 closed form with PROVEN choreography and periodicity;
     2. the Chaplygin topological integral with its PROVEN algebraic shape;
     3. the vortex integrals H, P, Q, I with the PROVEN exact anchor values
        of the equilateral reference state, plus the registered tolerance
        bands as a machine-checked record.

   The M2 flavor of this port is the *SMT-discharged numeric bounds*
   section: the tolerance bands are pinned as decidable strict
   inequalities. The SMT-discharged variants live in the optional theory
   `Trivortex_SMT.thy` (they replay with Z3; see ROOT for how to enable
   them) so the default build stays green on any Isabelle installation.

   Build (pinned toolchain, docker/isabelle/Dockerfile — Isabelle2024):
       docker build -t trivortex-isabelle verification/docker/isabelle
       docker run --rm -v "$PWD":/work -w /work trivortex-isabelle \
           isabelle build -D verification/isabelle

   Author: Isaev Iskhak Khamzatovich (repository owner)
   Year: 2026
   ========================================================================== *)

theory Trivortex
  imports Complex_Main
begin

section \<open>Theorem 3.1: the closed form and its certified properties\<close>

definition omega_thm :: "real \<Rightarrow> real \<Rightarrow> real"
  where "omega_thm C T = (2 * pi / T) * exp (C / pi)"

definition eps_thm :: "real \<Rightarrow> real"
  where "eps_thm C = 1 / (exp (C / pi) - 1)"

definition r_closed :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real"
  where "r_closed C T t k =
    sqrt C * (1 + eps_thm C * cos (omega_thm C T * t + 2 * pi * real k / 3))"

definition theta_closed :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real"
  where "theta_closed C T t k = omega_thm C T * t + 2 * pi * real k / 3"

subsection \<open>The physical regime\<close>

lemma two_pi_nonzero: "(2 * pi) \<noteq> (0::real)"
  by simp

lemma omega_thm_nonzero:
  assumes "0 < C" "0 < T"
  shows "omega_thm C T \<noteq> 0"
  unfolding omega_thm_def
  using assms by (simp add: field_simps exp_pos)

lemma omega_thm_pos:
  assumes "0 < C" "0 < T"
  shows "0 < omega_thm C T"
  unfolding omega_thm_def
  using assms by (simp add: exp_pos)

subsection \<open>Certified property (a): the equilateral choreography\<close>

text \<open>The angular closed form keeps the exact \<open>2\<pi>/3\<close> separation
      between consecutive vortices — the algebraic core of check V1.\<close>

lemma theta_separation:
  "theta_closed C T t (Suc k) - theta_closed C T t k = 2 * pi / 3"
  unfolding theta_closed_def by simp

lemma theta_three_step:
  "theta_closed C T t 0 + 2 * pi = theta_closed C T t 3"
  unfolding theta_closed_def by simp

subsection \<open>Certified property (b): periodicity of the closed form\<close>

text \<open>\<open>T\<^sub>r = 2\<pi>/\<omega>\<close> is a period of the radial closed form for every
      vortex index — the second pass/fail criterion of check V1.\<close>

lemma r_periodic:
  assumes "0 < C" "0 < T"
  shows "r_closed C T (t + 2 * pi / omega_thm C T) k = r_closed C T t k"
proof -
  have harg: "omega_thm C T * (t + 2 * pi / omega_thm C T)
            = omega_thm C T * t + 2 * pi"
    unfolding omega_thm_def using assms(2) by (simp add: field_simps)
  have hcos: "cos (omega_thm C T * (t + 2 * pi / omega_thm C T)
                       + 2 * pi * real k / 3)
            = cos (omega_thm C T * t + 2 * pi * real k / 3)"
    using harg cos_periodic[of "omega_thm C T * t + 2 * pi * real k / 3"] by simp
  show ?thesis
    unfolding r_closed_def by (simp add: hcos)
qed

lemma theta_periodic:
  assumes "0 < C" "0 < T"
  shows "theta_closed C T (t + 2 * pi / omega_thm C T) k
       = theta_closed C T t k + 2 * pi"
proof -
  have harg: "omega_thm C T * (t + 2 * pi / omega_thm C T)
            = omega_thm C T * t + 2 * pi"
    unfolding omega_thm_def using assms(2) by (simp add: field_simps)
  show ?thesis
    unfolding theta_closed_def using harg by simp
qed

section \<open>The Chaplygin topological integral\<close>

text \<open>With the gauge \<open>A\<^sub>\<theta> = 1/r\<close> of Section 6 of the core document,
      the combination recorded by the ladders is the algebraic shape
      \<open>C\<^sub>C\<^sub>h = r\<^sup>2\<theta>\<dot> \<minus> q\<cdot>r\<close> — proven once and for all.\<close>

lemma chaplygin_shape:
  assumes "r \<noteq> 0"
  shows "r * r * (theta_dot - q * (1 / r)) = r * r * theta_dot - q * r"
  using assms by (simp add: field_simps)

lemma gauge_inverse:
  assumes "r \<noteq> 0"
  shows "1 / r * r = 1"
  using assms by simp

section \<open>The vortex integrals of the Kirchhoff equations\<close>

definition rdist :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real"
  where "rdist x1 y1 x2 y2 = sqrt ((x1 - x2)^2 + (y1 - y2)^2)"

definition H_vortex :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real"
  where "H_vortex g1 g2 g3 x1 y1 x2 y2 x3 y3 =
    - (1 / (2 * pi)) * (g1 * g2 * ln (rdist x1 y1 x2 y2)
                      + g1 * g3 * ln (rdist x1 y1 x3 y3)
                      + g2 * g3 * ln (rdist x2 y2 x3 y3))"

definition P_vortex :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real"
  where "P_vortex g1 g2 g3 x1 x2 x3 = g1 * x1 + g2 * x2 + g3 * x3"

definition Q_vortex :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real"
  where "Q_vortex g1 g2 g3 y1 y2 y3 = g1 * y1 + g2 * y2 + g3 * y3"

definition I_vortex :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real"
  where "I_vortex g1 g2 g3 x1 y1 x2 y2 x3 y3 =
    g1 * (x1^2 + y1^2) + g2 * (x2^2 + y2^2) + g3 * (x3^2 + y3^2)"

subsection \<open>The equilateral reference state (side a = 1, circumradius 1/\<open>\<surd>3\<close>)\<close>

text \<open>The equilateral initial condition of the numerical ladders
      (`equilateral_initial(1.0)`): angles 0, 2\<pi>/3, 4\<pi>/3 on the circle
      of radius 1/\<open>\<surd>3\<close> — the same coordinates, exact over the reals.\<close>

definition eq_x1 :: real where "eq_x1 = 1 / sqrt 3"
definition eq_y1 :: real where "eq_y1 = 0"
definition eq_x2 :: real where "eq_x2 = -(1 / (2 * sqrt 3))"
definition eq_y2 :: real where "eq_y2 = 1 / 2"
definition eq_x3 :: real where "eq_x3 = -(1 / (2 * sqrt 3))"
definition eq_y3 :: real where "eq_y3 = -(1 / 2)"

lemma sqrt3_nonzero: "sqrt 3 \<noteq> (0::real)"
  using real_sqrt_eq_zero_cancel_iff[of 3] by simp

lemma hsq3: "(sqrt 3)^2 = (3::real)"
  by (metis real_sqrt_pow2 zero_le_numeral)

text \<open>The three side lengths of the reference state are exactly 1.\<close>

lemma rdist_eq1: "rdist eq_x1 eq_y1 eq_x2 eq_y2 = 1"
proof -
  have hdx: "((1/sqrt 3) - (-(1/(2*sqrt 3))))^2 = (3::real)/4"
    unfolding power2_eq_square using hsq3 sqrt3_nonzero
    by (simp add: field_simps)
  have hdy: "((0::real) - 1/2)^2 = 1/4"
    unfolding power2_eq_square by simp
  have "rdist eq_x1 eq_y1 eq_x2 eq_y2
      = sqrt ((3::real)/4 + 1/4)"
    unfolding rdist_def eq_x1_def eq_y1_def eq_x2_def eq_y2_def
    using hdx hdy by (simp add: field_simps)
  thus ?thesis by simp
qed

lemma rdist_eq2: "rdist eq_x2 eq_y2 eq_x3 eq_y3 = 1"
  unfolding rdist_def eq_x2_def eq_x3_def eq_y2_def eq_y3_def by simp

lemma rdist_eq3: "rdist eq_x3 eq_y3 eq_x1 eq_y1 = 1"
proof -
  have hdx: "((-(1/(2*sqrt 3))) - (1/sqrt 3))^2 = (3::real)/4"
    unfolding power2_eq_square using hsq3 sqrt3_nonzero
    by (simp add: field_simps)
  have hdy: "((-(1/2)) - (0::real))^2 = 1/4"
    unfolding power2_eq_square by simp
  have "rdist eq_x3 eq_y3 eq_x1 eq_y1
      = sqrt ((3::real)/4 + 1/4)"
    unfolding rdist_def eq_x1_def eq_y1_def eq_x3_def eq_y3_def
    using hdx hdy by (simp add: field_simps)
  thus ?thesis by simp
qed

subsection \<open>The exact anchor values of the vortex integrals\<close>

text \<open>For equal circulations \<open>\<Gamma>\<close> the reference state has exactly
      \<open>H = 0, P = 0, Q = 0, I = \<Gamma>\<close> — the anchor values the numerical
      ladders start from.\<close>

lemma H_equilateral:
  "H_vortex g g g eq_x1 eq_y1 eq_x2 eq_y2 eq_x3 eq_y3 = 0"
  unfolding H_vortex_def
  using rdist_eq1 rdist_eq2 rdist_eq3 by simp

lemma P_equilateral: "P_vortex g g g eq_x1 eq_x2 eq_x3 = 0"
  unfolding P_vortex_def eq_x1_def eq_x2_def eq_x3_def
  using sqrt3_nonzero by (simp add: field_simps)

lemma Q_equilateral: "Q_vortex g g g eq_y1 eq_y2 eq_y3 = 0"
  unfolding Q_vortex_def eq_y1_def eq_y2_def eq_y3_def by simp

lemma I_equilateral: "I_vortex g g g eq_x1 eq_y1 eq_x2 eq_y2 eq_x3 eq_y3 = g"
  unfolding I_vortex_def eq_x1_def eq_y1_def eq_x2_def eq_y2_def eq_x3_def eq_y3_def
  using hsq3 sqrt3_nonzero by (simp add: field_simps)

section \<open>The Lagrange specification and the registered bands\<close>

definition lagrange_omega :: "real \<Rightarrow> real \<Rightarrow> real"
  where "lagrange_omega gamma a = 3 * gamma / (2 * pi * a^2)"

text \<open>The tolerance bands of the framework (verification/README.md §6) as a
      machine-checked record: every language port quotes these numbers.\<close>

record tolerance_bands =
  band_closed_form :: real   \<comment> \<open>1e-12 : V1 residuals\<close>
  band_rk4 :: real           \<comment> \<open>1e-10 : V2\<hash>V4 drifts\<close>
  band_omega :: real         \<comment> \<open>1e-6 : measured omega\<close>

definition registered_bands :: tolerance_bands
  where "registered_bands = \<lparr>
      band_closed_form = 1 / 10^12,
      band_rk4 = 1 / 10^10,
      band_omega = 1 / 10^6 \<rparr>"

text \<open>The bands are strictly positive and mutually ordered — the sanity
      properties that make the registered contract decidable.\<close>

lemma bands_positive:
  "0 < band_closed_form registered_bands"
  "0 < band_rk4 registered_bands"
  "0 < band_omega registered_bands"
  unfolding registered_bands_def by simp_all

lemma band_ordering: "(band_closed_form registered_bands::real) < band_omega registered_bands"
proof -
  have "(1000000000000::real) > 1000000" by simp
  thus ?thesis
    unfolding registered_bands_def by (simp add: divide_simps)
qed

end
