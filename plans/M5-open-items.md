# M5 open items (Builder D: project, grader, project labs)

Scope: `course/modules/M/M5/project.html`, `course/modules/M/M5/grader/`, `tests/labs/M5/lab-M5-project-{1,2,3}.py`,
`ledgers/M5/` (mutants, alternatives, scripts). Other builders' items are in their own sections of this file when they add them.

## Decisions taken where the plan was silent (architect to confirm)

1. **Production function and feasibility (plan §5.2 names only `alpha`).** Output from capital k is `k**alpha`, so saving `k'`
   leaves consumption `k**alpha - k'`, and `k'` is feasible when `k' <= k**alpha`. Utility is `sqrt(c)` (architect Q2).
2. **Extra named invalid inputs (plan §5.3 lists five).** Added, because the feasibility guarantee needs them:
   - `alpha` outside `(0, 1)` (plan §5.2 gives `alpha` in (0, 1) as an input);
   - a grid point that is not positive, and a grid whose first point exceeds 1 (every state can then afford the first
     point, `k_1 <= k^alpha` for all `k` in the grid, so the feasible set is never empty);
   - a boolean or a non-finite number where a real number is meant.
   Each named condition has its own test in both directions (boundary values 0, 1, equal points, first point 1.01).
3. **Certified error.** The contract is "a valid upper bound on the sup-norm distance to the grid's fixed point", and the
   page states one bound: the Jacobi bound `beta/(1-beta) * max|V_n - V_{n-1}|`, with synchronous sweeps (project.html,
   Conventions, Iteration and Certified error). The in-place (Gauss-Seidel) sweep and the residual-stop alternative are
   not valid alternatives of this project (ruling 31, plans/FINAL-ARCHITECT-RULINGS.md, closing verifier row M5-d-r1-06).
   Both fail the suite's certified-error formula test on seeds 0-49 (0 of 50 each; `ledgers/M5/alternatives/not_accepted/`).
   The plan's alternatives bullet (plans/M5-build-plan.md:304-306) is amended to say so; the page is unchanged. The five
   alternatives in `ledgers/M5/alternatives/` (alt1 to alt5) pass seeds 0-49, 50 of 50 each.
4. **Closed-form test (plan §5.3 item 5, "if kept") omitted.** No closed form is stated for `sqrt` utility with `k**alpha`
   production in the plan or the architect decisions.
5. **Iteration budget.** The test allows `iterations <= a priori count + 1`, where the count is the least `n >= 0` with
   `beta**n * sqrt(max(grid)**alpha) / (1 - beta) <= tol`. The count is written into project.html (Conventions), so the
   bound the test uses is stated to the learner.
6. **`solve` takes a `Mapping[str, Any]` for `params`** (plan §5.3 wrote `dict[str, float]`); a mapping is the wider type.
7. **Mutants.** The plan asks for at least three; the builder brief asked for ten. Fourteen single-change mutants are in
   `ledgers/M5/mutants/`, generated from the reference by `ledgers/M5/scripts/make_variants.py`. They are killed by
   `tools/mutate_graders.py --unit M5 --seeds 0-9`, which reports 14/14. Mutant `m14` (a stored answer for seed 0's
   parameters) is killed by the budget test on seed 0 only, because it ignores `max_iter`; its description says so.

## Requests

- **NOTATION_REQUESTS:** none that block. The page uses `\mathcal{B}` (a KaTeX built-in, not a registry macro), `\lVert`
  and `\rVert` (built-ins), and `\R` (registered). The plan's `\norm` macro is not used. If the architect wants
  `\mathcal{B}` and `\norm` registered, the request is: symbol `\mathcal{B}`, meaning the discounted Bellman operator,
  needed for Conventions, Lab 2 and the brief; and `\norm`, meaning the sup norm.
- **GLOSSARY_REQUESTS:** none from this builder. Terms the project defines in prose (grid, feasible saving, sup norm,
  certified error) are defined in the Conventions subsection, without a `<dfn>`, as the plan requires for undeclared terms.
- **DATA_REQUESTS:** none. The instances are generated parameters, labelled SIMULATED in `grader/instance.py`.
- **REFERENCE_REQUESTS:** none. Both registry keys cited (`abbott2015understanding`, `rudin1976principles`) are used only
  in the reading list; the page attributes no statement to either.
- **CONTRACT_CHANGE_REQUESTS:** none (no Atlas milestone for M5).
- **DAG_DEFECTS:** none found by `check_dag.py --unit M5`. The project names the M5 concepts it uses and links the first use
  of `contraction-mapping` (L07) and `value-function-iteration` (L09). It does not use the term "Bellman equation", which
  is M7's concept (plan §0.3 and architect Q1).

## Gaps outside this builder's rows

- `course/modules/M/M5/cards.json` is missing (Builder F). `check_pages.py --unit M5` reports only this problem.
- `page_smoke.py` has been run for the project page only, after all other checks pass (see the report).

## Known limitations of the grader and labs

- The lab twins and the grader use the standard library only (plan §10 item 4 and architect Q10). Rung-3 numbers are
  printed with fixed seeds (`random.Random(7)` in Lab 3); the grader instances are seeded by `QF_SEED`.
- Lab 3's contraction line allows a `1e-12` rounding margin, because the observed ratio reaches `beta` exactly on this
  instance. The page says so.
- The Lab 1 "actual error" agrees with the certified error to nine decimals in that run. The page states that this is a
  property of that instance, not a general fact.

## Builder F (cards, `course/modules/M/M5/cards.json`)

Scope: `cards.json` only. Lessons L01–L10 were read in full and not edited. Defects found in them are listed below for their owners.

### Cards written

- 185 cards, `M5-c001` to `M5-c185`: L01 16, L02 18, L03 15, L04 19, L05 16, L06 16, L07 20, L08 19, L09 22, L10 24.
- Grades: 93 T (each with a `basis` naming its proof section), 34 C (each with a `basis` naming the lab, or Problem E1 for the L08 iteration counts), 58 without a grade (definitions, misconceptions, and the prose-defined terms).
- Coverage: every `<dfn>` and every definition in prose, every proposition, lemma, theorem, corollary and named example with a claim, all 30 misconceptions, and all key-results rows. Rows that restate a theorem are covered by that theorem's card. Rows without one have their own card (L01 row 6, L04 row 7, L07 rows 1 and 7, L03 row 6, L08 row 7, L09 row 6).
- No card cites a registry key, since the plan makes M5 empirical-free. Every lab-printed number on a card appears in the lesson's lab output block.

### Defects in the lessons (not edited; owners to fix)

1. **Raw `<` in math breaks the HTML** (`<` followed by a letter is parsed as a start tag, so text after it is lost). Escape as `&lt;`.
   - `L04.html:240` (`d(x,y)<r`) and `L04.html:249` (`d(x,z)...<d(x,y)+s=r`).
   - `L05.html:215` (`0<a<1`), `L05.html:220` (`0<a^{n}`), `L05.html:315` (table row, `0<a<1`).
   - `L06.html:56` (`n_1<n_2`), `L06.html:70` (`j<k`), `L06.html:234` (`M-1/n_k<f(x_{n_k})`), `L06.html:282` (`n_1<n_2`).
   - Found by a stdlib `html.parser` scan for start tags outside the HTML vocabulary.
2. **L07 misconception 1 (`L07.html:311`) and the quiz explanation (`L07.html:477`) say the ratio "tends to one for far-apart pairs".** The proof shows the ratio tends to 1 for `x = y + h` with `y → ∞`, a pair far from the origin with a fixed separation. Reword both.
3. **L08 Problem R2 (`L08.html:392`)** concludes "so no fixed point exists in R^G at β = 1" from unbounded iterates. That inference does not hold in general. The valid argument is `V(0.25) ≥ 0.5 + V(0.25)`, which no function satisfies. Add it.
4. **L08 canon break 1 (`L08.html:275`)** says "the proof of Theorem 2.1" without naming Lesson 7. Name it, as the Definition 1.1 link does.
5. **L10 (`L10.html:80`)** says P4 is taken "from the definition". P4 is not proved on the page. State it as a named prerequisite, or prove it.
6. **L05 lab docstring (`tests/labs/M5/lab-M5-L05-1.py`, line 9)** says Part A measures the distance to "the pointwise limit 0 on [0, 1]". The limit is 0 only on [0, 1). The code measures the distance to the constant 0 on the grid. Reword.
7. **L09 (`L09.html:272`)** says `naive_factor_times_step` "equals nine times the step to the printed digits". The printed step `0.0000009534` times 9 is `0.0000085806`, not `0.0000085808`. The match holds only for the unrounded step. State that basis. Also "stock" (`L09.html:272`, `:484`) is used for the state, which is never defined. Use "state" or "capital".
8. **L08 iteration counts (Misconception 2 and Problem E1)** give 40 at β = 0.5 and 527 at β = 0.95. The lab does not print them. I reproduced both by setting BETA in a copy of the twin, so they are correct. Either print them from the lab or keep the basis stated as it is.
9. **Stray file**: `tests/labs/M5/lab-M5-L10-1.py-e` (not created by this builder). Delete it once its owner confirms.

### Known limitations

- L07 Proposition 3.1 and Example 3.3 are graded T, but their proofs use "Input I" (fundamental theorem of calculus) and "Input II" (monotonicity of sin on [0, 1]), which are named and not proved. The cards say so in their basis.
- L10 Theorem 3.1 is graded T, and its proof uses (P1) to (P4) from M2. I checked the M2 locators: M2 L09 Definition 1.3 and Lemma 1.2, M2 L10 Theorem 2.1, M2 L11 Lemma 1.1, and M2 Example 3.2 (L09 and L11). (P4) is unproved (defect 5).
- The L10 closed forms for Example 3.3 (right- and left-tag sums) are graded C with a lab basis, because the page states them without a derivation. I checked them by algebra: the right error is `(3n−1)/(6n²)` and the left error is `−(3n+1)/(6n²)`.

### Requests

- GLOSSARY_REQUESTS: none. The terms used on the cards (feasible set, value function, policy, tagged partition, mesh) are defined in prose on the lesson pages without a `<dfn>`, as the plan requires.
- NOTATION_REQUESTS: none beyond the plan's §7.4 and the architect's decision.
- DATA_REQUESTS: none.
- REFERENCE_REQUESTS: none.
- CONTRACT_CHANGE_REQUESTS: none.
- DAG_DEFECTS: none. `check_dag.py --unit M5` passes.

### Checks run (from `/tmp/quant-b2`)

- `.venv/bin/python tools/check_pages.py --unit M5`: `check_pages M5: PASS`
- `.venv/bin/python tools/check_dag.py --unit M5`: `check_dag M5: PASS`
- `.venv/bin/python tools/check_projects.py --unit M5`: `check_projects M5: PASS`
- `.venv/bin/python tools/run_labs.py --unit M5`: `run_labs M5: PASS (13/13)`
- `.venv/bin/python tools/run_graders.py --unit M5 --seeds 0-49`: `run_graders M5: PASS (reference 50/50 seeds, slowest 0.2 s)`
- `page_smoke.py` was not run. No page or lab file was changed by this builder, and the cards file is not swept by it.
- ruff and mypy were not run. This builder wrote no `.py` file inside the repository; the scratch script is in `/tmp/m5cards/`.

## Round-2 fixer, slice d (project page, grader, alternatives)

- **Alternatives (verifier row M5-d-r1-06).** The page's solver contract is synchronous sweeps with the
  `beta / (1 - beta)` last-change certificate, stopping at the first sweep with certified error at most `tol`. The
  in-place sweep and the residual-stop-with-residual-bound alternatives contradict that contract, so they cannot pass
  it (0 of 50 seeds). They are moved to `ledgers/M5/alternatives/not_accepted/` with a README. Replacements, both
  synchronous and both passing seeds 0-49 (50 of 50 each): `alt1_functional_reduce_and_tuples.py` and
  `alt2_class_with_precomputed_feasible_tables.py`. The in-place sweep stays a stretch item (page Rung 4), and the
  architect may still choose to amend the page contract to admit it; that would also need the formula test to be
  restated for each solver.
- **Named invalid input, one-point grid (rows M5-d-r1-21 and M5-d-r2-34).** `[1.5]` is added to the invalid-grid
  parametrization (`one-point-first-above-one`). Mutant `d3_02` is killed.
- **Feasibility tie tolerance (row M5-d-r2-33).** New test `test_successor_within_a_tie_tolerance_above_the_resources_is_infeasible`
  uses a successor `0.5 + 5e-13`. Mutant `d3_01` is killed.
- **Failure output.** Every test function now sets `__tracebackhide__ = True`, so a failed check does not echo its
  source (which contains literal expected values in some tests and docstrings). The page sentence on `--assert=plain` is
  reworded to match.
- **Count.** The suite collects 100 checks (was 98). The page quotes 100.
- **Exemplar blinding (rows M5-d-r1-13, M5-d-r1-14).** Not addressed by the fixer. Ruling 23 assigns blind scoring to a
  separate agent that never opens the project page; the fixer has read the annotations and does not score.
