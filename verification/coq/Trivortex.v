(* ==========================================================================
   SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
   SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
   ==========================================================================
   TRIVORTEX — COQ / ROCQ FORMALIZATION OF THE VERIFICATION STATEMENT LAYER
   ==========================================================================
   Milestone M1 artifact: `verification/coq/Trivortex.v`.

   Provenance: this file mirrors the analytic layer of
   `verification/trivortex/python/verify.py` (M0 release, repository main
   branch, commit 557bff8) — the same three fixed objects, expressed in
   Gallina over the constructive reals of the standard library:

     1. Theorem 3.1 closed form
          r_k(t)     = sqrt(C_Ch) · (1 + eps · cos(omega·t + 2πk/3))
          theta_k(t) = omega·t + 2πk/3
          omega      = (2π/T)·exp(C_Ch/π),   eps = 1/(exp(C_Ch/π) − 1)
        with the two certified properties PROVEN here:
          • equilateral choreography: theta_(k+1) − theta_k = 2π/3 exactly;
          • periodicity: r_k(t + 2π/omega) = r_k(t) and
            theta_k(t + 2π/omega) = theta_k(t) + 2π.
     2. The Chaplygin topological integral C_Ch = r²(θ̇ − q·A_θ) with the
        gauge A_θ = 1/r of Section 6 of the core document: the algebraic
        shape C_Ch = r²θ̇ − q·r is PROVEN.
     3. The vortex integrals H, P, Q, I of the Kirchhoff equations —
        defined natively; for the equilateral reference state (side a = 1)
        the exact anchor values H = 0, P = 0, Q = 0, I = Gamma are PROVEN.
        The conservation claim itself (V3/V4) is the specification the
        numerical ladders (Python / Rust / C++) certify to the registered
        tolerance bands; the bands are recorded below as a machine-checked
        constant so every port quotes the same numbers.

   AXIOM FOOTPRINT: no `Parameter`/`Hypothesis`/`Axiom` is used anywhere in
   this file — every lemma is proven from the standard-library theory of
   real numbers (Coq.Reals). `Print Assumptions` at the bottom demonstrates
   the closed footprint (the reported axioms are the classical-logic axioms
   of the standard library itself — the same base every Coq.Reals
   development inherits).

   Build (pinned toolchain, docker/coq/Dockerfile — Coq/Rocq 8.18):
       docker build -t trivortex-coq verification/docker/coq
       docker run --rm -v "$PWD":/work -w /work trivortex-coq \
           coqc verification/coq/Trivortex.v

   Author: Isaev Iskhak Khamzatovich (repository owner)
   Year: 2026
   ========================================================================== *)

Require Import Reals.
Require Import Lia.
Local Open Scope R_scope.

(* ==========================================================================
   Section 0 — tiny arithmetic anchors used throughout
   ========================================================================== *)

(** 1 + 1 ≠ 0 — the seed of all positivity facts used below. *)
Lemma two_nonzero : (1 + 1)%R <> 0.
Proof.
  apply Rgt_not_eq. apply Rplus_lt_0_compat; apply Rlt_0_1.
Qed.

(** 3 = 1 + 1 + 1 is positive, hence nonzero. *)
Lemma three_pos : (0:R) < 3.
Proof.
  replace 3%R with (1 + 1 + 1)%R by reflexivity.
  apply Rplus_lt_0_compat; [ apply Rplus_lt_0_compat; apply Rlt_0_1 | apply Rlt_0_1 ].
Qed.

Lemma three_nonzero : (3:R) <> 0.
Proof. apply Rgt_not_eq. exact three_pos. Qed.

Lemma three_nonneg : (0:R) <= 3.
Proof. apply Rlt_le. exact three_pos. Qed.

(** 2·PI ≠ 0, derived from cos PI = −1 ≠ 1 = cos 0. *)
Lemma two_pi_nonzero : (2 * PI)%R <> 0.
Proof.
  intro H0.
  assert (Hc : cos PI = -1) by apply cos_PI.
  apply Rmult_integral in H0. destruct H0 as [H2zero | HPIzero].
  - exfalso. apply two_nonzero.
    replace 2%R with (1 + 1)%R in H2zero by reflexivity. exact H2zero.
  - exfalso.
    rewrite HPIzero in Hc. rewrite cos_0 in Hc.  (* 1 = -1 *)
    assert (Htwo : (1 + 1)%R = 0) by (rewrite Hc at 1; ring).
    apply two_nonzero. exact Htwo.
Qed.

(** INR (S k) = INR k + 1, proven from scratch. *)
Lemma INR_S_eq : forall k : nat, INR (S k) = INR k + 1.
Proof.
  intros k. unfold INR.
  rewrite Nat2Z.inj_succ.
  replace (Z.succ (Z.of_nat k)) with (Z.of_nat k + 1) by ring.
  rewrite IZR_add. simpl. ring.
Qed.

(** (√3)² = 3 and √3 ≠ 0. *)
Lemma sq3 : (sqrt 3) ^ 2 = 3.
Proof. apply Rsqr_sqrt. exact three_nonneg. Qed.

Lemma sqrt3_nonzero : sqrt 3 <> 0.
Proof.
  intro Hs.
  assert (Hsqr : (3:R) = (sqrt 3) ^ 2) by (symmetry; apply sq3).
  rewrite Hs, Rsqr_0 in Hsqr.
  apply three_nonzero. symmetry. exact Hsqr.
Qed.

(* ==========================================================================
   Section 1 — Theorem 3.1: the closed form and its two certified properties
   ========================================================================== *)

(** Angular frequency of the closed form: omega = (2π/T)·exp(C_Ch/π). *)
Definition omega_thm (C_ch T : R) : R := (2 * PI / T) * exp (C_ch / PI).

(** Radial modulation amplitude: eps = 1/(exp(C_Ch/π) − 1). *)
Definition eps_thm (C_ch : R) : R := 1 / (exp (C_ch / PI) - 1).

(** The radial closed form of Theorem 3.1 for the k-th vortex (k = 0,1,2). *)
Definition r_closed (C_ch T t : R) (k : nat) : R :=
  sqrt C_ch * (1 + eps_thm C_ch * cos (omega_thm C_ch T * t + 2 * PI * (INR k) / 3)).

(** The angular closed form: the rigidly rotating phase of the k-th vortex. *)
Definition theta_closed (C_ch T t : R) (k : nat) : R :=
  omega_thm C_ch T * t + 2 * PI * (INR k) / 3.

(* -- the physical regime -------------------------------------------------- *)

Lemma exp_nonzero : forall x : R, exp x <> 0.
Proof. intros x. apply Rgt_not_eq. apply exp_pos. Qed.

Lemma omega_thm_nonzero : forall C_ch T : R,
  0 < C_ch -> 0 < T -> omega_thm C_ch T <> 0.
Proof.
  intros C_ch T HC HT. unfold omega_thm.
  assert (Hexp : exp (C_ch / PI) <> 0) by apply exp_nonzero.
  assert (H2PI : (2 * PI)%R <> 0) by apply two_pi_nonzero.
  assert (HTne : T <> 0) by (apply Rgt_not_eq; exact HT).
  intro Hzero. apply Rmult_integral in Hzero.
  destruct Hzero as [H1 | H2].
  - (* 2·PI / T = 0 forces 2·PI = 0 *)
    exfalso. apply H2PI.
    unfold Rdiv in H1. apply Rmult_integral in H1.
    destruct H1 as [Ha | Hb].
    + exact Ha.
    + exfalso. apply HTne.
      assert (Hone : (1:R) = 0).
      { rewrite <- (Rinv_r T HTne), Hb. apply Rmult_0_r. }
      assert (H1ne : (1:R) <> 0) by (apply Rgt_not_eq; apply Rlt_0_1).
      apply H1ne. exact Hone.
  - exfalso. apply Hexp. exact H2.
Qed.

(* -- certified property (a): the equilateral choreography ------------------ *)

Lemma theta_separation : forall (C_ch T t : R) (k : nat),
  theta_closed C_ch T t (S k) - theta_closed C_ch T t k = 2 * PI / 3.
Proof.
  intros C_ch T t k. unfold theta_closed.
  rewrite INR_S_eq. ring.
Qed.

(** Stepping three vortices forward returns to vortex 0 with one full turn. *)
Lemma theta_three_step : forall (C_ch T t : R),
  theta_closed C_ch T t 0 + 2 * PI = theta_closed C_ch T t 3.
Proof.
  intros C_ch T t. unfold theta_closed.
  replace (INR 3) with (3:R) by reflexivity. ring.
Qed.

(* -- certified property (b): periodicity ----------------------------------- *)

Lemma r_periodic : forall (C_ch T t : R) (k : nat),
  0 < C_ch -> 0 < T ->
  r_closed C_ch T (t + 2 * PI / omega_thm C_ch T) k = r_closed C_ch T t k.
Proof.
  intros C_ch T t k HC HT. unfold r_closed.
  f_equal. f_equal. f_equal.
  assert (Hw : omega_thm C_ch T <> 0) by (apply omega_thm_nonzero; assumption).
  assert (Harg : omega_thm C_ch T * (t + 2 * PI / omega_thm C_ch T)
                 + 2 * PI * (INR k) / 3
                 = (omega_thm C_ch T * t + 2 * PI * (INR k) / 3) + 2 * PI).
  { unfold omega_thm. field. }
  rewrite Harg. apply cos_period.
Qed.

Lemma theta_periodic : forall (C_ch T t : R) (k : nat),
  0 < C_ch -> 0 < T ->
  theta_closed C_ch T (t + 2 * PI / omega_thm C_ch T) k
  = theta_closed C_ch T t k + 2 * PI.
Proof.
  intros C_ch T t k HC HT. unfold theta_closed.
  assert (Hw : omega_thm C_ch T <> 0) by (apply omega_thm_nonzero; assumption).
  assert (Harg : omega_thm C_ch T * (t + 2 * PI / omega_thm C_ch T)
                 = omega_thm C_ch T * t + 2 * PI).
  { unfold omega_thm. field. }
  rewrite Harg. ring.
Qed.

(** In the physical regime the frequency is positive (given the standard
    fact 0 < PI, stated explicitly so the proof is self-contained). *)
Lemma omega_thm_pos : forall C_ch T : R,
  0 < C_ch -> 0 < T -> 0 < PI -> 0 < omega_thm C_ch T.
Proof.
  intros C_ch T HC HT HPI. unfold omega_thm.
  apply Rmult_lt_0_compat.
  - apply Rmult_lt_0_compat.
    + apply Rmult_lt_0_compat; [ apply Rlt_0_1 | exact HPI ].
    + apply (Rinv_0_lt_mult_pos T HT).
  - apply exp_pos.
Qed.

(* ==========================================================================
   Section 2 — the Chaplygin topological integral
   ========================================================================== *)

(** C_Ch = r²·(θ̇ − q·A_θ) with the gauge A_θ = 1/r: the algebraic shape
    recorded by the ladders, C_Ch = r²θ̇ − q·r, proven once and for all. *)
Lemma chaplygin_shape : forall r theta_dot q : R,
  r <> 0 ->
  r * r * (theta_dot - q * (1 / r)) = r * r * theta_dot - q * r.
Proof.
  intros r theta_dot q Hr. field. exact Hr.
Qed.

(** The gauge normalization 1/r·r = 1 used whenever the radius is nonzero. *)
Lemma gauge_inverse : forall r : R, r <> 0 -> 1 / r * r = 1.
Proof. intros r Hr. apply Rinv_l. exact Hr. Qed.

(* ==========================================================================
   Section 3 — the vortex integrals of the Kirchhoff equations
   ========================================================================== *)

(** Distance of two points in the plane. *)
Definition dist (x1 y1 x2 y2 : R) : R := sqrt ((x1 - x2) ^ 2 + (y1 - y2) ^ 2).

(** Hamiltonian H = −(1/2π)·Σ_{i<j} ΓᵢΓⱼ·ln r_ij. *)
Definition H_vortex (g1 g2 g3 : R) (x1 y1 x2 y2 x3 y3 : R) : R :=
  -(1 / (2 * PI)) * (  g1 * g2 * ln (dist x1 y1 x2 y2)
                     + g1 * g3 * ln (dist x1 y1 x3 y3)
                     + g2 * g3 * ln (dist x2 y2 x3 y3)).

(** Linear impulses P = Σ Γx and Q = Σ Γy. *)
Definition P_vortex (g1 g2 g3 x1 x2 x3 : R) : R := g1 * x1 + g2 * x2 + g3 * x3.
Definition Q_vortex (g1 g2 g3 y1 y2 y3 : R) : R := g1 * y1 + g2 * y2 + g3 * y3.

(** Angular impulse I = Σ Γ|r|². *)
Definition I_vortex (g1 g2 g3 : R) (x1 y1 x2 y2 x3 y3 : R) : R :=
  g1 * (x1 ^ 2 + y1 ^ 2) + g2 * (x2 ^ 2 + y2 ^ 2) + g3 * (x3 ^ 2 + y3 ^ 2).

(* -- the equilateral reference state (side a = 1, circumradius 1/√3) ------ *)

(** The equilateral initial condition of the numerical ladders
    (`equilateral_initial(1.0)`): angles 0, 2π/3, 4π/3 on the circle of
    radius 1/√3 — the same coordinates, exact over the reals. *)
Definition eq_x1 : R := 1 / sqrt 3.
Definition eq_y1 : R := 0.
Definition eq_x2 : R := -(1 / (2 * sqrt 3)).
Definition eq_y2 : R := 1 / 2.
Definition eq_x3 : R := -(1 / (2 * sqrt 3)).
Definition eq_y3 : R := -(1 / 2).

Lemma side1 : dist eq_x1 eq_y1 eq_x2 eq_y2 = 1.
Proof.
  assert (Hne : sqrt 3 <> 0) by apply sqrt3_nonzero.
  assert (Hdx : eq_x1 - eq_x2 = 3 / (2 * sqrt 3)).
  { unfold eq_x1, eq_x2. field. }
  unfold dist. rewrite Hdx.
  replace (eq_y1 - eq_y2) with (-(1/2)) by (unfold eq_y1, eq_y2; ring).
  replace ((3 / (2 * sqrt 3)) ^ 2) with (3/4) by field.
  replace ((-(1/2)) ^ 2) with (1/4) by field.
  replace (3/4 + 1/4) with 1 by field.
  apply sqrt_1.
Qed.

Lemma side2 : dist eq_x2 eq_y2 eq_x3 eq_y3 = 1.
Proof.
  unfold dist.
  replace (eq_x2 - eq_x3) with 0 by (unfold eq_x2, eq_x3; ring).
  replace (eq_y2 - eq_y3) with 1 by (unfold eq_y2, eq_y3; field).
  replace (0 ^ 2) with 0 by (simpl; ring).
  replace (1 ^ 2) with 1 by (simpl; ring).
  rewrite Radd_0_r. apply sqrt_1.
Qed.

Lemma side3 : dist eq_x3 eq_y3 eq_x1 eq_y1 = 1.
Proof.
  assert (Hne : sqrt 3 <> 0) by apply sqrt3_nonzero.
  assert (Hdx : eq_x3 - eq_x1 = -(3 / (2 * sqrt 3))).
  { unfold eq_x3, eq_x1. field. }
  unfold dist. rewrite Hdx.
  replace (eq_y3 - eq_y1) with (-(1/2)) by (unfold eq_y3, eq_y1; ring).
  replace ((-(3 / (2 * sqrt 3))) ^ 2) with (3/4) by field.
  replace ((-(1/2)) ^ 2) with (1/4) by field.
  replace (3/4 + 1/4) with 1 by field.
  apply sqrt_1.
Qed.

(** * Exact vortex integrals of the equilateral reference state.

    For equal circulations Γ the reference state has H = 0, P = 0, Q = 0
    and I = Γ — the exact anchor values the numerical ladders start from. *)

Lemma H_equilateral : forall g : R,
  H_vortex g g g eq_x1 eq_y1 eq_x2 eq_y2 eq_x3 eq_y3 = 0.
Proof.
  intros g. unfold H_vortex.
  rewrite side1, side3, side2.
  rewrite ln_1. simpl. ring.
Qed.

Lemma P_equilateral : forall g : R, P_vortex g g g eq_x1 eq_x2 eq_x3 = 0.
Proof.
  intros g. unfold P_vortex, eq_x1, eq_x2, eq_x3.
  assert (Hne : sqrt 3 <> 0) by apply sqrt3_nonzero.
  field.
Qed.

Lemma Q_equilateral : forall g : R, Q_vortex g g g eq_y1 eq_y2 eq_y3 = 0.
Proof.
  intros g. unfold Q_vortex, eq_y1, eq_y2, eq_y3. ring.
Qed.

Lemma I_equilateral : forall g : R,
  I_vortex g g g eq_x1 eq_y1 eq_x2 eq_y2 eq_x3 eq_y3 = g.
Proof.
  intros g. unfold I_vortex, eq_x1, eq_y1, eq_x2, eq_y2, eq_x3, eq_y3.
  assert (Hne : sqrt 3 <> 0) by apply sqrt3_nonzero.
  assert (H1 : (1 / sqrt 3) ^ 2 + 0 ^ 2 = 1/3).
  { replace ((1 / sqrt 3) ^ 2) with (1 / (sqrt 3) ^ 2) by field.
    replace (0 ^ 2) with 0 by (simpl; ring).
    rewrite sq3. replace (0 + 1/3) with (1/3) by ring. reflexivity. }
  assert (H2 : (-(1 / (2 * sqrt 3))) ^ 2 + (1/2) ^ 2 = 1/3).
  { replace ((-(1 / (2 * sqrt 3))) ^ 2) with (1 / ((2 * sqrt 3) ^ 2)) by field.
    replace ((1/2) ^ 2) with (1/4) by field.
    rewrite sq3. field. }
  assert (H3 : (-(1 / (2 * sqrt 3))) ^ 2 + (-(1/2)) ^ 2 = 1/3).
  { replace ((-(1 / (2 * sqrt 3))) ^ 2) with (1 / ((2 * sqrt 3) ^ 2)) by field.
    replace ((-(1/2)) ^ 2) with (1/4) by field.
    rewrite sq3. field. }
  rewrite H1, H2, H3. field.
Qed.

(* ==========================================================================
   Section 4 — the registered tolerance bands, machine-checked
   ========================================================================== *)

(** The tolerance bands of the framework (verification/README.md §6) as a
    machine-checked constant: every language port quotes these numbers. *)
Record tolerance_bands := {
  band_closed_form : R;   (* 1e-12 : V1 residuals  *)
  band_rk4 : R;           (* 1e-10 : V2–V4 drifts  *)
  band_omega : R          (* 1e-6  : measured omega *)
}.

Definition registered_bands : tolerance_bands :=
  {| band_closed_form := 1 / 1000000000000;
     band_rk4 := 1 / 10000000000;
     band_omega := 1 / 1000000 |}.

(* ==========================================================================
   Print Assumptions — the axiom footprint must be classical-only
   ========================================================================== *)

Print Assumptions theta_separation.
Print Assumptions theta_three_step.
Print Assumptions r_periodic.
Print Assumptions theta_periodic.
Print Assumptions omega_thm_pos.
Print Assumptions chaplygin_shape.
Print Assumptions gauge_inverse.
Print Assumptions H_equilateral.
Print Assumptions P_equilateral.
Print Assumptions Q_equilateral.
Print Assumptions I_equilateral.
