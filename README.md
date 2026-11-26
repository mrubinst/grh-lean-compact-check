# GRH Lean check: compact edition (private)

Independent build and check of **lsernau/grh-lean**, folder `grh-compact`, commit `72fead102f663d5c7a407964a13dc0cf9d977207` (25 Nov 2026), on our own hardware (UWaterloo cpu160, local disk). Lean v4.35.0, Mathlib `56a00585` as pinned by the project. This page reports only our own runs.

Last updated: 2026-11-26 00:29 UTC

## Plan
1. `lake exe cache get` (Mathlib oleans from the Mathlib cache)
2. `lake build` of all project modules
3. `#print axioms` for the five theorems (project script and our own file), and `#check` of their types against `Statements.lean`
4. Kernel replay of every project module with `leanchecker`
5. (later) export and independent checker

## Current state
```
modules_total=794 built=794 replay_ok=794 replay_bad=0
--- stages
2026-11-25T23:49:38Z start host=cpu160 commit=72fead102f663d5c7a407964a13dc0cf9d977207 lean=Lean (version 4.35.0
2026-11-25T23:49:38Z cache_get begin
2026-11-25T23:50:15Z cache_get ok
2026-11-25T23:50:15Z build begin modules=794
2026-11-26T00:18:13Z build ok
2026-11-26T00:18:13Z axioms begin
2026-11-26T00:18:27Z axioms ok
2026-11-26T00:18:40Z our_axioms ok
2026-11-26T00:18:40Z replay begin
2026-11-26T00:28:15Z replay done ok=794 bad=0
2026-11-26T00:28:15Z pipeline finished
--- load 431.19 451.90 438.78
--- axioms
'riemannHypothesis' depends on axioms: [propext, Classical.choice, Quot.sound]
'riemannZeta_eq_zero_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'LFunction_ne_zero_of_half_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'LFunction_eq_zero_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'LFunction_eq_zero_re_of_isPrimitive' depends on axioms: [propext, Classical.choice, Quot.sound]
--- our_axioms
'riemannHypothesis' depends on axioms: [propext, Classical.choice, Quot.sound]
'riemannZeta_eq_zero_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'LFunction_ne_zero_of_half_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'LFunction_eq_zero_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'LFunction_eq_zero_re_of_isPrimitive' depends on axioms: [propext, Classical.choice, Quot.sound]
riemannHypothesis : RiemannHypothesis
riemannZeta_eq_zero_re : RiemannZetaZerosOnLine
LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf
LFunction_eq_zero_re : DirichletLZerosOnLine
LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine
def RiemannHypothesis : Prop :=
∀ (s : ℂ), riemannZeta s = 0 → (¬∃ n, s = -2 * (↑n + 1)) → s ≠ 1 → s.re = 1 / 2
--- buildtime
	Elapsed (wall clock) time (h:mm:ss or m:ss): 27:58.23
	Maximum resident set size (kbytes): 9140112
```

## Statements
`src/Statements.lean` (imports only Mathlib) is identical, apart from blank lines, to the one in the original Alpöge–Claude development we checked on 20–21 Nov 2026.
