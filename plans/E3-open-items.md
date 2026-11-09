# E3 open items (Builder D: L07, L08)

Scope of this file: the two lessons written by Builder D, `course/modules/E/E3/L07.html` and `L08.html`, and their twins
`tests/labs/E3/lab-E3-L07-1.py` and `lab-E3-L08-1.py`. Items are for the orchestrator and the architect. Nothing here is
learner text.

## 1. Cross-lesson anchors the pages link to (integration)

L07 and L08 link to these definitions, which Builders A to C must place with the same ids:

- `L01.html#def-expected-utility` (L07 meta row; L08 meta row)
- `L02.html#def-certainty-equivalent` (L08 meta row)
- `L03.html#def-crra-utility` (L08 meta row; Model 1 uses CRRA with gamma = 2)
- `L04.html#def-first-order-stochastic-dominance` (L07 meta row and Section 2). L07 also states the finite-support
  theorem of L04 (expected utility with a nondecreasing u never ranks a dominated lottery higher). That theorem must
  exist in L04 as stated; L07 cites it by lesson, not by key.
- `L05.html#def-epstein-zin-preferences` and `L05.html#def-elasticity-of-intertemporal-substitution` (L08 Section 3).
  L08 Definition 3.1 fixes the two-date form `V0 = [(1-beta) c0^rho + beta (E c1^(1-gamma))^(rho/(1-gamma))]^(1/rho)`
  with `rho = 1 - 1/psi`, `psi` the EIS and `beta` the discount factor. L05 must use the same symbols and form.
- `L06.html#def-prospect-theory` and `L06.html#def-loss-aversion` (L07 and L08 meta rows). L06 must use gains exponent
  alpha and losses exponent delta, with `v(x) = -lambda(-x)^delta` for losses. L08 Model 2 uses alpha = delta = 1/2 and
  lambda = 2 as stated parameters.

Until those pages exist, `check_pages`, `check_dag` and the page-level links are not checked against them.

## 2. Deviations from the plan (for the architect to confirm)

1. **Name of the weighted value.** The plan calls the L07 exhibit "the 1979-form". `kahneman1979prospect` was not read
   beyond its registry record (title and year), so no functional form is attributed to it. L07 calls the value
   "non-cumulative weighted value" (Definition 1.2). Its mention of the 1979 paper is an ungraded naming sentence
   under ruling 39 (L07.html:80): it names the registry title, carries no data-grade and no data-cite, and cites no result.
2. **Weighting symbols.** The plan's `w` for the weighting function clashes with `w` for wealth (plan section 4). L07
   uses `omega` for the weighting function and `eta` for its exponent. Both are new local symbols, defined where used.
   No symbol is registered.
3. **Weighting exponent.** The plan lists `alpha`, `delta` as "value and weighting exponents". L07 uses `alpha` for the
   gains exponent, `eta` for the weighting exponent, and does not use `delta` (L08 Model 2 uses `delta`, as the losses
   exponent of L06).
4. **Epstein–Zin in the four-model lab.** The architect decision asks for a two-date convention. L08 uses a gamble at
   the last date (date 1 only, with date-0 consumption fixed at initial wealth). Under that convention the
   Epstein–Zin certainty equivalent equals the CRRA one for every psi and beta (Proposition 3.2, checked in Lab 1,
   part B), so the Epstein–Zin row duplicates the expected-utility row. The lesson states this as the finding. The
   architect should confirm this is the intended four-model design, or name a gamble that resolves before a later
   consumption date (Remark 3.3, Problem R1).
5. **Alpha-MEU.** The architect decision names "max-min (alpha-MEU)". L08 defines alpha-MEU in general (Definition 1.2),
   computes alpha = 1 (maxmin, the model row) and alpha = 1/2 (a sensitivity row). At alpha = 1/2 the row equals
   expected utility here, because the prior set is symmetric (Remark 4.2). A different prior set would show a difference.
6. **Bisection.** Every model in L08 has a closed form, so the bisection is used for the Epstein–Zin certainty
   equivalent (a stated tolerance, 1e-9 cents) and for a check of the prospect inverse, not for the reported prospect
   value. The architect decision asks for bisection "without a closed form"; none is needed for the reported values.
7. **Prize bet and Ellsberg-type check.** The two-urn check (L08 Example 2.5) uses a stated prize of 100 CU and the full
   prior set of red counts 0 to 90. It does not use the paper's numbers, which were not read.

## 3. Registry and citations

- The three registry records, `kahneman1979prospect`, `ellsberg1961risk` and `gilboa1989maxmin`, are verified in
  `references/references.json` with `used_by` E3. No locator was read, so none is given. Under ruling 39 the three
  registry-title claims are ungraded naming sentences, not graded results: `kahneman1979prospect` (L07.html:80),
  `gilboa1989maxmin` (L08.html:67) and `ellsberg1961risk` (L08.html:133). Each names the registry title, carries no
  `data-grade` and no `data-cite`, and cites no result. They have no grade-C row in the key-results tables of L07 and
  L08. Cards E3-c134, E3-c157 and E3-c158 carry no grade and no citation key.
- L07 and L08 make no claim about how people weight probabilities or behave under ambiguity, and quote no magnitude of
  loss aversion or of any risk-aversion coefficient.
- REFERENCE_REQUESTS from plan section 8.1, relevant to these lessons: R2 (full second-order dominance characterisation,
  used only as a plan item; L04 proves the finite case), R3 (rank-dependent repair, named in L07 Section 3 but not
  derived), R4 (ambiguity generalisations, not used), R5 (two-sided loss-aversion evidence, needed before any magnitude
  of loss aversion is quoted; L06 and L08 quote none). None of R1 to R6 is admitted, so the lessons cite no source for a
  magnitude.

## 4. Gaps in the content, stated for the verifier

- L07 Observation 1.5 (the shape of omega on the grid) is a finite check, not a theorem, and is not graded as a claim.
  The key-results row grades it C with the basis "Lab 1, part A (finite grid of 1001 points)".
- L07 Proposition 2.2 relies on the closed form of Example 1.4 for omega(3/10)/omega(3/5); the threshold comparison is
  exact, and the printed ratio (0.73045450) is computed in floating point with a margin of about 0.064 above the
  threshold at alpha = 1.
- L08 Model 2 (prospect value) and Model 3 (Epstein–Zin bisection) are floating point. The rounding rule refuses a
  value within 1e-6 cents of a half cent. None of the reported values is within that distance.
- L08 Proposition 2.4 and Theorem 2.2 are general (any strictly increasing utility). Lab 1 checks CRRA only.

## 5. Notation and glossary

- No NOTATION_REQUESTS for these lessons. The plan's optional `\CE` macro was not requested, because the lessons use
  `\mathrm{CE}` throughout.
- No GLOSSARY_REQUESTS. Plain terms ("prior set", "maxmin expected utility", "alpha-MEU", "risk premium", "non-cumulative
  weighted value", "two-date value") are `<dfn>` without `data-concept`, which `check_dag` skips.

## 6. Hours

L07 and L08 each declare `data-hours="7"`. The project (14 h) and the hub split (56 + 14 = 70) belong to the hub, which
Builder A writes.

## 3. Project, grader and ledger items (Builder E)

Scope: `course/modules/E/E3/project.html`, `course/modules/E/E3/grader/`, `tests/labs/E3/lab-E3-project-1..3.py`,
`ledgers/E3/mutants/` and `ledgers/E3/scripts/`, and the completion-markup change in `course/modules/E/E3/L04.html`.

1. **Plan deviations, for the architect to confirm.**
   - The plan's §6.7 dominance tests (FOSD and SOSD verdicts) and mutants 6, 7 and 9 of §6.5 (dominance and
     Epstein–Zin) have no interface: §6.2 names no dominance function. They are not tested. Mutants 6 to 10 were replaced
     by the student errors that apply to `elicit.py` (see `ledgers/E3/mutants/`).
   - §6.2 says the responses are `{pair_id, choice}`. The engine needs each pair's lotteries, so the response carries
     `prizes_a`, `probs_a`, `prizes_b`, `probs_b` and `choice`, with probabilities as `"numerator/denominator"` text.
     The three signatures are unchanged.
   - §6.2 says "round half up". The rule is stated as `floor(x + 1/2)`: an exact half goes toward plus infinity, so
     -0.5 gives 0 and 2.5 gives 3.
   - §6.7 proposed "within 4 standard errors on at least 47 of seeds 0 to 49". The suite instead checks each seed
     against 5 standard errors. Seed 2 has |z| = 4.89 for lambda (see KNOWN_LIMITATIONS); a 4 SE bound fails there.
     Decision needed (§10 Q12).
   - The plan's near-indifference pair design (§6.7 `instance.py`) gave choices that are almost coin flips, and the
     estimator drifted to lambda near 0 on seeds 0 and 2. `instance.py` now sets a target certainty equivalent within
     $50 of A's, and the closest of 30 candidate lotteries is B. The 50 seeds converge with interior estimates.
   - `instance.py` docstring corrected to the code: 200 pairs, at least 100 with a mixed lottery.
   - Found while checking the alternatives: for some participants the likelihood is higher at gamma near 0 than at
     the truth, so the maximum-likelihood estimate sits on the edge of the domain. `estimate` then raises (the observed
     information is not positive definite), and a local maximum hides the edge. `instance.py` now rejects such a draw:
     the likelihood at the truth must exceed, by 0.5, its best value on a grid of lambda and kappa at gamma = 0.001.
     Checked: all 50 seeds 0 to 49 and their second participants (seeds 7919 to 7968) estimate with gamma inside (0, 1)
     and log-likelihood at the estimate at least that at the truth.
2. **Lab 3 is a twin of the reference case, not a call to `elicit.py`.** A lab cannot import the learner's module. The
   page tells the learner to copy the lab and substitute a call to their own `estimate`, and the lab prints the reference
   numbers. Its estimator is a grid plus Newton's method with finite differences of step 1e-6, so it is a second
   implementation; it agrees with `reference.estimate` on the same twelve answers to the printed digits
   (gamma 0.6352, lambda 6.1503, kappa 2.0201, log-likelihood -7.1445, standard errors 0.32, 9.59, 1.86).
3. **L04 layout fix (markup only).** The 69 px horizontal scroll at 360 px came from an unbreakable quiz option: a
   label is a flex row and its KaTeX span is `white-space: nowrap`. Five option labels now wrap their text in a `<span>`,
   and the six quiz fieldsets carry `style="min-inline-size: 0"`, as L07 does. No text changed.
4. **Completion lab markup.** The page shows the blanked code for Lab 2 and embeds its output; the twin is the completed
   solution. `tools/embed_labs.py` would insert the twin unblanked, so do not re-run it on that section without
   restoring the blanks.
5. **Pyodide timing.** The suite ran in CPython in about 0.5 s per seed, and `estimate` takes about 0.25 s per call.
   In Pyodide, `page_smoke` runs the 26 checks in 1.8 s in total (item 7).
6. **Alternatives and mutants (final).** `ledgers/E3/scripts/run_alternatives.py --seeds 0-49`: alt1 to alt5 PASS
   50/50 each. `tools/mutate_graders.py --unit E3 --seeds 0-9`: 10/10 killed. Two alternatives first failed on seeds 47
   and 49 (a compass search and Nelder-Mead stopped short of the maximum); both now end with a Newton polish, and the
   failure they showed was the boundary participant of item 1, not a suite error.
7. **Gates run by Builder E.** `tools/run_graders.py --unit E3 --seeds 0-49`: PASS (reference 50/50, slowest 1.1 s).
   `tools/check_projects.py --unit E3`: PASS. `tools/run_labs.py --unit E3 --page project`: PASS (3/3).
   `tools/page_smoke.py --unit E3 --pages project L04`: PASS (both pages; in-browser grader 26 of 26 in 1.8 s).

## Architect ruling (batch 3, round 9): plan 6.5 items 6, 7, 9

The project specification defines no dominance function and no Epstein-Zin model, so `reference.py` has no code path
that those mutants could alter. Items 6 (FOSD inequality reversed), 7 (SOSD on CDFs) and 9 (Epstein-Zin exponent swap)
are therefore not applicable and are dropped. The FOSD and SOSD behaviour is tested through the specified
`certainty_equivalent_cents` ordering (two witness pairs, FOSD and SOSD, in `test_project.py`). Adding a dominance
interface to the specification would be a scope change and is not made.

## Architect ruling (batch 3, round 13): project exemplars are excerpts

The two rubric exemplars on the project page are excerpts of memos (103 and 375 words), not full reports of 350 to
800 words, and the page says so. The build plan wording is amended to match. Full-length exemplars are not required:
their purpose is to calibrate the rubric levels, and the rubric text itself states the full-report length.
