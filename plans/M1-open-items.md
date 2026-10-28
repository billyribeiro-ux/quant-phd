# M1 open items and gaps (Builder A: hub, L01, L02, L03; 2026-10-27)

Requests and gaps raised by Builder A under the BUILDER_RULES §10 output contract. Nothing here is a claim the
lessons rely on. Each item is a gap the pages state honestly, or work for a person or a later round.

## DATA_REQUESTS
None. The plan (Real-data policy) requires no embedded data for M1, and the labs and grader compute from formulas.

## REFERENCE_REQUESTS
None required by L01 to L03. The only registry key the unit cites is `velleman2019prove`, which the curriculum names
as the source for proof technique (`curriculum/01-foundations.yaml:111-112`). No passage locator from it has been
confirmed, so no statement on L01 to L03 is attributed to it. The pages say so in each References section.
Open: a person with the book should confirm passage locators for any proof-technique statement a later lesson wants
to attribute. Until then such a statement is not made.

## NOTATION_REQUESTS
None. The lessons use standard KaTeX commands for the logic and arithmetic symbols (for example `\forall`, `\exists`,
`\neg`, `\Rightarrow`, `\gcd`). No registered macro changes meaning.

## GLOSSARY_REQUESTS (terms defined inline in L01 to L03; the glossary is generated from the curriculum)
- statement, predicate, domain (L01 §1, Definition 1.1)
- quantifiers, the empty-domain convention (L01 §2, Definition 2.1 and Remark 2.2; concept `quantifiers`)
- direct proof, even and odd integers, divisibility, implication (L02 §1, Definitions 1.1 to 1.3; concept `direct-proof`)
- contradiction, coprime integers and lowest terms (L02 §2, Definitions 2.1 and 2.4; concept `proof-by-contradiction`)
- natural logarithm (L03 §1, Definition 1.1; concept `exponential-and-logarithm`)
- Curriculum decision needed: the core text names "sets", "functions", "algebra" and "sequences" without listing them
  in `introduces` (Architect decision Q3). The lessons use them as prose with no `<dfn>`, as decided.

## CONTRACT_CHANGE_REQUESTS
None. M1 has no Atlas milestone.

## DAG_DEFECTS
None found by `check_dag.py --unit M1` on the three lessons and the hub. The concept `limit` is not used anywhere in
L01 to L03, following Architect decision Q1. Lesson 4 (Builder B) is responsible for stating the compounding limit
as a numerical observation without the concept.

## KNOWN_LIMITATIONS
- Assumptions, not constructions. L03 takes the exponential as given with properties A1 to A3. It does not construct
  the exponential by a series or a differential equation, and it does not show the existence of the function
  beyond taking A3 as given. A reader who needs that construction must go to a source outside the unit.
- Lab evidence is floating-point. The L03 lab checks identities to a tolerance of 1e-12 on finite grids. Those are
  checks of the library functions, graded C, and not proofs. The proofs in L03 use A1 to A3.
- The L01 and L02 labs enumerate finite domains. Each count is exact for its domain, and each is graded C. A
  refutation by counterexample is a valid proof of falsity, but a finite search with no counterexample proves nothing
  about other domains; the pages say so.
- Placement skill checks (hub) test rung-1 and rung-2 skills whose content is taught in L06 and L07 and in the
  project. The skill items are written to match the plan (the worked-example task and the completion step), but the
  full skill set is not taught before L06, so a reader who skips to the placement early may face material not yet
  taught. The hub says that the skill checks are for skipping rungs 1 and 2 only.
- The hub's lesson map links L04 to L08 and the project. At the time of this report the L04 to L08 pages exist (other
  builders), `project.html` does not, and `cards.json` does not. `check_pages.py --unit M1` therefore reports only
  those two missing files, and the hub's hours split (70 + 30) matches the lesson hours declared by the eight pages.
- Cards (`cards.json`) are Builder E's responsibility after Builders A to C finish, so they are not written here.

# Builder C additions (L06, L07, L08; 2026-10-27)

Requests and gaps raised by Builder C. Each is a gap the pages state, or work for a later round.

## Builder C: GLOSSARY_REQUESTS (defined inline, one term each)
- proof by induction, the induction principle (L06 §1, Definition 1.1 and Theorem 1.2; concept `mathematical-induction`)
- geometric series, finite (L06 §2, Definition 2.1; concept `geometric-series`)
- annuity and annuity due (L07 §1, Definition 1.1; concept `annuity`)
- perpetuity and its value (L07 §2, Definition 2.1; concept `perpetuity`)
- growing perpetuity (L07 §3, Definition 3.1; concept `growing-perpetuity`)
- loan amortization schedule (L08 §1, Definition 1.1; concept `amortization-schedule`)
- level payment (L08 §1, Proposition 1.2); nominal annual rate and the monthly convention i = j/12 (L08 §1)

## Builder C: REFERENCE_REQUESTS
None. L06 to L08 cite no registry key. `velleman2019prove` is not cited on these pages: no passage locator from the
book has been read, so no statement is attributed to it. The L06 References list is therefore empty.

## Builder C: DATA_REQUESTS
None. The L08 loan is illustrative input, labelled as such in the lab and on the page.

## Builder C: CONTRACT_CHANGE_REQUESTS, NOTATION_REQUESTS
None. \(\mathrm{PV}_n\) and \(\mathrm{PV}\) use standard KaTeX, not a registered macro.

## Builder C: DAG_DEFECTS
None found: `check_dag.py --unit M1` passes with all eight lessons present. The links from L07 and L08 to L05 and
L06 are to definitions that exist (`def-present-value`, `def-discount-factor`, `def-mathematical-induction`,
`def-geometric-series`, `def-annuity`), and the concept `limit` is not used on any page.

## Builder C: KNOWN_LIMITATIONS
- The perpetuity value (L07 Definition 2.1, Theorem 2.4) is defined by an ε-statement about partial values, not by
  the concept `limit`, following Architect decision Q1. The growing perpetuity uses the same definition (Theorem 3.3).
- The well-ordering principle is taken as the defining property of the natural numbers (L06 §1). It is not proved.
- L06 Lab 1 checks the closed form in exact arithmetic (420 checks), and its float lines are graded C. L07 Lab 1 part B
  and L08 Lab 1 part B are floating-point or cent arithmetic on one illustrative input each, graded C.
- The L08 cent schedule (Lab 1, part B) takes three conventions (interest to the nearest cent with halves up, the
  regular payment to the nearest cent, a final payment that closes the balance). These are conventions, stated in
  §3 of the page, and the lab shows one loan only.
- Labs were run with local CPython 3.14 (`python -I -W error`) through `run_labs.py`. They were not run in Pyodide,
  and `page_smoke.py` was not run, as instructed for the parallel round.
- `cards.json` for L06 to L08 is not written here; it is Builder E's responsibility, and the quiz sections already
  point at `cards.json`.

# Builder D additions (project.html, grader/, lab-M1-project-1 to 3; 2026-10-27)

Requests and gaps raised by Builder D. Each is a gap the page states, or work for a later round.

## Builder D: DATA_REQUESTS
None. The project uses no embedded data. The loans in Lab 1, Lab 2 and Lab 3 are illustrative inputs, and the
grader instances are SIMULATED (`grader/instance.py`).

## Builder D: REFERENCE_REQUESTS
None. The only key the project cites is `velleman2019prove`, in the reading list, with no passage locator. The page
attributes no statement to it. The proof methods of Appendix A are derived on the page.

## Builder D: NOTATION_REQUESTS, GLOSSARY_REQUESTS, CONTRACT_CHANGE_REQUESTS
None. The project page uses KaTeX built-ins only (\varepsilon, \ne, \times, \,) and no registered macro. It defines no
term; it links annuity, perpetuity, growing perpetuity and amortization schedule to their definitions in L07 and L08.

## Builder D: DAG_DEFECTS
None found: `check_dag.py --unit M1` passes.

## Builder D: KNOWN_LIMITATIONS
- Exemplars A and B and their annotations were written by Builder D. An independent verifier must check every number
  they quote against Lab 3's output and every proof in them (A1 to A4), before the rubric is trusted.
- The project's proofs (A1 to A4) are graded by rubric, not by machine. The suite checks only the code.
- Not run: `page_smoke.py` (asked not to run in parallel), a Pyodide run of the grader and of the completion lab, and a
  360 px layout check. The page's code blocks scroll inside their own box, as the stylesheet defines for `pre`.
- The grader suite runs 65 checks, from `pytest --collect-only` on the final `test_project.py`. The page quotes 65.
  If the suite changes, the page's count must be recounted.
- The cent rule has no exact-tie instances: `instance.py` redraws a loan whose exact schedule has an amount within
  1e-6 of a half cent. The tie-free condition is what lets five correct implementations agree on integers.
- The second instance (`make_instance(SEED + 7919)`) is the suite's guard against a hard-coded answer. Builder D did
  not run a hard-coded-answer mutant; that mutant is left to the verifier's required mutants.
- Mutants checked by Builder D (not the verifier's set): annuity-due used for the ordinary factor; growing perpetuity
  without the r > g guard; the nominal rate used as a monthly rate in the schedule; the last payment not adjusted. All
  four are killed by the suite on seed 0. Five correct variants (expm1/log1p floats; exact Fraction arithmetic with
  Decimal half-up; a plain int cast; a factor-reciprocal payment; a while-loop schedule) pass on seeds 0 to 49.
- The final payment differs from the level payment by 120 cents in Lab 3 and by 343 cents in Lab 1. Both are real
  outputs of the cent rule, not errors. The bound n(1+i)^n + 1 cents is derived in Appendix A4 and is loose.

# Builder E additions (cards.json, L01 to L08; 2026-10-27)

Requests and gaps raised by Builder E. Each is a lesson-text or grading defect for the architect or the lesson owner.

## Builder E: LESSON_TEXT_DEFECTS (cards follow the current text; these lines need an owner's decision)
- L06 Key results, row "The exact-fraction check of Theorem 2.2 passes ... (420 checks)": graded T with source
  "Theorem 2.2; Lab 1 (exact arithmetic)". The pass is a finite enumeration, so the card grades it C, as L02 grades
  its equivalent enumeration row. The row should read C.
- L06 Misconception 2 says the polynomial is prime for n from 0 to 39 "checked directly"; Lab 1 of L06 runs no such
  check. The mathematical fact is correct, but the phrase "checked directly" has no lab behind it.
- L02, L03 and L01 labs are labelled "(SIMULATED range)" or "(SIMULATED rate)" or "(SIMULATED domain)" in their
  Empirical problems (L01 E1 to E3, L02 E1 to E3, L03 E1 to E3). These are exact or deterministic computations, not
  simulations. BLUEPRINT and BUILDER_RULES §1.7 reserve the SIMULATED label for simulated data.
- L07 Misconception 2: "a change of 25 per cent from a change of one percentage point in the spread". The values are
  2500 at a spread of 0.04 and 2000 at 0.05, so the move from 2000 to 2500 is +25 per cent and the move from 2500 to
  2000 is −20 per cent. The sentence needs its direction and base stated.
- L08 Lab 1 code comment "Convention (project Q5)" is a planning reference inside the embedded lab code. It should
  read as the convention itself.
- L01 Lab 1 interpretation ends with a stray character ("... C The lab result is ...") where a grade mark appears to
  have been pasted into the prose.

## Builder E: REFERENCE_REQUESTS, DATA_REQUESTS, NOTATION_REQUESTS
None. The cards cite no registry key (the cards carry no `cite` field, and no M1 claim is empirical).

## Builder E: GLOSSARY_REQUESTS
None beyond Builders A to C.

## Builder E: CONTRACT_CHANGE_REQUESTS, DAG_DEFECTS
None.

## Builder E: KNOWN_LIMITATIONS
- `cards.json` holds 141 cards: L01 20, L02 21, L03 22, L04 13, L05 16, L06 11, L07 19, L08 19. Every definition,
  misconception and key-results row of L01 to L08 has at least one card. Some key-results rows with three values were
  split into one card per value.
- Grades follow the lesson's own key-results row where the row is a proof (T). Where a row rests on a lab output, the
  card grades it C with the lab named in `basis`, even when the lesson grades the row T (see the L06 row above).
- Numbers on the cards were checked by a script against the lesson text (every number on every card appears in its
  own lesson). The script ran on the text as it stood when the cards were written.
- The cards were not reviewed by an independent verifier. Verification is the verifier's task (VERIFIER_RULES).
