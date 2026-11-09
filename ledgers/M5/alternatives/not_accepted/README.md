# M5 alternatives not accepted

These two files were the round-1 alternatives 1 and 2. They fail the project grader on seeds 0-49
(`ledgers/M5/scripts/M5-d-r2/d2_alternatives_seeds0-49_counts.out`: 0 of 50 each), because they contradict
`course/modules/M/M5/project.html` as written:

- `alt1_gauss_seidel_in_place.py` updates states in place. The page states that each sweep is synchronous
  (Conventions, "Iteration"), and the suite checks the first sweep from zero against the synchronous operator.
- `alt2_residual_stop.py` stops on the residual and reports `residual / (1 - beta)`. The page states that the
  certified error is `beta / (1 - beta)` times the last change, and that the solver stops at the first sweep whose
  certified error is at most `tol`.

They are kept for the record. Their replacements are `alt1_functional_reduce_and_tuples.py` and
`alt2_class_with_precomputed_feasible_tables.py`, which obey the page. The decision is recorded in
`plans/M5-open-items.md` (round-2 fixer, slice d).
