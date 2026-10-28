# E1 open items and gaps (Builder E: project page, grader, project labs)

Requests and gaps raised by Builder E under the BUILDER_RULES §10 output contract. Each item is a gap the page
states, a change to the plan that the architect should confirm, or work for a later round.

## Plan corrections (the architect should confirm)

1. **Unit of `a`.** Plan §5.2 says `a` is "cents per trade: the choke fee". Under the plan's own demand
   `Q(f) = a - b*f` (trades), `a` is in trades: the volume at a fee of zero. The choke fee (the fee at which volume is
   zero) is `a/b`, in cents. The closed forms of §5.3 (`(a + b*c)/(2*b)` and so on) are consistent with `a` in trades,
   `b` in trades per cent, and `c` in cents per trade. The page uses these units.
2. **Cost condition.** Plan §5.2 requires `a > b*c > 0`, but the exception table (§5.4) names `c < 0`. With `c = 0`
   the product `b*c` is zero and the stated validity condition fails, so `c = 0` is a named condition in the page:
   `c <= 0` raises `ValueError("c must be positive")`. Tests cover `c = 0` and `c = -1`.
3. **Volume is an integer, the exact volume is not.** `volume_trades` must be an `int` (plan §5.2), but the exact
   Cournot volume is `200/3` for the reference case. The page adds one rule: `volume_trades` is the exact volume rounded
   once to the nearest whole trade, a tie going up. No money output uses the rounded volume; consumer surplus,
   welfare and deadweight loss use the exact volume.
4. **Test count.** Plan §6 lists the test categories, not a count. The suite collects 57 tests (`pytest
   --collect-only`), and the page quotes 57.
5. **Mutants and alternatives.** Plan §6 requires at least three mutants and five alternatives, written by the verifier.
   Builder E wrote ten mutants (`ledgers/E1/mutants/`, one change each, all killed on seed 0) and the five alternatives
   (`ledgers/E1/scripts/alt1_closed_form.py` to `alt5_float_half_up.py`). The verifier should still write its own.
6. **Memo file names.** The plan names `memo.md` but no folder. The page puts `market_structure.py`, `memo.md`,
   `run_report.py` and `self_assessment.md` at the repository root.
7. **Lab 3 shows the closed forms.** `lab-E1-project-3` computes the table with the closed forms, as the M1 Lab 3
   precedent does. A public lab therefore shows the formulas. The architect may prefer a lab that prints only the
   expected table. The grader is unaffected.
8. **Derivations on the page.** Architect decision Q4 says the page proves the closed forms. Propositions 1 to 5 do
   that, graded T with their hypotheses. Proposition 3 (Bertrand) is proved for fees in `[0, a/b]` with the equal-split
   tie rule, and the page says so.

## REFERENCE_REQUESTS

None. The only key cited is `varian2014intermediate`, in the reading list, with no passage locator read, so no statement
on the page is attributed to it.

## NOTATION_REQUESTS

None. The page uses standard KaTeX commands (`\int`, `\max`, `\lfloor`, `\rfloor`, `\big`, `\,`).

## GLOSSARY_REQUESTS (defined in prose on `project.html`; none is a registered concept)

- inverse demand, the fee at volume Q: `f(Q) = (a - Q)/b` (project page, Definitions)
- volume, fee, gap `d = a - bc`, competitive benchmark (project page, Definitions and Model)
- best response, equilibrium (in words, no Nash name), consumer surplus, welfare as total surplus, deadweight loss
  (project page, Definitions)

## DATA_REQUESTS

None. The inputs are integers from `grader/instance.py` (SIMULATED) and the reference case, an input of the
specification. No dataset is read.

## CONTRACT_CHANGE_REQUESTS

None. E1 has no Atlas milestone.

## DAG_DEFECTS

None. `check_dag.py --unit E1` passes. The project page has no concept links. The page does not use `nash-equilibrium`,
`lagrange-multiplier`, `convex-function` or `first-welfare-theorem`, and it names no concept owned by another unit.

## Dependencies on other builders

- The project page links `index.html#placement` (the hub's placement section) and `L09.html`. Both must exist at
  integration.
- The hub's `data-hours-project` must be `30` (it is `30` on the project page).

## KNOWN_LIMITATIONS

- **Browser run.** The grader passes locally on seeds 0 to 49 (`run_graders.py`) and `page_smoke` was run at the end
  for this page. See the report for its exact result. The Pyodide run of the labs and the grader was not checked by
  a person.
- **Model.** The three structures are a proposal the architect accepted (Q4). Linear inverse demand, constant cost, and
  two exchanges are stated as limits on the page. No parameter is estimated.
- **Bertrand tie rule.** Proposition 3 uses the equal split. Other tie rules are not covered, and the page says so.
- **Cournot uniqueness.** Proposition 2 proves uniqueness among nonnegative quantities with the stated profit. It
  does not cover other demand functions.
- **Rounding of fees.** Fees are exact in the model and rounded only at output. The model does not make the exchange
  charge a whole-cent fee.
- **Tool quirk.** `check_pages.py --page project` applies the lesson rules (misconceptions, lesson sections, a
  mark-complete button) to a project page. The same output appears for M1's project page. The unit-wide run
  (`check_pages.py --unit E1`) reports nothing for the project page.
- **Rubric.** The level descriptors are observable, but no learner has scored the exemplars.
- **Alternatives and mutants.** The mutants and alternatives are Builder E's. The verifier should write its own.
