# M8 build plan: Numerical Methods & Scientific Computing (2026-11-09)

Unit: **M8 · Numerical Methods & Scientific Computing** · tier U · 110 h · prerequisites M2, M3, CS1, FC2 ·
no Atlas milestone · no debate key · grading `autograder` (no rubric) · output directory `course/modules/M/M8/` (part code `M`) ·
lab twins `tests/labs/M8/` · project solution and grader `course/modules/M/M8/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to F, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.
Structure: the section list 0 to 13 is copied from `plans/E5-build-plan.md` (its section headings, in order), adapted to M8.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Statements about the
registry and the notation cite `file:line` in `references/references.json` and `notation/notation.json`. Statements about
tooling were checked by reading the tool source, or by running `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`,
`built_units`, `units`) through `.venv/bin/python`. Anything not in these sources is marked **NOT IN CURRICULUM** or **not
established**.

**Status: BLOCKING ISSUES EXIST (§0.3, items B1 to B4). The hours are feasible and the registry covers the two curriculum
sources. The project's scope (a million-input stress inside a browser-graded suite, and a failure-region report under an
autograder-only grading mode) and its accuracy contract need an architect decision before the builders start.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part M, code `M`, title "Mathematics"; M8 is in part M | `curriculum/01-foundations.yaml:70-72` (part header), M8 entry at `:329` |
| M8 id and title "Numerical Methods & Scientific Computing" | `curriculum/01-foundations.yaml:329-330`; `curriculum/curriculum.json` (`"id": "M8"`, line 6575) |
| Tier `U`, hours `110` | `curriculum/01-foundations.yaml:331-332` |
| Direct prerequisites `[M2, M3, CS1, FC2]` | `curriculum/01-foundations.yaml:333`; `curriculum.json` M8 entry (`prereqs`) |
| Core: "IEEE 754, conditioning and stability, root finding, linear solvers, interpolation, quadrature, finite differences, random-number generation, Monte Carlo and variance reduction." | `curriculum/01-foundations.yaml:334-337` |
| `introduces` has **15 concepts** (mapped to lessons in §1) | `curriculum/01-foundations.yaml:338-353`; coursekit `concept_owner()` gives 15 entries with module M8 |
| Sources: two strings, Goldberg (1991) ACM Computing Surveys 23(1) and Glasserman (2003) | `curriculum/01-foundations.yaml:354-356` |
| Lab: "Catastrophic cancellation; antithetic and control-variate efficiency." | `curriculum/01-foundations.yaml:357` |
| Project "Robust implied-volatility solver"; brief: "Build an implied-vol solver that never fails on valid inputs (deep ITM/OTM, near expiry), using bracketing with Newton acceleration. Stress it on a generated grid of a million inputs."; deliverable "Tested solver plus a failure-region report."; grading `autograder` | title `:359`; brief `:360-363`; deliverable `:364`; grading `:365` |
| No `debate:` key on M8 | `curriculum/01-foundations.yaml:329-365` (absent) |
| No `atlas:` key on the M8 project; no Atlas entry names M8 (the 20 entries name CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/01-foundations.yaml:358-365`; `curriculum/curriculum.json` `atlas` array (computed: `M8 in atlas` is False) |
| Course map: M8 is in the Core course "Computational Finance" with SC4 and DV4 | `curriculum/meta.yaml:104` |
| Downstream units that require M8: CS6 `[CS5, M8]`, AP1 `[M6, AP2, FC1, FC2, M8, E4]`, SC4 `[SC2, M8]`, DV4 `[DV1, M8, SC4, CS5]` | prereq lines `curriculum/01-foundations.yaml:545`, `curriculum/03-markets.yaml:268`, `:592`, `:774` (module ids at `:541`, `:264`, `:588`, `:770`) |
| Studios that require M8: STUDIO-M `[M7, M8]` and STUDIO-SC `[SC2, M8]` | `curriculum/01-foundations.yaml:76`; `curriculum/03-markets.yaml:495` |
| Prerequisite closure of M8 (computed): **{AC1, CF1, CS1, E1, FC1, FC2, M1, M2, M3, M4, P0.1}**; the closure introduces **140 concepts** | coursekit `prerequisite_closure("M8")` and the sum of closure `introduces`, run by the planner |
| Built units that M8 may link (hub pages exist): M2, M3, FC2 (and M1, M4, FC1, AC1, CF1, E1 among the closure) | `course/modules/M/M2/index.html`, `course/modules/M/M3/index.html`, `course/modules/FC/FC2/index.html`; coursekit `built_units()` |
| **CS1 is not built** (no `course/modules/CS/CS1/`; `course/modules/CS/` holds CS2 only) | `ls course/modules/CS/`; coursekit `built_units()` omits CS1 |
| Topological position: CS1 3, M2 5, M3 6, FC2 30, M8 38 | `curriculum/curriculum.json` `topological_order` (computed) |
| **Nearest built prerequisite (by topological order): FC2.** Its plan is the structure precedent for the autograder design | `plans/FC2-build-plan.md` (read in full sections 0, 4, 5, 14) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 110 h (`curriculum/01-foundations.yaml:332`). Tool rules (read in tool source):

- lesson `data-hours` 6 to 12 (`tools/check_pages.py:228`, message "a lesson is 6–12 study hours");
- hub `data-hours-lessons + data-hours-project = 110` (`tools/check_pages.py:337-338`);
- project share 10 to 40 % of 110, i.e. 11 to 44 h (`tools/check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split: **8 lessons × 10 h = 80 h; project 30 h (27.3 %)**. 80 + 30 = 110. Feasible. **No STOP condition on hours.**
Hours are design targets; the architect ruling forbids changing them because a verifier's estimate differs
(`/Users/billyribeiro/.fanout/fixer-rules.md:16`, the HOURS bullet).

### 0.3 Blocking issues (architect decision required before builders start)

**B1. The project's million-input stress cannot run inside the browser-graded suite.**
- The brief asks for "a generated grid of a million inputs" (`curriculum/01-foundations.yaml:362-363`).
- The grader runs in Pyodide: each test must finish in under 5 s and the whole suite in under 60 s (`BUILDER_RULES.md` §5.3 item 4, "Dual-mode"). `tools/run_graders.py:40` sets `SUITE_LIMIT_S = 60.0`.
- A million inversions, each with tens of pricing calls, is far beyond that budget in Pyodide. The planner did not time it; the
  estimate is a planner judgement (not established by a run).
- **Recommended decision (Q1):** the graded suite uses a seeded grid of **N = 2 000 inputs per seed**, timed under the limit. The
  million-input run becomes **rung 4 (stretch, ungraded, local only)** with a timing report. The brief's wording stays in the
  curriculum; the page states the graded size and why.

**B2. The deliverable "failure-region report" is not covered by the grading mode.**
- Deliverable: "Tested solver plus a failure-region report." (`curriculum/01-foundations.yaml:364`). Grading: `autograder` only (`:365`).
- `tools/check_projects.py` `GRADING_WORDS` (line 38) and `grading_problems` (lines 41-50) accept an autograder entry; a free-text
  report has no check, and the rubric machinery is not applicable to an autograder-only project (`check_projects.py` calls
  `rubric_problems` (line 58) only for `rubric | both`, lines 138-139).
- **Recommended decision (Q2):** the report is a **machine-checked structure** returned by the solver module (`region()` per input
  and a count dictionary over the seeded grid, §5.2), so the suite tests it. Any prose note is either (a) not graded and labelled as
  ungraded on the page, or (b) the architect amends `yaml:365` to `both` (a curriculum change; builders do not edit `curriculum/*.yaml`).

**B3. The accuracy contract cannot be one absolute tolerance on the volatility.**
- Where vega is tiny (deep OTM or near expiry), a price rounded to double precision fixes the implied volatility only to a
  width that grows as vega shrinks. This is the conditioning idea of M8's own lesson 2 (`condition-number`), and the grader
  must not demand more than the conditioning allows.
- **Recommended decision (Q3):** a two-part contract stated on the page: (i) a **residual** bound, `|C(σ̂) − price| ≤ 1e-12 · S`,
  on every valid input; (ii) a **forward** bound, `|σ̂ − σ*| ≤ 1e-8`, only where `vega(σ*) ≥ 0.01` (price units per unit volatility).
  The builders measure the constants on the reference over seeds 0 to 49 and fix them before the tests are written. Until
  then the constants are placeholders for the architect's decision, not facts.

**B4. "Bracketing with Newton acceleration" is a method requirement, and a property-only grader cannot see the method.**
- The brief names the method (`curriculum/01-foundations.yaml:361`). A pure bisection solver satisfies every property test that
  is stated on accuracy alone, so the alternatives (§5.5) are valid only if the page makes the method observable.
- **Recommended decision (Q4):** the spec names the method; the suite adds an **evaluation budget**, a count of pricing calls per
  inversion that the solver reports through `last_evaluations()` (§5.2). The budget is fixed only after the reference's
  counts are measured. A budget that bisection cannot meet is not chosen blindly: the architect sets it from the measurement.

Non-blocking, but the architect should see them:

- **N1. The core text names "linear solvers" and "finite differences" (`curriculum/01-foundations.yaml:334-337`), but `introduces`
  has only `cholesky-decomposition` as a linear-algebra concept (`:345`).** Resolution in this plan (Q10): finite differences are
  taught with M2's `finite-difference-derivative` (in the closure, `curriculum/01-foundations.yaml` M2 `introduces`), and
  linear solvers are the LU and Cholesky concept (`:345`). No new concept is needed.
- **N2. FC2 already teaches bisection implied-volatility inversion.** `course/modules/FC/FC2/L08.html:110-121` (Definition 3.1
  and Lab 1: bracket `[10^{-6}, 10]`, tolerance `10^{-10}`, a named error when the bracket does not contain the root) and
  `:121` states that the fixed upper end fails for a price above `C(10)`. M8 must not re-teach that lab. It extends it.
- **N3. CS1 is not built.** Its concepts are in the closure (§4), so their ids may be linked through `concepts.html`, but no
  link to a CS1 hub page is possible (§11 item 4).
- **N4. The IEEE 754 standard itself is not a registry record**, and `ieee.org` is not on the allow-list in
  `references/authorities.yaml` (the issuer list at lines 9-31 has no IEEE entry; `docs.python.org` at line 31 is allow-listed).
  See Q13.
- **N5. Registry coverage is thin for M8.** Only two keys carry `used_by: ["M8"]`: `goldberg1991every` (`references/references.json:10493`)
  and `glasserman2003monte` (`:10373`). Every numerical-analysis source that the lessons would need beyond these two is a
  REFERENCE_REQUEST (§7.2), so those statements are taught by derivation (grade T) or left ungraded.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

8 lessons × 10 h = 80 h; project 30 h; total 110 h. The 15 concepts are split 2+2+2+1+2+2+2+2 = 15, each in exactly one row
(`curriculum/01-foundations.yaml:338-353`). Concepts are listed by id; names are in the yaml.

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/M8/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Floating-point arithmetic and cancellation | `ieee-754-floating-point` (`:339`), `catastrophic-cancellation` (`:342`) | `lab-M8-L01-1` (**the curriculum lab, part A**, `:357`): cancellation in `(1+h)-1`, in a quadratic-root formula and in a variance formula on seeded data with a large offset (SIMULATED data) | 10 | Builder A |
| L02 | Conditioning and stability | `condition-number` (`:340`), `numerical-stability` (`:341`) | `lab-M8-L02-1`: a 2×2 system solved exactly in `Fraction`; the exact `κ∞` and the observed relative change of the solution under a perturbed right-hand side | 10 | Builder A |
| L03 | Bracketing root finders and Newton's method | `bracketing-root-finder` (`:343`), `newtons-method` (`:344`) | `lab-M8-L03-1`: bisection step count against `⌈log₂(W/tol)⌉`; Newton's error sequence on `x²−2`; the FC2 bisection is the baseline and is not re-run | 10 | Builder B |
| L04 | Linear solvers and finite differences | `cholesky-decomposition` (`:345`) (LU and Cholesky) | `lab-M8-L04-1`: Cholesky of a 3×3 SPD matrix in `Fraction` against float; the forward-difference error against the step `h` (truncation against round-off) | 10 | Builder B |
| L05 | Interpolation and quadrature | `cubic-spline-interpolation` (`:346`), `numerical-quadrature` (`:347`) | `lab-M8-L05-1`: natural cubic spline error on a smooth function; trapezoid and Simpson errors against `n` | 10 | Builder C |
| L06 | Pseudo-random numbers and Monte Carlo integration | `pseudo-random-number-generator` (`:348`), `monte-carlo-integration` (`:349`) | `lab-M8-L06-1`: seeded determinism; the Monte Carlo estimate of `∫₀¹ eˣ dx` with its standard error; `error × √n` against `n` (SIMULATED) | 10 | Builder C |
| L07 | Variance reduction: antithetic and control variates | `antithetic-variates` (`:350`), `control-variates` (`:351`) | `lab-M8-L07-1` (**the curriculum lab, part B**, `:357`): variance ratios for a European call under a lognormal terminal law, against the closed form (SIMULATED) | 10 | Builder D |
| L08 | Importance sampling and robust implied-volatility inversion | `importance-sampling` (`:352`), `robust-implied-vol-inversion` (`:353`) | `lab-M8-L08-1`: importance sampling of a Gaussian tail probability against its closed form (SIMULATED); `lab-M8-L08-2`: the fixed bracket `[10⁻⁶, 10]` against an expanding bracket, on prices that the fixed bracket rejects | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 80/30 | none | none | - | Builder A |
| project | Robust implied-volatility solver (`autograder`, §5) | none | `lab-M8-project-1` (rung 1), `lab-M8-project-2` (rung 2, `class="lab completion"`), `lab-M8-project-3` (rung 3 check: the reference on the seeded grid, printing the region counts) | 30 | Builder E |
| cards | `cards.json` from L01 to L08 | none | none | - | Builder F (after A to E) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01 and L02 exist.
Builder E writes `project.html`, the grader folder (`instance.py`, `pricing.py`, `starter.py`, `test_project.py`,
`reference.py`) and the three project labs, and does not depend on the lessons' prose.

**Builder split (Q8).** Eight lessons over four lesson builders gives two lessons each, not "about three". Five builders A to E
are fixed by the orchestration (the last builder owns the project). A 3-3-2 split would need an extra lesson builder and is
not proposed.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses only E1 and M1 concepts (`exponential-and-logarithm`, M1, for the `log` in the variance lab), and CS1 (`python`
  floats) in prose.
- L02 uses M3 `linear-map` (`concepts.html#linear-map`) and M2 `derivative`. It uses L01 `catastrophic-cancellation` by link.
- L03 uses M2 `derivative`, `taylor-theorem` (`concepts.html#taylor-theorem`), M1 `mathematical-induction` for the interval
  invariant, and L02 `numerical-stability` in prose (`Lnn.html#def-numerical-stability`).
- L04 uses M3 `positive-semidefinite-matrix` and `eigendecomposition`, M2 `finite-difference-derivative` and `taylor-theorem`,
  and L01 for the round-off model.
- L05 uses M2 `definite-integral` and `taylor-theorem`, and L04 `cholesky-decomposition` for the tridiagonal spline system
  (in prose: a tridiagonal LU is the same elimination).
- L06 uses M4 `random-variable`, `expectation`, `variance`, `law-of-large-numbers`, `central-limit-theorem`, and L01 for the
  floating-point sum error in the estimator.
- L07 uses M4 `correlation`, `expectation`, `normal-distribution`, `variance`, FC2 `black-scholes-formula` and `put-call-parity`
  (not needed here), and L06 `monte-carlo-integration` (`Lnn.html#def-monte-carlo-integration`).
- L08 uses M4 `normal-distribution`, `infinite-variance-clt-failure`, L07 `control-variates` in prose only, FC2
  `implied-volatility` and `option-arbitrage-bounds` (link to `concepts.html`), and L02 `condition-number` for the vega threshold.

Hours check: 8 × 10 = 80 (hub `data-hours-lessons="80"`); project 30 (hub `data-hours-project="30"`); 110 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to M8)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `plans/FC2-build-plan.md` (the nearest built
prerequisite; its Architect decisions section is binding precedent), `plans/E5-build-plan.md` (structure template), and this
file. Study `course/modules/FC/FC2/` for the autograder layout (grader folder, panel attributes, project page) and
`course/modules/M/M7/` for the hub grammar. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) where the
   value is exact, and from `float` only where the lesson is about floating point. A rounded display states its rounding rule.
   Precedent: AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2, FC2 §5.7.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what
   the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS ("checked directly" with no lab behind it).
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited, and only at book or paper level unless the builder has
   read the abstract (VERIFIER §2.1). Every locator must be read. The Goldberg and Glasserman records give the DOI and the
   publisher; the builder reads the abstract at the DOI before attributing any claim. No page, table, equation or date is typed
   from memory. A paper known only by its title is named in an ungraded sentence (precedent: E3 L05 to L08, ruling 39).
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "robust", "stable", "optimal", "never fails" are
   used only where a derivation, a finite check or a lab computes the claim. The page's scope is stated once in L01:
   IEEE 754 binary64 (Python `float`), exact arithmetic with `fractions`, the one-dimensional root finders and the two-dimensional
   linear systems; the Monte Carlo of a European payoff; no PDE solvers, no sparse or iterative linear solvers, no quasi-random
   sequences (none is in the curriculum's `introduces`).
5. **Define before use.** Each of the 15 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson,
   and never before it. Terms outside the 15 (ulp, machine epsilon, backward and forward error, residual, vega, moneyness,
   time to expiry, standard error, log-normal law, unit roundoff) are defined in prose at first use with a plain `<dfn>` and no
   `data-concept` (`tools/check_dag.py:45-47` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions (A1, A2,
   ...) before the statement. Examples the builders must state: bisection needs a sign change on the bracket; Newton's quadratic
   convergence needs a simple root, a `C²` function and a start close enough to the root; the Cholesky factorisation needs a
   symmetric positive-definite matrix; the trapezoid error bound needs `f` twice differentiable on the panel; the control-variate
   coefficient needs `Var(Y) > 0`; the importance-sampling estimator needs the proposal to dominate the integrand's support.
7. **Grader rule (autograder).** The rule is active (§5). Enumerate every condition, boundary and error type the page states,
   and give each its own isolated test in both directions of each inequality (`/Users/billyribeiro/.fanout/fixer-rules.md`,
   PROJECT GRADERS bullet, line 19, read in full).
8. **Money.** M8 has no money output. Price inputs in the grader are `float` in currency units, and the page says so.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their container.
   `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network (`tools/run_labs.py:55`, per the
    FC2 precedent in `plans/FC2-build-plan.md` §5.7). The M1 twin `tests/labs/M1/lab-M1-L04-1.py` is the model.
11. **Errors and messages.** The grader's failure messages name the violated property and hint at the concept. They never print
    the expected value: the failing helper sets `__tracebackhide__ = True` (`fixer-rules.md` line 19). The exception types the page names are
    `ValueError` only (§5.2, Q6).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. The registry holds no
  record that this plan checked for a numerical-analysis claim beyond the two keys in §7. Claims about algorithms are derivations
  (grade T, conditional on the stated assumptions) or are ungraded naming sentences (§7.2 REFERENCE_REQUESTS).
- Concepts: §1 table; `<dfn>` only for the 15 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">` for a
  concept outside the prerequisite closure {AC1, CF1, CS1, E1, FC1, FC2, M1, M2, M3, M4, P0.1} (§4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts (from `course/modules/M/M8/`, the path to
  `course/concepts.html` is `../../../concepts.html`); `href="Lnn.html#def-<id>"` for earlier M8 lessons. A lesson never links a
  concept defined in a later lesson. No link to a CS1 hub (not built, N3). Links to the built hubs M2, M3 and FC2 are allowed.
- Labs: code lives once in `tests/labs/M8/lab-M8-Lnn-1.py` (and `lab-M8-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-M8-<page>-<n>`
  (`check_pages.py` lab rule). Standard library only (`fractions`, `math`, `random.Random(seed)`, `dataclasses`, `statistics`
  is not used). Seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab or figure that uses generated data (L01's offset data, L06, L07, L08-1 and the project's
  instances). Exact labs (L02, L03, L04's Fraction part, L05's closed-form checks, L08-2's bracket arithmetic) are not labelled
  SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments (precedent: M1 "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py` lines 58 to 72, `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted",
  "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree",
  "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent and relative changes state the base and the direction. Growth rates and errors state the convention (absolute,
  relative, ulps).
- A finite enumeration (for example the bracket check over a grid) is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that M8 must not give a different meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered symbol | Registered meaning (locator) | M8 conflict and rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation/notation.json:112`, module S1) | **Conflict.** Maturity is written `\tau` (FC2 already does: `course/modules/FC/FC2/L08.html:110`, Definition 3.1, "to keep \(\tau\) for maturity"). `T` is never used for maturity, time or a sample size. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`:117`, module M4) | **Used with that meaning.** The Black–Scholes `N(d)` is written `\Phi(d)`, not `N(d)`. |
| `\se` (macro) | standard error (`:101`) | **Used with that meaning** for the Monte Carlo standard error. |
| `\E`, `\Var`, `\Cov`, `\Corr` (macros) | expectation, variance, covariance, correlation (`:5` and following) | Used with those meanings. |
| `\R` (macro) | real numbers (`:25`) | Standard. |
| `\Normal`, `\iid`, `\indic` (macros) | normal law, iid, indicator | Used with those meanings where needed. |
| `\gamma_3`, `\gamma_4`, `\emgamma` | skewness, kurtosis, Euler constant (M4 and program) | Not used. |
| `R_f`, `R^\ast`, `R^{e\ast}`, `\mathbb{Q}` | AP1 symbols | Not used. An equivalent measure, if mentioned, is written in prose. |

Local symbols (allowed; `notation/notation.json` `about`: letters conventionally local are defined per lesson, and it names
`sigma` among them): `\sigma` volatility (the standard deviation of the log return per unit time; consistent with M4's registered
`\gamma_3` definition, which also uses `\sigma` for a standard deviation); `\tau` time to expiry in years; `S` spot; `K` strike;
`r` continuously compounded rate; `\kappa(A)` condition number; `u` unit roundoff (`2^{-53}` for binary64, stated as derived
on L01); `h` step size; `d_1`, `d_2` Black–Scholes arguments; `\mu` mean; `\varepsilon` machine epsilon. Each is defined on the
lesson where it first appears and never redefined.

NOTATION_REQUESTS: none. The plan uses the registered `\Phi`, `\se`, `\E`, `\Var`, `\R`, and local symbols.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01 `ieee-754-floating-point`, `catastrophic-cancellation`.** The binary64 format: 53 significant bits, round to nearest,
  `u = 2^{-53}` (a derivation from the format, grade T, with the format's assumptions stated). The rounding model
  `fl(x op y) = (x op y)(1 + δ)`, `|δ| ≤ u`, as an assumption-level statement. Catastrophic cancellation: the relative error of
  `x − y` for nearly equal `x`, `y` (a derivation, grade T). Lab `lab-M8-L01-1` (part A of the curriculum lab): `(1+h)−1` for
  `h = 10^{-k}`; the quadratic root by the textbook formula and the stable formula; the variance by the one-pass formula against a
  two-pass formula on seeded data with a large offset (SIMULATED). Where the canon breaks: floats are not reals; addition is not
  associative (a checked example, not a claim about all data).
- **L02 `condition-number`, `numerical-stability`.** For a linear system, `κ(A) = ‖A‖‖A⁻¹‖` and the bound on the relative
  change of the solution (a derivation, grade T, with the perturbation assumption `‖δA‖ ‖A⁻¹‖ < 1`). Relative condition of a
  scalar function `|x f′(x)/f(x)|` (grade T). Backward stability as a definition. Lab `lab-M8-L02-1`: a 2×2 example with exact
  `κ∞` (`Fraction`) and the observed relative change against the bound. Where the canon breaks: `κ` is infinite for a singular
  matrix; a bound is not an observation.
- **L03 `bracketing-root-finder`, `newtons-method`.** Bisection with the interval invariant `f(a) f(b) ≤ 0`, proved by
  induction on the number of steps (grade T; M1 `mathematical-induction`). The step count `⌈log₂(W/tol)⌉` (T). A pointer to FC2
  L08 (`concepts.html#implied-volatility` and `FC2/L08.html`) for the implied-volatility use, with no re-run of FC2 Lab 1. Newton's
  method: the iteration, its quadratic error recursion under assumptions (simple root, `C²`, start near the root) as a Taylor
  derivation (grade T, M2 `taylor-theorem`). Brent's method is described, not proved; its convergence is an ungraded statement
  (no registry key, §7.2 R2). Lab `lab-M8-L03-1`: bisection step counts against the formula; Newton's error ratios on `x²−2`.
- **L04 `cholesky-decomposition`; finite differences.** LU with partial pivoting as Gaussian elimination in matrix form (T for the
  factorisation with the stated pivot rule). Cholesky `A = LLᵀ` for symmetric positive-definite `A` (T: existence and uniqueness
  under the stated assumption, M3 `positive-semidefinite-matrix`). The backward-stability theorem of these factorisations is **not
  stated** here (no registry key, §7.2 R4). The forward-difference error `|f(x+h)−f(x))/h − f′(x)| ≤ (h/2) M + u |f|/h` as a derivation
  with the bound's assumption on `f″` (grade T), and the optimal `h` as a consequence (grade T, conditional). M2
  `finite-difference-derivative` is linked. Lab `lab-M8-L04-1`: the Fraction Cholesky and the float Cholesky on the same 3×3 SPD matrix;
  the forward-difference error on `exp` at `x = 1` against `h`.
- **L05 `cubic-spline-interpolation`, `numerical-quadrature`.** Natural cubic spline: the tridiagonal system for the second
  derivatives, existence and uniqueness under the stated assumption (T). The `O(h⁴)` order for smooth functions is **not** derived
  here; it is a lab result graded C naming `lab-M8-L05-1` (ruling 13). Quadrature: the trapezoid rule for one panel with its
  error term from Taylor's theorem (T); the Simpson rule for one panel (T, with the stated hypothesis); the composite rules
  (T as sums of panel errors). Lab `lab-M8-L05-1`: the spline and the composite rules' errors against `n`, with `log₂` of the
  error ratios printed. Uses M2 `definite-integral`.
- **L06 `pseudo-random-number-generator`, `monte-carlo-integration`.** A pseudo-random generator as a deterministic map from a
  seed to a sequence; no statement about statistical quality is made unless a test is run and printed in the lab. Monte Carlo
  estimator `θ̂ₙ = (1/n) Σ f(Xᵢ)` for `Xᵢ` iid: unbiasedness (T), `\Var(θ̂ₙ) = \Var(f(X))/n` (T), the standard error `\se = s/√n`
  (T), the root-n error from the central limit theorem (M4 `central-limit-theorem`, conditional on `\Var(f(X)) < ∞`, T).
  Lab `lab-M8-L06-1`: seeded determinism (same seed, same output, checked in the lab); the estimate of `∫₀¹ eˣ dx` with its
  standard error; `error × √n` against `n` (SIMULATED).
- **L07 `antithetic-variates`, `control-variates`.** Antithetic pairs: `\Var((X+X′)/2) = (\Var X)(1+ρ)/2` for an identically
  distributed pair with correlation `ρ` (T). Control variates: the optimal coefficient `b* = \Cov(X,Y)/\Var(Y)` and the variance
  reduction factor `1 − \Corr(X,Y)²` (T, derived with the stated assumptions, M4 `correlation`). Application: a European call
  under a lognormal terminal law `S_τ = S e^{(r−σ²/2)τ + σ√τ Z}` (the model is stated in prose; `geometric-brownian-motion`
  is SC2 and is **not** linked, §4 D3). The exact value through FC2 `black-scholes-formula`
  (`concepts.html#black-scholes-formula`), computed with `math.erf` and printed to a stated number of decimals. Lab
  `lab-M8-L07-1` (part B of the curriculum lab): the variance ratios of the antithetic and control-variate estimators against plain
  Monte Carlo (SIMULATED).
- **L08 `importance-sampling`, `robust-implied-vol-inversion`.** Importance sampling: `\E[f(X)] = \E_q[f(Y) w(Y)]` with `w = p/q`
  under the stated support assumption (T); the variance of the weighted estimator (T); the warning that a weight with infinite
  variance breaks the central limit theorem (M4 `infinite-variance-clt-failure`, linked; the claim is the M4 result, not a new one).
  Robust inversion as a design: a price has an implied volatility iff it lies strictly between the no-arbitrage bounds
  (FC2 Theorem 2.3, linked through `concepts.html#implied-volatility`; M8 cites the result as FC2's, it does not re-prove it).
  Bracket expansion from a valid bracket, the safeguarded Newton step (accept the Newton step only if it stays in the bracket
  and at least halves its width, otherwise bisect) and the failure region defined by `vega < 0.01` (§5.2). Labs `lab-M8-L08-1`
  (importance sampling of `P(Z > 4)` against the closed form `½ erfc(4/√2)`; SIMULATED for the estimates) and
  `lab-M8-L08-2` (the fixed bracket `[10⁻⁶, 10]` against an expanding bracket, on prices above `C(10)` for a strike of 100; the
  lab recomputes its own values, it does not copy FC2's numbers).
- **Lesson-level constraints.** Each lesson's "Where the canon breaks" names at least one limit and what changes without it. No
  lesson uses a term from a later unit as a concept (for example `geometric-brownian-motion`, `option-greeks`, `volatility-smile`,
  §4). No lesson presents a numerical result as a theorem unless it is derived (grade T) or graded C with its lab named.

---

## 4. DAG problems (concepts that natural M8 content would use outside the closure)

Prerequisite closure of M8 (computed): **{AC1, CF1, CS1, E1, FC1, FC2, M1, M2, M3, M4, P0.1}**, with 140 usable concepts (the
closure's `introduces`). Owners below are from `curriculum/curriculum.json` `concepts` (coursekit `concept_owner`).

| Ref | Concept | Owner (outside closure) | Where natural M8 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `option-greeks` (`DV1`) | DV1 | vega in the Newton step and in the failure-region threshold (L03, L08, project) | Plain prose: "vega, the partial derivative of the Black–Scholes price with respect to σ", defined in place with M2 `partial-derivative` (in closure). No link, no `data-concept`. |
| D2 | `volatility-smile` (`DV2`) | DV2 | motivation of the robust inversion across strikes (L08) | Plain prose, no link. |
| D3 | `geometric-brownian-motion` (`SC2`), `brownian-motion` (`SC1`) | SC2, SC1 | the lognormal terminal law in L07 and the project's instances | Plain prose: "the lognormal terminal law implied by the normal log return", derived from M4 `normal-distribution` (in closure). No SDE is solved. **Not linked** (Q12). |
| D4 | `euler-maruyama-scheme`, `strong-vs-weak-convergence` (`SC2`) | SC2 | a path-discretisation example | Not used. The lognormal law is sampled exactly. |
| D5 | `estimator`, `estimator-bias-variance`, `bootstrap` (`S1`) | S1 | the words "estimator" and "unbiased" in L06 | Plain prose. Unbiasedness is derived for the sample mean, with M4 `expectation` (in closure). No link. |
| D6 | `contraction-mapping`, `banach-fixed-point-theorem`, `uniform-convergence` (`M5`) | M5 | a fixed-point view of Newton's method (L03) | Not used. Newton's quadratic error recursion is derived by Taylor's theorem (M2, in closure). |
| D7 | `lebesgue-integral`, `dominated-convergence-theorem` (`M6`) | M6 | measure-theoretic justification of Monte Carlo unbiasedness (L06) | Not used. Unbiasedness is a finite-sum computation with iid draws. |
| D8 | `bias-variance-tradeoff` (`QR3`), `ols-estimator` (`S2`) | QR3, S2 | none planned | Not used. |
| D9 | `black-76-model` (`FI6`), `bachelier-model` (`FI6`), `trinomial-tree` and `early-exercise-boundary` (`DV4`) | FI6, DV4 | none planned | Not used. |
| D10 | `lognormal`, `bisection`, `vega`, `unit-roundoff`, `ulp` | not concepts in `curriculum.json` (`concepts` has no entry) | L01 to L03, the project | Plain `<dfn>` with no `data-concept` (`tools/check_dag.py:45-47`). |
| D11 | `monte-carlo-npv` (`CF1`, in closure) | CF1 (in closure) | name overlap with `monte-carlo-integration` (M8) | Distinct ids. M8 text says "Monte Carlo integration" and does not link `monte-carlo-npv` (Q22). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q11).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1 to D9 passes the tool, so the
verifier reads every lesson for these names (VERIFIER §2.9).

**Missing prerequisite question.** None is required. The curriculum's `core` items "linear solvers" and "finite differences"
(`curriculum/01-foundations.yaml:334-337`) map to M8's `cholesky-decomposition` and to M2's `finite-difference-derivative`
(in closure). This is recorded as N1 in §0.3.

---

## 5. Project (`project.html`, Builder E): autograded, ladder, spec, grader, budget

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order, rung titles "worked example", "completion", "independent", "stretch")

1. **Rung 1, worked example** (`lab-M8-project-1`, SIMULATED): one fully solved, annotated inversion on one seeded instance
   (`make_instance(0)` from the support file, see §5.2): the no-arbitrage bounds check, the bracket expansion, the bisection step,
   the safeguarded Newton step, and the residual and forward error at the end. Each step has a "why" annotation.
2. **Rung 2, completion** (`lab-M8-project-2`, `class="lab completion"`, SIMULATED): the Newton-step line and the bracket-update
   line of the safeguard are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the
   twin's line or contains a blank (`tools/run_labs.py` docstring; ruling 11 of the architect rulings).
3. **Rung 3, independent project** (graded by the autograder): `solver.py`, the suite `test_project.py` and the region report (§5.2).
   `lab-M8-project-3` is the rung-3 check: it runs the reference on the seeded grid and prints the region counts the suite expects.
4. **Rung 4, stretch** (optional, ungraded, local): the million-input grid (the brief's own size) with a timing report on the
   student's machine, and a plot of the region map. Resolves B1 (Q1).

### 5.2 Spec (`dl.spec`; `check_projects.py` requires terms context, inputs, required outputs, constraints, grading)

- **Context.** A desk needs an implied volatility for every quoted European option in a chain, including deep in- and out-of-the-
  money strikes and quotes a few hours from expiry. The solver must never fail on a valid quote. Where it cannot be accurate,
  it must say so.
- **Inputs.** For a call or a put: `price` (currency units, `float`), `spot` `S` (`float`), `strike` `K` (`float`), `tau` `τ`
  in years (`float`), `rate` `r` (continuously compounded, `float`), `kind` (`"call"` or `"put"`). The pricing functions
  `bs_price`, `vega`, `bounds` are supplied in `pricing.py` (a support file, not graded, not the student's file; Q5). No real
  data: every instance is generated (SIMULATED), and the page says so.
- **Required outputs.**
  - `solver.py` exposing `implied_vol(price, spot, strike, tau, rate, kind) -> float` (the returned `σ̂`, a `float > 0`).
  - `solver.py` exposing `region(price, spot, strike, tau, rate, kind) -> str`, returning `"solved"` when the input is valid and
    `vega(σ̂) ≥ 0.01`, `"ill_conditioned"` when it is valid and `vega(σ̂) < 0.01`, and raising `ValueError` for an invalid input.
    The region of an input is a property of the input's conditioning, not of the solver's output (Q2).
  - `solver.py` exposing `last_evaluations() -> int`, the number of pricing calls of the last `implied_vol` call (Q4; the budget
    in §5.2 constraint 4 is set only after measurement).
  - Standard library only. No third-party package.
- **Constraints.**
  1. **Contract (exception table, ValueError only; Q6).** `ValueError` is raised for: `kind` not `"call"` or `"put"`; `spot`,
     `strike` or `tau` not finite or not positive; `price` not finite; `price` on or outside the strict no-arbitrage bounds
     (for a call, `max(S − K e^{−rτ}, 0) < price < S`; for a put, `max(K e^{−rτ} − S, 0) < price < K e^{−rτ}`; the bounds are
     derived on the lesson, FC2 Theorem 2.3 is the call case). Any other valid input returns a volatility. The page names these
     conditions in this order and no other error type is required.
  2. **Accuracy (Q3).** (i) Residual: `|C_kind(σ̂) − price| ≤ 1e-12 · S` for every valid input. (ii) Forward:
     `|σ̂ − σ*| ≤ 1e-8` where `σ*` is the generating volatility and `vega(σ*) ≥ 0.01`. The constants are the builders'
     measured values, fixed before the tests are written.
  3. **Valid volatility range.** Any `σ > 0` for which the price is strictly inside the bounds is valid. The generator uses
     `σ* ∈ [0.02, 5]`. A hand-built call (`S = 100`, `K = 100`, `τ = 1`, `r = 0.05`, price `99.99995`) has its only solution above
     `σ = 10` (`course/modules/FC/FC2/L08.html:121` states this for the same strike and price), so it checks that the upper bracket
     is not fixed (test T5 below).
  4. **Evaluation budget (Q4).** At most `B` pricing calls per inversion on the seeded grid, with `B` set after the reference's
     measured counts. The page states `B` and the measurement.
  5. **Determinism.** The same inputs give bit-identical outputs.
  6. **Failure-region report (Q2).** For the seeded grid of `N` inputs per seed (Q1: `N = 2000`), the count of each region label
     (`"solved"`, `"ill_conditioned"`) and of each rejected input (ValueError) is an exact integer count that the suite recomputes
     from the generating parameters, not from `region()` alone.
- **Grading.** Autograder (`autograder`): the grader panel `section.grader-panel` with `data-unit="M8"`, `data-grader="grader/"`,
  `data-suite="test_project.py"`, `data-support="instance.py pricing.py"`, `data-solution="solver.py"`,
  `data-starter="starter.py"`, `data-packages=""` (the FC2 attribute set, `course/modules/FC/FC2/project.html`). The spec's grading
  entry names the autograder. No rubric, no exemplars, no question bank (§12 Q6).
- **Reading list.** `ol.reading-list` cites `goldberg1991every` and `glasserman2003monte` (registry keys only, §7.1). Nothing else.

**Test list (Builder E; each test is one isolated check, in both directions where an inequality is stated; `fixer-rules.md` line 19).**

| Test | Property or condition (the page names it) | Direction tested |
|---|---|---|
| T1 `kind` | `kind` not in {call, put} raises ValueError | the two valid kinds pass; a third raises |
| T2 non-positive or non-finite | `S`, `K`, `τ` each ≤ 0 or NaN or infinite raise ValueError | each positive value passes |
| T3 bounds, call, both sides | `price == S`, `price == max(S−Ke^{−rτ},0)` and `price` just above the lower bound and just below `S` | the boundary equalities raise; the interior values solve |
| T4 bounds, put, both sides | the put analogue | the boundary equalities raise; interior solves |
| T5 upper bracket not fixed | hand-built call with price `99.99995` (§5.2 constraint 3; the test oracle finds `σ*` by its own bracket expansion and bisection, written apart from `reference.py`) | the solver returns `σ̂` with the residual bound; `σ̂ > 10` |
| T6 valid deep ITM and OTM | instances with `|ln(S/K)| ≥ 2` | residual and forward bounds hold |
| T7 near expiry | `τ = 1/365` and `τ = 1/52` instances | residual bound holds everywhere; forward bound only where vega passes |
| T8 put round trip | put instances on the seeded grid | the put is inverted without the call formula |
| T9 residual everywhere | every valid instance of the seeded grid | `|C(σ̂) − price| ≤ 1e-12 · S` |
| T10 forward bound | valid instances with `vega(σ*) ≥ 0.01` | `|σ̂ − σ*| ≤ 1e-8` |
| T11 region labels | `region()` labels agree with `vega(σ̂) ≥ 0.01` on the grid | both labels occur on seeds 0 to 49 (instances differ across seeds) |
| T12 region counts | the report counts equal the suite's recomputed counts | exact equality |
| T13 determinism | two calls with the same inputs return identical floats | equality of `float` bits |
| T14 evaluation budget | `last_evaluations() ≤ B` across the seeded grid | the budget is an upper bound; a bisection-only solver is not forced to fail unless `B` is below its count (Q4) |
| T15 no fabricated answer | the output on seeds 1 to 49 is not seed 0's value | answers differ across seeds (kills a stored-answer mutant) |
| T16 time | `N` inversions finish under 5 s in Pyodide and under the suite limit locally | the timing check is local-run only for the 60 s suite limit |
| T17 starter fails | the empty `starter.py` (NotImplementedError stubs) fails the suite | the suite fails |
| T18 instance validity | `make_instance(seed)` returns only valid inputs (strict bounds, positive `S`, `K`, `τ`) and is deterministic | every seed 0 to 49 |

Failure messages name the violated property (for example "the residual is above the 1e-12 relative bound") and hint at the
concept (for example "bracket expansion; see the no-arbitrage bounds"). They never print the expected value.

### 5.3 Time budget (`<table id="hours">`, sums to 30 h; every row needs a one-line rationale; `check_projects.py` lines 58 to 73)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved seeded instance, annotated line by line |
| Rung 2, completion problem | 2 | Fill the Newton-step and bracket-update lines, then run the instant check |
| Solver: bracket expansion, bisection, safeguarded Newton | 10 | The core algorithm, its step rule and its loop invariant |
| Input contract and no-arbitrage bounds | 3 | The ValueError conditions, the strict bounds for calls and puts, the put case |
| Accuracy and conditioning analysis | 4 | Residual and forward bounds, the vega threshold, the constants measured on seeds 0 to 49 |
| Failure-region report and counts | 4 | `region()`, the counts, the recomputed totals in the suite |
| Local stress run on the grid, and timing | 3 | `N = 2000` per seed on the local suite; the timing line for the page |
| Self-test against the suite and the starter | 2 | Run the suite on the solver and on the empty starter |
| **Total** | **30** | Equals `data-hours-project` on the hub |

### 5.4 Grader design (Builder E; the verifier writes mutants and alternatives, §5.5 and §5.6)

Files in `course/modules/M/M8/grader/`: `instance.py` (`make_instance(seed: int) -> dict[str, object]`, deterministic from
`random.Random(seed)`, SIMULATED, valid for every seed, `σ* ∈ [0.02, 5]`, a mix of deep ITM, deep OTM, near expiry and puts),
`pricing.py` (`bs_price`, `vega`, `bounds`, pure functions with `math.erf`), `reference.py` (the full solution; excluded from deployment,
BLUEPRINT §7; ruling 4 of the architect rulings: no deploy step yet, recorded for the owner), `starter.py` (`NotImplementedError`
stubs; the suite must fail on it, T17), `test_project.py` (the §5.2 tests, with oracles written apart from `reference.py`).
Every test recomputes its expected value from the instance's generating parameters, not from the solver.

### 5.5 Five alternative correct implementations (validity criteria; written by the verifier; each must pass seeds 0 to 49)

Each alternative keeps the bracket and uses Newton steps (the method named in the brief, B4). Each must pass every test in §5.2
on seeds 0 to 49 (ruling 10). Test-only fixtures under `ledgers/M8/alternatives/`; scripts under `ledgers/M8/scripts/` (VERIFIER §3).

1. **A1, safeguarded Newton with bisection fallback** in `σ` coordinates (the reference's family, written independently).
2. **A2, the same algorithm in `log σ` coordinates**, with the bracket mapped by `exp`.
3. **A3, Newton with a secant fallback** (instead of bisection) inside the bracket, with the same accept-and-halve rule.
4. **A4, a closed-form starting guess** (an at-the-money approximation, derived on the page, not cited), bracket expansion by doubling,
   then safeguarded Newton.
5. **A5, batch-vectorised** (a list comprehension over the grid, per-element brackets and masks, the same stop rule), with the scalar API
   wrapping it.

An implementation that fails any test is replaced by another correct one, so the five stay five (FC2 precedent, §5.5 of its plan).

### 5.6 Mutants (ten student errors; each a single-change copy of `reference.py`; each must be killed)

The verifier writes each mutant as a complete module under `ledgers/M8/mutants/`, the first docstring line naming the student error
(ruling 9; VERIFIER §2.6). Builder E does not write mutant files. Each mutant must fail at least one test in §5.2.

1. **M01, upper bracket fixed at 10 with no expansion** (copies FC2 L08 Lab 1's bracket). Killed by T5 (the hand-built price `99.99995`, whose solution exceeds 10).
2. **M02, Newton step taken even when it leaves the bracket.** Killed by T6 (deep OTM, where the step is huge).
3. **M03, division by vega with no guard**, raising `ZeroDivisionError` on a valid input whose vega underflows. Killed by T7 (near expiry, deep OTM).
4. **M04, stop test on the price only** (`|C(σ) − price| < 1e-6`), ignoring the forward bound. Killed by T10 (low-vega instances with `vega ≥ 0.01`).
5. **M05, bisection update reversed** (`hi = m` when `C(m) < price`). Killed by T9 or T10.
6. **M06, a put inverted with the call formula** (uses `bs_price(kind="call")` for puts). Killed by T8.
7. **M07, `τ` scaled by `365/360` inside the pricing call.** Killed by T9 (systematic residual bias on the grid).
8. **M08, out-of-bounds price returns `NaN` or `0.0` instead of raising ValueError**, and the boundary `price == S` accepted. Killed by T3 and T4.
9. **M09, put price from the call by parity and cancellation** (`P = C − S + K e^{−rτ}` computed in floating point, then inverted), losing digits for deep OTM puts. Killed by T8 with the residual bound (T9); the kill is measured, and if no test kills it the verifier reports the mutant as equivalent with a proof, not as a pass.
10. **M10, a stored answer for seed 0** (returns seed 0's `σ` when the price equals seed 0's price). Killed by T15.

Ten mutants is the stricter bar (VERIFIER §2.6 asks for three). A mutant that differs from the reference only where the page states
nothing is moved to `ledgers/M8/equivalent/` with a README proof (ruling 9), and never left in `mutants/`.

### 5.7 Lab numerics (Builders A to D, and E for the project labs)

- Every lab is standard library only (`fractions`, `math`, `random`), seeded where random (`random.Random(seed)`), no network,
  no warnings under `python -I -W error`, under 10 s in Pyodide.
- Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":` guard.
- Exact labs (L02, L03's step counts, L04's Fraction part, L08-2's bracket arithmetic) print exact values. Closed forms that use
  `math.erf` (L07, L08-1) print to a stated number of decimals, and the hypothesis says so. Numbers in prose come from unrounded
  values, and the rounding is stated at display.
- Labels: SIMULATED only where data is generated (L01's offset data, L06, L07, L08-1, the project instances and grid).

---

## 6. Real-data policy (no real data)

- **No embedded real data is needed or named.** The curriculum names no dataset for M8 (`curriculum/01-foundations.yaml:329-365`);
  the brief names a generated grid (`:362-363`). `tools/data_sources.yaml` has no M8 entry (the embedded snapshots are
  `fx_daily`, `fx_monthly`, `ust_daily`; `course/assets/data/market/MANIFEST.json`), and none of them is needed.
- Every lab and the project are **SIMULATED**, labelled on the page and in the lab docstring (BUILDER_RULES §1.7).
- No `data-files` attribute on any M8 lab. No MANIFEST entry is added by builders. No DATA_REQUESTS.
- The honest statement on the project page: "All instances are generated; no market quotes are used." (Wording to be confirmed
  under Q16; not yet decided.)

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in M8 |
|---|---|---|---|
| `goldberg1991every` | Goldberg, "What every computer scientist should know about floating-point arithmetic", DOI 10.1145/103162.103163, journal-article, ACM Computing Surveys, volume 23, issue 1, pages 5-48, year 1991 (`references/references.json:10493`); `used_by: ["M8"]`; source string `yaml:355` matches | verified | L01 at paper level; the builder reads the abstract at the DOI before attributing any claim; reading list |
| `glasserman2003monte` | Glasserman, "Monte Carlo Methods in Financial Engineering", Springer New York, DOI 10.1007/978-0-387-21617-1, book, year 2003 (`references/references.json:10373`); `used_by: ["M8"]`; source string `yaml:356` matches | verified | L06 and L07 at book level, with a read locator for any number; reading list |
| `black1973pricing` | Black and Scholes, "The Pricing of Options and Corporate Liabilities", Journal of Political Economy 81(3), DOI 10.1086/260062 (`references/references.json:2892`); `used_by: ["DV1", "FC2"]` | verified; not yet `used_by` M8 | Only if M8 cites the formula's origin; then at paper level with no locator (Q14). Default: not cited; the formula is FC2's (`concepts.html#black-scholes-formula`). |
| `hull2021options` | Hull, "Options, Futures, and Other Derivatives", book, year 2021 (`references/references.json:13118`); `used_by: ["FC2"]` | verified; not M8 | Not cited by default (Q14). |
| `boyle1977options` | "Options: A Monte Carlo approach", Journal of Financial Economics 4(3), DOI 10.1016/0304-405x(77)90005-8 (`references/references.json:3694`); `used_by: ["DV4"]` | verified; not M8 | Title-level only, in an ungraded sentence, if L06 or L07 names the Monte Carlo approach to option pricing (Q14). |
| `cox1979option` | "Option pricing: A simplified approach", Journal of Financial Economics 7(3), DOI 10.1016/0304-405x(79)90015-1 (`references/references.json:6136`); `used_by: ["FC2"]` | verified; not M8 | Not cited by default. |

Not to be used by M8: none in the registry is needed for a claim outside these rows.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

The registry has no record for the following topics. Each is needed only for a claim the lessons would otherwise leave ungraded.
No author, title, year or venue is typed here. The architect resolves each through `tools/add_reference.py` (DOI, ISBN, or an
allow-listed issuer page; `references/authorities.yaml`).

- **R1.** Floating-point error analysis beyond the paper in §7.1 (needed for an error-bound statement about a sum): needed_for L01;
  confidence "the need is certain; no record identified by this planner".
- **R2.** Bracketing root-finder methods (bisection and a Brent-type hybrid) with convergence statements: needed_for L03 (Brent is
  described only, ungraded); confidence "the need is certain; no record identified".
- **R3.** Newton's method, its convergence region and safeguarded (bracketed) variants: needed_for L03 and the alternatives' rationale;
  confidence "the need is certain; no record identified".
- **R4.** Backward stability of LU with partial pivoting and of Cholesky: needed_for L04 (the stability sentence is not stated without
  it); confidence "the need is certain; no record identified".
- **R5.** Error theory for cubic-spline interpolation and composite quadrature: needed_for L05 (the `O(h⁴)` claim stays a lab result
  graded C without it); confidence "the need is certain; no record identified".
- **R6.** Design and quality of pseudo-random generators: needed_for L06 (the generator's quality is not claimed without it);
  confidence "the need is certain; no record identified".
- **R7.** Implied-volatility inversion methods (starting guesses and rational approximations): needed_for the alternatives' rationale
  only (optional); confidence "optional; no record identified".
- **R8.** The IEEE 754 standard as a primary document. `ieee.org` is not an allow-listed issuer (`references/authorities.yaml`).
  needed_for L01 (a citation of the format); confidence "the need is optional; the architect decides whether an issuer is added (Q13)".
- **R9.** Python's floating-point documentation: `docs.python.org` is allow-listed (`references/authorities.yaml`, issuer `psf`).
  needed_for L01 (what Python `float` is); confidence "optional; admitted only through `add_reference.py`".

### 7.3 DATA_REQUESTS and NOTATION_REQUESTS

- DATA_REQUESTS: none (§6).
- NOTATION_REQUESTS: none (§2.3).

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for M8 (`curriculum/01-foundations.yaml:358-365`; no Atlas entry names M8, §0.1). No
`atlas/M8.contract.md` is needed, and no contract is drafted here. `check_projects.py` skips the contract check when the project
names no `atlas` key (`tools/check_projects.py:144-146`, as read at `check_projects.py` `check_unit`).

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/M/M8/cards.json`, ids `M8-c001` upward (ids need not be sequential, architect ruling 2), `lesson` in L01 to L08,
  one card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7). `check_pages.py`
  `check_cards` checks the id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab lab-M8-L03-1, Proposition 3.2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`. A card and the key-results row it mirrors carry the same grade and basis (ruling 13).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit M8            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M8
.venv/bin/python tools/check_projects.py --unit M8
.venv/bin/python tools/run_labs.py --unit M8               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/M/M8/L01.html        # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/M/M8/L02.html --refresh lab-M8-L02-1   # after editing a twin
.venv/bin/ruff check tests/labs/M8 course/modules/M/M8/grader && .venv/bin/ruff format --check tests/labs/M8 course/modules/M/M8/grader
.venv/bin/mypy --strict tests/labs/M8 course/modules/M/M8/grader   # repository configuration; strict
.venv/bin/python tools/run_graders.py --unit M8 --seeds 0-49    # reference on 50 seeds, starter must fail, timing check
```

Verifier only (fresh checkout, not run by builders):

```bash
.venv/bin/python tools/mutate_graders.py --unit M8 --seeds 0-9     # ten mutants and the standing set
.venv/bin/python tools/page_smoke.py --unit M8                     # timing-sensitive; run alone on a quiet machine
.venv/bin/python tools/verify_refs.py --unit M8                    # the unit ledger's run (VERIFIER §2.1)
```

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md.

Not run for M8: `tools/fetch_data.py --check` (no dataset added, §6).

Flag checks: `tools/check_pages.py`, `tools/check_dag.py` and `tools/check_projects.py` accept `--unit`; `tools/run_labs.py` accepts
`--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`; `tools/run_graders.py` and
`tools/mutate_graders.py` accept `--unit` and `--seeds` (read in the tool source).

Cost note (CLAUDE.md, targeted testing): the grader run is the expensive step (50 seeds of `N = 2000` inversions plus pytest per seed).
It runs once before a push, and once after each change to `reference.py` or `test_project.py`.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the M8 project (`curriculum/01-foundations.yaml:358-365`) and no Atlas entry names M8.
   `check_projects.py` skips the contract check (lines 144-146).
2. **No debate.** M8 has no `debate:` key, so `check_pages.py` does not require a debate brief (the check keyed on
   `u.entry.get("debate")`). The two-sided rule (BUILDER_RULES §2.5) applies to any contested claim; the plan names none for M8.
3. **Autograder grading.** Unlike E5, M8 needs `run_graders.py` and `mutate_graders.py`: `run_graders.py` skips only units whose
   grading is not `autograder` or `both` (`tools/run_graders.py` lines 138-139).
   `mutate_graders.py` needs at least three mutants in `ledgers/M8/mutants/` (`tools/mutate_graders.py:42-43`).
4. **CS1 is not built.** `course/modules/CS/` holds CS2 only. Prerequisite concept links go to `concepts.html` anchors only; the hub
   may not link a CS1 page. `check_dag.py` uses the curriculum closure and is not blocked by this.
5. **The Pyodide budget.** The suite limit is 60 s locally (`tools/run_graders.py:40`) and 5 s per test in the browser
   (BUILDER_RULES §5.3 item 4). B1 applies.
6. **Grader panel attributes.** `check_projects.py` requires `data-unit`, `data-grader`, `data-suite`, `data-solution` and
   `data-starter` on `section.grader-panel`, the support files named in `data-support` and `reference.py`, `instance.py` (the
   `make_instance(seed: int)` signature is checked as text, `check_projects.py` `check_unit`).
7. **Rung 2.** `check_projects.py` requires a completion lab (`section.completion`) or a quiz for a module. The plan uses a completion
   lab (`lab-M8-project-2`); the module-level check on lesson pages is not affected.
8. **One curriculum lab, eleven labs in total.** The curriculum names one lab (`yaml:357`), which the plan splits into
   `lab-M8-L01-1` (part A) and `lab-M8-L07-1` (part B) (Q9). Eleven labs in total (ten lesson labs plus three project labs; L08 has two).
   BUILDER_RULES §3.4 requires a numerical check per key formula, which these labs provide.
9. **The FC2 overlap.** FC2 L08 is a built prerequisite that teaches bisection for implied volatility (N2). M8 links to it and does not
   import FC2 grader code (`course/modules/FC/FC2/grader/` is FC2's; the reference there is not M8's).
10. **The "first-year sequence" group.** No action (not M8's concern).

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start; recommended decision given)

1. **B1, the million-input stress.** Recommended: the graded suite uses `N = 2000` inversions per seed under the 5 s and 60 s limits;
   the million-input run is rung 4 (ungraded, local, with a timing report). Decision needed.
2. **B2, the failure-region report.** Recommended: `region()` and the report counts are machine-checked by the suite (T11, T12); any
   prose note is labelled ungraded on the page. The alternative is to amend `curriculum/01-foundations.yaml:365` to `both` (a
   curriculum change). Decision needed.
3. **B3, the accuracy contract.** Recommended: the two-part contract in §5.2 (residual `1e-12 · S` everywhere; forward `1e-8`
   where `vega ≥ 0.01`). The constants are confirmed by measurement on seeds 0 to 49 before the tests are written. Decision needed.
4. **B4, method and evaluation budget.** Recommended: the spec names bracket plus Newton; the suite checks an evaluation budget
   `B` that the architect sets from the reference's measured counts (T14). Decision needed before the alternatives are written.
5. **Pricing support file.** Recommended: `pricing.py` (`bs_price`, `vega`, `bounds`) is a support file supplied to the student, so the
   project tests the solver and not the formula (the formula is FC2's). Decision needed.
6. **Adversarial and error types.** Recommended: not adversarial (no question bank); `ValueError` only, for the conditions in §5.2
   constraint 1 (FC2 precedent: `course/modules/FC/FC2/grader/reference.py` raises `ValueError` at its named checks, lines 26, 33, 40, 43, 50, 57).
   Decision needed.
7. **Hours.** Recommended: 8 lessons × 10 h and a 30 h project (27.3 %). Alternatives within the rules: 9 × 9 h and a 29 h project; 7 × 10 h
   and a 40 h project (36 %). Decision needed.
8. **Builder split.** Recommended: A (L01, L02, hub), B (L03, L04), C (L05, L06), D (L07, L08), E (project and grader), F (cards).
   Eight lessons over four lesson builders gives two each, not "about three" (§1). Decision needed.
9. **The curriculum lab across two lessons.** Recommended: `lab-M8-L01-1` carries "catastrophic cancellation" and `lab-M8-L07-1` carries
   "antithetic and control-variate efficiency" (both named in `yaml:357`). Confirm.
10. **Core items with no concept.** Recommended: no new concept. Finite differences use M2 `finite-difference-derivative` (closure);
    linear solvers use the `cholesky-decomposition` concept, which covers LU (its name, `yaml:345`). Confirm, with no curriculum change.
11. **The outside-closure list in §4 (D1 to D11).** Recommended: each row as resolved (plain prose or not used; no link; no prerequisite
    change). Confirm.
12. **Geometric Brownian motion (D3).** Recommended: plain prose, the lognormal law derived from M4; no SC2 prerequisite. Confirm.
13. **Primary sources (R8, R9).** Recommended: cite `goldberg1991every` only for floating point; no IEEE standard citation unless the
    architect adds an issuer to `references/authorities.yaml`; Python's `docs.python.org` documentation may be admitted through
    `add_reference.py` if the builder needs it. Decision needed.
14. **`used_by` for keys M8 might cite.** Recommended: M8 cites only `goldberg1991every` and `glasserman2003monte` (both already list
    M8). `black1973pricing`, `hull2021options`, `boyle1977options` are cited only if the architect updates `used_by` through
    `add_reference.py`. Confirm.
15. **Notation.** Recommended: `\tau` for maturity (never `T`), `\Phi` for the normal CDF, `\se` for the Monte Carlo standard error,
    `\sigma` for volatility, no NOTATION_REQUESTS. Confirm.
16. **No real data.** Recommended: none; every lab and the project SIMULATED; the project page states that no market quotes are used. Confirm.
17. **No Atlas, no debate.** Recommended: confirm both (§8, §11).
18. **Ledger locations.** Recommended: the verifier writes `ledgers/M8/mutants/` (ten, §5.6), `ledgers/M8/alternatives/` (five, §5.5),
    `ledgers/M8/scripts/` and `ledgers/M8.verification.json`; builders write none of these.
19. **Reference deployment.** Recommended: record only (architect ruling 4: the repository has no deploy step yet). Confirm.
20. **CS1 not built.** Recommended: no link to a CS1 page; CS1 concepts linked through `concepts.html` only where used. Confirm.
21. **Name overlap with CF1.** Recommended: no link to CF1's `monte-carlo-npv` (D11). Confirm.
22. **FC2 overlap.** Recommended: M8 links to FC2 L08 through `concepts.html#implied-volatility` and recomputes its own lab values; it does not
    re-run FC2 Lab 1 (N2). Confirm.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L02 (includes curriculum lab part A), L03 to L04, L05 to L06,
   L07 to L08 (includes curriculum lab part B), project (grader: `run_graders.py --seeds 0-49`, ten mutants, five alternatives,
   the budget and the constants), cards. Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/M8.verification.json`; verifier scripts archived under `ledgers/M8/scripts/` (VERIFIER §3); mutants under
   `ledgers/M8/mutants/`; alternatives under `ledgers/M8/alternatives/`; equivalents, if any, under `ledgers/M8/equivalent/` with a README.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 to B4 must be resolved
   or named as honest gaps first.

Architect decisions: pending (§12). This plan is the planner's proposal. No decision in this file has been taken on the
architect's behalf.

---

## Output contract (planner)

- Path: `plans/M8-build-plan.md`.
- Lesson count: **8** lessons × 10 h = 80 h; project 30 h; total 110 h (curriculum 110 h, `curriculum/01-foundations.yaml:332`).
- Blocking questions: **B1** (million-input stress vs the browser budget), **B2** (failure-region report vs autograder-only grading),
  **B3** (accuracy contract vs conditioning), **B4** (method requirement vs a property-only grader). Each has a recommended decision in §12.
- Not established by the planner: the run time of the million-input stress and of the reference on `N = 2000` (no run was made);
  the accuracy constants (§5.2 constraint 2) and the evaluation budget (constraint 4), which depend on measurement; the bibliographic
  content of any source beyond the two registry records in §7.1 (no record was read beyond its registry fields); whether IEEE 754 can
  be admitted as a primary source (not on the allow-list).
