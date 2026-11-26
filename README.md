# GRH Lean check: compact edition (private)

Independent build and check of **lsernau/grh-lean**, folder `grh-compact`, commit `72fead102f663d5c7a407964a13dc0cf9d977207` (25 Nov 2026), on our own hardware (UWaterloo cpu160, local disk). Lean v4.35.0, Mathlib `56a00585` as pinned by the project. This page reports only our own runs.

Last updated: 2026-11-26 00:11 UTC

## Plan
1. `lake exe cache get` (Mathlib oleans from the Mathlib cache)
2. `lake build` of all project modules
3. `#print axioms` for the five theorems (project script and our own file), and `#check` of their types against `Statements.lean`
4. Kernel replay of every project module with `leanchecker`
5. (later) export and independent checker

## Current state
```
modules_total=794 built=748 replay_ok=0 replay_bad=0
--- stages
2026-11-25T23:49:38Z start host=cpu160 commit=72fead102f663d5c7a407964a13dc0cf9d977207 lean=Lean (version 4.35.0
2026-11-25T23:49:38Z cache_get begin
2026-11-25T23:50:15Z cache_get ok
2026-11-25T23:50:15Z build begin modules=794
--- load 428.00 438.05 411.54
--- axioms
--- our_axioms
--- buildtime
```

## Statements
`src/Statements.lean` (imports only Mathlib) is identical, apart from blank lines, to the one in the original Alpöge–Claude development we checked on 20–21 Nov 2026.
