# M2 build plan: Single & Multivariable Calculus (planner output, 2026-10-28)

Unit: **M2 · Single & Multivariable Calculus** · tier F · **300 h** · prerequisites M1 · no Atlas milestone · grading
`both` (autograder + rubric) · output directory `course/modules/M/M2/` (part code `M`). Phase 2 fan-out (BLUEPRINT §9).
Executors: Claude Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never
writes a ledger. No git commit, no push.

Status: planner's proposal. Section 9 lists open questions that need an architect decision before builders start. No
lesson content is written here.

## 0. Curriculum facts (file and line read; anything not listed is absent from the curriculum)

| Fact | Locator |
|---|---|
| M2 block: id, tier F, hours 300, prereqs [M1] | `curriculum/01-foundations.yaml:122-126` |
| M2 core text (limits, derivatives, Taylor, integration, partials, gradients, Jacobians, Hessians, multiple integrals, implicit-function and envelope theorems) | `curriculum/01-foundations.yaml:127-130` |
| M2 introduces 13 concepts, one per line | `curriculum/01-foundations.yaml:132-144` (limit 132 ... automatic-differentiation 144) |
| M2 sources: Spivak, *Calculus*, 4th ed. (2008); Hubbard & Hubbard, 5th ed. (2015) (free text) | `curriculum/01-foundations.yaml:145-147` |
| M2 lab: "Taylor expansion of a bond price: duration and convexity preview." | `curriculum/01-foundations.yaml:148` |
| M2 project "Sensitivity engine", deliverable "Tested module plus an error-analysis note.", grading `both` | `curriculum/01-foundations.yaml:150-156` |
| M2 has no `debate` key, so no debate brief is required | `curriculum/01-foundations.yaml:122-156` (absent) |
| No Atlas milestone names M2 (the 20 atlas entries name other modules) | `curriculum/meta.yaml` atlas block (lines 194-276); `grep` for `M2` hits only `meta.yaml:66` (credential group "Calculus", modules [M1, M2]) and PM2 at `meta.yaml:180` |
| JSON row mirrors the YAML (id, hours 300, prereqs [M1], 13 introduces, sources, lab, project grading both) | `curriculum/curriculum.json` `parts` module with `"id": "M2"` at line 6350 |
| M1 (prerequisite) block: prereqs [P0.1]; 14 introduces | `curriculum/01-foundations.yaml:87-111` (prereqs at 91) |
| P0.1 has empty prereqs | `curriculum/curriculum.json` parts, module P0.1: `prereqs: []` (read by script in session); YAML `curriculum/01-foundations.yaml:6` |
| Registry keys with `used_by` containing M2: `spivak2008calculus` (year 2008, Open Library, status verified) and `hubbard2015vector` (year 2015, Open Library, status verified) | `references/references.json` entries of those keys; each `source_strings` equals the curriculum's string |
| `velleman2019prove` (verified, used_by ["M1"]) is not an M2 source | `references/references.json` (same record as M1 plan cites) |
| Vendored runtime packages include numpy, scipy, pytest | `tools/vendor_spec.yaml:59` (`packages: [numpy, scipy, pytest]`) |

Prerequisite closure of M2 (computed from the curriculum): M1 and P0.1 only. Concepts usable without definition are the
14 M1 concepts (`curriculum/01-foundations.yaml:96-110`) and the P0.1 concepts. Every other concept is outside the closure.

## 1. Hours arithmetic (checked against the tools' rules)

Rules read: a lesson declares 6-12 study hours (`tools/check_pages.py` line 228); the hub's
`data-hours-lessons + data-hours-project` must equal 300 and the project must be 10-40 % of module hours (`check_pages.py`
lines 337-340); the project's time-budget rows must sum to its `data-hours-project` (`tools/check_projects.py` lines 103-118).

- The 6-12 h lesson rule plus a 300 h total forces the lesson count N into the range 20 ≤ N ≤ 40 when the project takes
  60 h (240 h of lessons, 240/12 = 20 and 240/6 = 40). **No conflict**: the rules are satisfiable, so this plan does not
  stop. It does mean the unit needs at least 20 lessons. See open question Q1.
- Proposal: **24 lessons × 10 h = 240 h**, project **60 h** (20 % of 300, inside 10-40 %). Total 300 = curriculum.

## 2. Concept coverage and DAG check

The 13 concepts of M2 (`curriculum/01-foundations.yaml:132-144`, `curriculum/curriculum.json` concepts with `"module": "M2"`)
are each defined in exactly one lesson below. Collisions with concepts owned by later modules (curriculum.json `concepts`):

| Term the M2 core or lab uses | Owner (curriculum.json `concepts`) | Consequence |
|---|---|---|
| Jacobian matrix, Hessian matrix (M2 own) need a matrix or linear-map notion | `linear-map` (M3), `vector-space` (M3), `positive-semidefinite-matrix` (M3) | **DAG_DEFECT** candidate; see Q2 |
| Fubini's theorem | `fubini-theorem` (M6; `curriculum/01-foundations.yaml:276`) | M2 must not `<dfn>` or link it; see Q3 |
| Continuity (epsilon-delta) | `epsilon-delta-continuity` (M5; `01-foundations.yaml:241`) | M2 may use "continuity" in prose only; no dfn, no link |
| Riemann integral | `riemann-stieltjes-integral` (M5; line 249), `lebesgue-integral` (M6; line 273) | M2 defines `definite-integral` by Riemann sums; never names the later concepts as links |
| Constrained optimization, Lagrangian | `lagrange-multiplier` (M7; `01-foundations.yaml:309`), `lagrangian-duality` (M7) | L22 may not define or link them; see Q4 |
| Duration, convexity (lab title) | `duration`, `convexity` (03-markets.yaml lines 37-38; module MKT, after M2) | Preview word only; no dfn, no link; see Q8 |
| Taylor's theorem, derivative, limit, gradient, etc. | M2 (own) | defined once in the lesson in §3 |

Undeclared terms (not in `concepts`): sequence, function, open set, continuity (prose), chain rule, Riemann sum,
iterated integral, Lagrangian, bond, cash flow, matrix. These are plain prose, never `<dfn>`, per the architect's
precedent in the M1 and AC4 plans (Q7).

## 3. Outline (one row per lesson; every M2 concept appears in exactly one row)

| Lesson | Title (working) | Concept defined (`<dfn>`) | Lab twin id (`tests/labs/M2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Sequences and the limit of a sequence | `limit` | `lab-M2-L01-1.py`: limit of a sequence by tabulation, error column against a known limit | 10 | A |
| L02 | Continuity and the limit laws | none (continuity in prose) | `lab-M2-L02-1.py`: limit-law sums and quotients checked on a grid | 10 | A |
| L03 | Limits of functions and one-sided limits | none | `lab-M2-L03-1.py`: one-sided limits of a piecewise function at its break | 10 | A |
| L04 | The derivative as a limit | `derivative` | `lab-M2-L04-1.py`: difference quotient converges to the derivative, error column | 10 | A |
| L05 | Differentiation rules and the chain rule | none (chain rule in prose) | `lab-M2-L05-1.py`: product, quotient and chain rules against central differences | 10 | A |
| L06 | Mean value theorem, monotonicity and extrema | none | `lab-M2-L06-1.py`: sign of the derivative against the monotone intervals of a cubic | 10 | A |
| L07 | Higher derivatives and Taylor polynomials | none | `lab-M2-L07-1.py`: Taylor polynomials of exp at 0 by degree, error column | 10 | B |
| L08 | Taylor's theorem with remainder | `taylor-theorem` | `lab-M2-L08-1.py`: the Lagrange remainder bound checked at sampled points | 10 | B |
| L09 | Riemann sums and the definite integral | `definite-integral` | `lab-M2-L09-1.py`: upper and lower Riemann sums converge to the integral | 10 | B |
| L10 | The fundamental theorem of calculus | none | `lab-M2-L10-1.py`: integral of a derivative recovers the increment | 10 | B |
| L11 | Integration techniques: substitution and parts | none | `lab-M2-L11-1.py`: substitution and parts checked by quadrature to tolerance | 10 | B |
| L12 | Improper integrals | none | `lab-M2-L12-1.py`: truncated integral against a known improper value, convergence rate printed | 10 | B |
| L13 | Finite-difference derivative approximation | `finite-difference-derivative` | `lab-M2-L13-1.py`: forward and central errors against h; the round-off turn-up | 10 | C |
| L14 | Automatic differentiation: forward and reverse mode | `automatic-differentiation` | `lab-M2-L14-1.py`: forward-mode dual numbers against the analytic derivative | 10 | C |
| L15 | Euclidean space, open sets and functions of several variables | none | `lab-M2-L15-1.py`: a function on R^2 tabulated on a grid; continuity checked by sampling | 10 | C |
| L16 | Partial derivatives | `partial-derivative` | `lab-M2-L16-1.py`: each partial by central difference against the closed form | 10 | C |
| L17 | The gradient and the directional derivative | `gradient` | `lab-M2-L17-1.py`: directional derivative equals the gradient dotted with the unit vector | 10 | C |
| L18 | Differentiability and the Jacobian matrix | `jacobian` | `lab-M2-L18-1.py`: Jacobian of a map R^2 to R^2 by finite differences against the closed form | 10 | C |
| L19 | Second-order Taylor expansion and the Hessian matrix | `hessian` | `lab-M2-L19-1.py`: Hessian symmetry (Schwarz) checked; second-order expansion error | 10 | D |
| L20 | Multiple integrals and iterated integrals | `multiple-integral` | `lab-M2-L20-1.py`: double integral over a rectangle by iterated Riemann sums | 10 | D |
| L21 | The implicit-function theorem | `implicit-function-theorem` | `lab-M2-L21-1.py`: implicit derivative dy/dx from F(x,y)=0 against finite differences | 10 | D |
| L22 | Constrained optimization and the envelope theorem | `envelope-theorem` | `lab-M2-L22-1.py`: derivative of the value function equals the partial of the objective at the optimum | 10 | D |
| L23 | Sensitivities of a bond price: a Taylor preview | none | `lab-M2-L23-1.py` (**the curriculum lab**): Taylor expansion of a SIMULATED bond price in its yield; duration and convexity named as a preview | 10 | D |
| L24 | Where numerical sensitivities fail | none | `lab-M2-L24-1.py`: finite-difference error sweep on a kink and near a cancellation | 10 | D |
| hub | Module hub | none | none | - | A |
| project | Sensitivity engine (`both`) | none | `lab-M2-project-1..3` (rungs 1-3) | 60 | E |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | E |
| cards | `cards.json` from L01-L24 | none | none | - | F (after A-D) |

Totals: lessons 24 × 10 = 240 h; project 60 h; unit 300 h. Coverage: 1+0+0+1+0+0+0+0+1+0+0+0+1+1+0+1+1+1+1+1+1+1+1+0+0 =
13 concepts, each in exactly one row (limit L01, derivative L04, taylor-theorem L08, definite-integral L09,
finite-difference-derivative L13, automatic-differentiation L14, partial-derivative L16, gradient L17, jacobian L18,
hessian L19, multiple-integral L20, implicit-function-theorem L21, envelope-theorem L22).

Ordering check (no lesson links a later definition): L04 uses L01 (limit); L08 uses L04 (derivative) and L07; L09 uses
L01-L03 (limit of sums); L13 uses L08 (Taylor) and L04; L14 uses L05 (chain rule); L16 uses L04; L17 uses L16; L18 uses
L16-L17 and the matrix as prose; L19 uses L17-L18 (gradient, Jacobian) and L08; L20 uses L09 and L10; L21 uses L18; L22
uses L17 and L21; L23 uses L08 and L19; L24 uses L13.

Lesson-level constraints: each lesson opens with "why it matters" of at most 120 words, has at least three misconceptions,
at least three problems in each of the four tiers (Mechanics, Proof, Empirical, Research), each with a worked solution in
`<details class="solution">` of at least 15 words (`check_pages.py` lines 285-296), a key-results table, and a quiz of 8-15
items. Tier F keeps rungs 1-2 full (BLUEPRINT §4, §5.1).

The curriculum's one lab (L23, "Taylor expansion of a bond price") is the only lab the curriculum names. Per the M1 and AC2
precedent, every lesson carries one lab (Q15). The lab id must match `lab-M2-<page>-<n>` (`check_pages.py` line 258) and
be numbered in display order.

## 4. Hub (`index.html`, Builder A)

- `<main data-hours-lessons="240" data-hours-project="60">`.
- 4-8 measurable objectives (verbs such as "derive", "compute", "bound").
- Prerequisites: M1 and P0.1, linked. M1 concepts that M2 uses are linked to `../../../concepts.html#<id>`.
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="M2" data-page="placement" data-mastery="0.8">`,
  matching the M1 hub (`course/modules/M/M1/index.html:67`). At least two `data-skill` items test what rungs 1-2 teach
  (the worked example's derivative-by-definition task and the completion problem's missing step); the rest test M1 and P0.1.
- Lesson map linking L01-L24; project ladder (`ol.ladder` with four rung titles in order); data-status section stating
  "No data used" (§7); core reading as registry keys (§6).

## 5. Project ladder and grader design (Builder E)

Project: **Sensitivity engine**. Curriculum scope (`curriculum/01-foundations.yaml:150-156`): first- and second-order
sensitivities for any differentiable pricing function, by analytic, finite-difference and automatic-differentiation
approaches, and where finite differences break. Deliverable: tested module plus an error-analysis note.

Ladder (per BLUEPRINT §5.1 and the M1 / AC2 examples):

1. **Rung 1, worked example** (`lab-M2-project-1`, skippable on placement): one fully solved, annotated sensitivity of the
   SIMULATED bond price in yield, analytic and by central difference, each step annotated with why.
2. **Rung 2, completion** (`section.lab.completion`, `lab-M2-project-2`): the Hessian second difference and the
   AD-derivative lines removed (`___`); graded instantly. Its twin is the completed solution.
3. **Rung 3, independent project** (graded): (a) the autograded module `sensitivity_engine.py` (§5.2); (b) the
   error-analysis note, rubric-graded (§5.3). `lab-M2-project-3` is the rung-3 check.
4. **Rung 4, stretch** (open-ended, not graded): a sensitivity of a multivariable function with a stated hypothesis
   about where its finite differences break.

Time budget (`<table id="hours">`, declared 60 h, every row needs a one-line rationale; `check_projects.py` lines 117-124):

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 4 | Read and annotate one analytic-versus-difference comparison |
| Rung 2 completion | 6 | Fill the second-difference and AD lines, then run the instant check |
| 3a Engine: analytic, FD, AD and Hessian | 22 | Implement and test the four sensitivity paths on the instances |
| 3a' Edge cases and failure behaviour | 6 | Non-positive step, unknown scheme, yield at or below -1 |
| 3b Error-analysis note (rubric) | 14 | Step-size sweep, convergence orders, where differences break |
| 3c Self-check against grader and rubric | 8 | Run the suite; score the note against the two exemplars |
| **Total** | **60** | Equals `data-hours-project` on the hub |

### 5.1 Autograder (`grading: both`, the spec must name both "autograder" and "rubric", `check_projects.py` lines 41-50)

- `grader/instance.py`: `make_instance(seed: int) -> dict`. Deterministic; generates a SIMULATED bond (face in integer
  cents, annual coupon rate, maturity in years, yield) and a smooth test function with seeded parameters. Valid instances
  only: maturity ≥ 1, yield > -1, face > 0. Seeds 0-49 must give materially different answers, not only different labels.
- `grader/reference.py`: the full solution. Must pass every test for seeds 0-49
  (`run_graders.py --unit M2 --seeds 0-49`).
- `grader/starter.py`: stubs raising `NotImplementedError`; the suite must fail on it.
- `grader/test_project.py`: pytest suite checking properties and numbers:
  - analytic first and second derivatives of the price in yield agree with the central difference to a stated tolerance,
    at a step where round-off is negligible (tolerance stated in the spec);
  - forward-mode AD agrees with the analytic derivative to a stated tolerance on the test function;
  - the Hessian of a function is symmetric to tolerance (Schwarz) and its diagonal matches the second difference;
  - the forward difference has error of order h and the central difference of order h² (checked from two step sizes);
  - bond price in integer cents: the reported price is an `int`, and equals the round-half-even of the unrounded price;
  - edge cases: a step of zero or less raises `ValueError`; an unknown scheme raises `ValueError`; yield ≤ -1 raises
    `ValueError`.
- Feedback: a failing test names the violated property and gives a concept hint; it never prints the answer.
- Dual mode: identical suite in Pyodide and CPython; each test < 5 s in Pyodide; suite < 60 s.
- **Five alternative correct implementations must pass** (checked by the verifier): central difference with a Richardson
  extrapolation; complex-step derivative for a real-analytic function; reverse-mode AD; a closed-form analytic price
  derivative written from the cash-flow sum; a NumPy-vectorized implementation. The suite must not fix a default step or a
  scheme name beyond what the spec states.
- **Exception types**: the tests demand `ValueError` only for the three conditions the spec names above. No other
  exception type is required.

Mutants the verifier must write (VERIFIER_RULES §2.6; each must be killed, mutants under `ledgers/M2/mutants/`):
1. forward difference reported as the central difference (order h instead of h²);
2. a step too small for the round-off floor used for the second derivative;
3. AD dropping the product-rule term;
4. Hessian accepted without symmetry check (asymmetric off-diagonal);
5. price rounded by truncation (`int(x)`) instead of round-half-even;
6. a hard-coded answer for seed 0;
7. sign error in the yield derivative.

### 5.2 Engine signatures (proposal; the architect freezes them, Q9)

```python
def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float: ...        # scheme: "forward" | "central"
def ad_derivative(f: Callable[[Dual], Dual], x: float) -> float: ...                                # forward-mode, Dual is student-defined
def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]: ...
def bond_price_cents(instance: dict[str, Any]) -> int: ...                                         # integer cents, round-half-even
def sensitivities(instance: dict[str, Any]) -> dict[str, float]: ...                               # keys: "dprice_dy", "d2price_dy2", "duration_analytic", "convexity_analytic"
```

### 5.3 Rubric and exemplars (`grading: both`)

Five criteria (4-7 required, `check_projects.py` lines 58-71), each with four observable levels (`table.rubric`):

1. **Truncation and round-off.** Level 4 states both error terms for each scheme and reports a step-size sweep table with the
   turning point; level 1 says "small h is better" with no sweep.
2. **Where differences break.** Level 4 names the kink and the cancellation case, each with a sweep row; level 1 has no case.
3. **Agreement with the analytic value.** Level 4 reports, per seed used, the analytic, FD and AD values and the tolerance;
   level 1 reports no comparison.
4. **Convergence orders.** Level 4 derives each order (grade T, steps shown); level 1 asserts orders without a derivation.
5. **Units and conventions.** Level 4 states price per 100 face or per unit, yield compounding and the derivative's units, and
   uses them consistently; level 1 leaves a derivative's unit unstated.

Exemplars at level 4 and level 2, fully written, annotated per criterion (`exemplar data-level="4"` and `data-level="2"`).
Self-assessment form; the page shows where the student's score diverged from the exemplar score.
Not adversarial: no question bank (`check_projects.py` requires 15 angles only for an adversarial project, Q10).

## 6. Real-data policy and references

### 6.1 Real data: none

- No dataset in `course/assets/data/market/MANIFEST.json` relates to calculus; the MANIFEST holds `fx_daily`, `fx_monthly`
  and `ust_daily` only (`tools/data_sources.yaml` lines 19, 53, 91, per the AC4 plan's read). No `data-files` attribute is used,
  so `check_pages.py` `check_data_files` is vacuous.
- Lab L23 and the project use **generated bond specifications and test functions, labelled SIMULATED** on the page, in the
  figure source line and in the grader docstring (BLUEPRINT §5.3). The label "illustrative input, not market data" is not
  enough: the word SIMULATED is required.
- No DATA_REQUESTS entry is needed.

### 6.2 Registry keys the module may cite

| Key | Verified record (`references/references.json`) | Use in M2 | Flag |
|---|---|---|---|
| `spivak2008calculus` | Spivak, *Calculus*, Publish or Perish, Open Library, year 2008, status verified, `used_by` ["M2"] | the curriculum source; cite with a locator only after the builder has read the locator in a source that reproduces it | record carries no edition; the curriculum's "4th ed." is in `source_strings` only |
| `hubbard2015vector` | Hubbard & Hubbard, Matrix Editions, Open Library, year 2015, status verified, `used_by` ["M2"] | Jacobian, Hessian and multivariable results, cited with a confirmed locator only | record carries no edition; "5th ed." is in `source_strings` only |
| `velleman2019prove` | verified (Crossref), `used_by` ["M1"] | not a curriculum source for M2; usable only if the architect approves (Q11) | none |

Builders cite the key only. Any number or theorem attributed to Spivak or Hubbard that the builder cannot confirm at a
locator is either derived on the page (grade T with a proof) or left out. Never type bibliographic data, a table, a page
or a coefficient from memory.

### 6.3 REFERENCE_REQUESTS

- None required by the curriculum: both named sources are registered. If a builder needs a source for the convergence of
  the Riemann sums or for the Schwarz theorem, it is a REFERENCE_REQUEST with DOI or ISBN, and the architect resolves it via
  `add_reference.py`. The planner has not verified any new source, so none is requested here.

## 7. Atlas and studios

- **Atlas: none.** No atlas entry names M2 (§0). The project has no `atlas:` key, so `check_projects.py` lines 144-146 do not
  apply. No `atlas/A*.contract.md` is needed or drafted.
- **Studios:** STUDIO-M requires M7 and M8 (`curriculum/01-foundations.yaml:73-76`), not M2. No studio reuse point is needed.

## 8. Commands for this unit (targeted, run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit M2          # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M2
.venv/bin/python tools/check_projects.py --unit M2
.venv/bin/python tools/run_labs.py --unit M2             # --page L23 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/M/M2/L01.html   # per page, after each twin is written
.venv/bin/python tools/run_graders.py --unit M2 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit M2 --seeds 0-9     # verifier only
.venv/bin/ruff check tests/labs/M2 course/modules/M/M2/grader && .venv/bin/ruff format --check tests/labs/M2
.venv/bin/mypy tests/labs/M2 course/modules/M/M2/grader           # strict, repo configuration
```

Flags are the repo's own (read from argparse blocks): `check_pages.py --unit/--page/--all` (line 429), `check_dag.py --unit`
(line 89), `check_projects.py --unit` (line 159), `run_labs.py --unit/--page` (lines 119-121), `run_graders.py
--unit/--seeds` (lines 129-131), `mutate_graders.py --unit/--seeds` (lines 30-32). The planner did not execute them; they
are unverified against M2.

Not run by builders: `page_smoke.py` (verifiers, quiet machine). Repository-wide gates (`check_pages.py --all`,
`build_site.py --check`, `render_curriculum.py`) are the architect's, once, before merge.

## 9. Open questions for the architect (numbered; each needs a decision)

1. **Lesson count and hours.** The 6-12 h rule plus 240 h of lessons forces 20-40 lessons. The proposal is 24 × 10 h with a
   60 h project. With 13 concepts, 11 lessons define no concept. Confirm, or name another split (for example 20 × 12 h).
2. **Jacobian and Hessian (DAG).** `jacobian` and `hessian` are defined as matrices. The curriculum places `linear-map`,
   `vector-space` and `positive-semidefinite-matrix` in M3 (`curriculum.json` concepts). Options: (a) define them as arrays of
   partial derivatives in prose, with "matrix" as an undeclared term; (b) record a DAG_DEFECT and move both to M3 (curriculum
   change). Planner recommends (a) for this unit and a curriculum note.
3. **Fubini's theorem (DAG).** `fubini-theorem` is owned by M6 (`curriculum/01-foundations.yaml:276`). L20 may state
   iterated-integral equality for a continuous function on a rectangle, but may not dfn or link `fubini-theorem`. Is an
   unproved statement with hypotheses acceptable (grade T requires a proof or a precise cited locator)? Or is the statement
   cited to `spivak2008calculus` at a locator the builder confirms? Architect decides which.
4. **Constrained envelope theorem (DAG).** L22 needs constraints. `lagrange-multiplier` (M7, `01-foundations.yaml:309`) is
   outside the closure. Option (a): state the envelope theorem for the unconstrained problem and for a constraint written as an
   equation absorbed into the parameter, naming no multiplier concept. Option (b): allow the multiplier in prose, undefined.
   Planner recommends (a).
5. **Continuity.** `epsilon-delta-continuity` belongs to M5 (`01-foundations.yaml:241`). L02 uses "continuity" in prose only.
   Confirm.
6. **Riemann integral.** `definite-integral` is defined by Riemann sums. Confirm that the later concepts
   (`riemann-stieltjes-integral` M5, `lebesgue-integral` M6) are not named as links; they may be named in "where the canon
   breaks" prose only if the architect allows.
7. **Undeclared prose terms.** Sequence, function, open set, continuity, chain rule, Riemann sum, iterated integral,
   Lagrangian, bond, cash flow and matrix are prose, with no `<dfn>`, per the M1 Q3 and AC4 Q4 decisions. Confirm. BLUEPRINT §8
   asks for `<dfn>` at a term's first appearance per `glossary.json`; a GLOSSARY_REQUEST is the other route.
8. **Lab L23 wording.** The curriculum's lab text (`01-foundations.yaml:148`) names "duration and convexity", which the
   curriculum defines later in `03-markets.yaml:37-38`. Keep the words as a named preview with no dfn and no link (planner
   recommends), or ask the architect to reword the curriculum lab.
9. **Engine interface.** Freeze the §5.2 signatures, the module name `sensitivity_engine.py`, and the tolerances in the spec.
   Confirm that `sensitivity_engine.py` is the student file and `reference.py` is excluded from deployment (BLUEPRINT §7).
10. **Adversarial or not.** The error-analysis note is not an IC defense, so no 15-angle question bank is planned. Confirm.
11. **Velleman for proofs.** M2's proofs (the Taylor remainder, the mean value theorem, Fubini) may need a citation for proof
    technique. `velleman2019prove` is not in the M2 sources (`01-foundations.yaml:145-147`). Allow it, or none.
12. **Money in the engine.** The bond price is reported in integer cents (round-half-even). Sensitivities are derivatives,
    not money, so they are floats with a stated tolerance. Confirm that this is the intended scope of the integer-cents rule
    (user-level CLAUDE.md money rule, stated there for Rust/PG/TS and not in BUILDER_RULES.md).
13. **NumPy in labs.** `tools/vendor_spec.yaml:59` lists numpy, scipy and pytest, so the labs may use NumPy under Pyodide, unlike
    the M1 labs (standard library only). Confirm.
14. **Registry edition gaps.** The Spivak and Hubbard records carry no edition field. Builders cite keys, and the curriculum's
    edition strings are in `source_strings`. Confirm no further registry action is needed before builders start.
15. **Lab count.** One lab per lesson (24) plus three project labs. Confirm, following the M1 Q2 and AC2 precedents.

## 10. Tooling assumptions that do not hold for M2 (flagged)

1. **No Atlas milestone** (§7). `check_projects.py` lines 144-146 do not apply; no contract is needed.
2. **No debate tag** (§0). `check_pages.py` line 412 does not trigger.
3. **Foundations graded `both`** (`01-foundations.yaml:156`). `check_projects.py` requires both an autograder and a rubric with
   exemplars at two or more levels (lines 38-71, 138-139).
4. **Lab per lesson** is stricter than the curriculum's single named lab (`01-foundations.yaml:148`). The plan follows the
   BUILDER_RULES §3.4 rule that every key formula gets a numerical check.
5. **`check_dag.py` checks links, not prose.** Its docstring states that a concept used by name without a link cannot be
   detected statically; the verifier reads for it (VERIFIER_RULES §2.9). The name collisions in §2 are therefore a reading
   task, not a tool check.
6. **Cards need one set per lesson.** `check_pages.py` line 398 requires at least one card per lesson, so 24 lessons need cards.
7. **No data-driven figure.** Charts draw formula output or seeded simulation, labelled "computed from the formula" or SIMULATED,
   with a source line and caption (BUILDER_RULES §6.4).

## 11. DAG problems

- **DAG_DEFECT (candidate):** Jacobian and Hessian need a matrix or linear-map notion owned by M3 (Q2). Not a build failure
  under the prose rule, but a curriculum-level ordering question.
- **Name collisions, no defect yet:** Fubini (M6), continuity (M5), Riemann-Stieltjes (M5), Lebesgue (M6), Lagrange multiplier
  (M7), duration and convexity (MKT, later). M2 must neither define nor link these (§2, Q3-Q8).
- **Closure check:** every concept M2 links is in the closure (M1, P0.1) or is M2's own. None is used from a later module by
  link. No concept from a module after M2 is introduced by M2.

## 12. Builder rules (binding, adapted to M2; BUILDER_RULES and the verification campaign lessons)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2, this file. Study
  `course/modules/M/M1/` (template, lab embedding, ladder, cards) and `course/modules/AC/AC4/` (rubric and `both` grading).
  Imitate structure, not wording.
- **Evidence.** Every substantive claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key from §6.2, or it is a
  derivation on the page. Theorems carry the hypotheses explicitly (for example Taylor's theorem: f is n+1 times differentiable
  on the interval; IFT: F is C¹ and the partial in y is non-zero at the point; Fubini-type statement: continuous on a rectangle;
  envelope: unique interior optimum and differentiable objective). A proof sketch is labelled, and it names the skipped steps.
- **Numbers recomputed from unrounded values.** Every displayed number is recomputed from the unrounded value (a lab's float or
  the closed form), never from a rounded table entry.
- **Lab statements match code and output.** A lab's hypothesis and interpretation describe exactly what the twin prints; the
  twin's `main()` is called at module top level (unguarded), so the lab runs the same way under Pyodide and CPython.
- **Attribute nothing unread.** Every registry key and every locator is read before it is used. Unread sources are not cited.
- **Scope words need a computation.** Words such as "small", "fast", "smooth", "most", "typically", "in practice" are used only
  where a lab, figure or table shows the computation. Otherwise they are deleted.
- **Define before use.** A term is defined (or linked) at its first appearance in the lesson sequence; the lesson never
  relies on a later definition.
- **Proposition hypotheses explicit.** Each theorem lists all of its hypotheses in its statement, not in a footnote.
- **Grader tests demand an exception type only for conditions the page names.** Tests accept the five alternative correct
  implementations in §5.1. No test fixes a default step, a scheme name or an internal representation beyond the spec.
- **Integer cents for money.** The bond price is `int` cents with a stated rounding rule; no float money anywhere. Sensitivities
  are not money (Q12). The money rule is the user-level CLAUDE.md rule (BUILDER_RULES.md does not state it).
- **No horizontal scroll at 360 px.** Long code lines in labs and the grader wrap or sit in a scroll container inside the
  block; the page itself never scrolls horizontally at 360 px. Charts draw at the container width.
- **Labs call `main()` at top level** (unguarded), so the twin runs the same under Pyodide and CPython.
- **No placeholders.** No TODO, TBD, lorem, "for brevity", "beyond the scope", "left as an exercise" without a worked solution,
  "it is important to note", "studies show", "it is well known".
- **No code that has not run.** Every executable block and grader passes under the pinned runtime.
- Builders write only their own lesson files and twins; the hub is written by Builder A after its lessons exist. Builder E's
  grader is independent of the lessons. Builder F writes `cards.json` after A-D.
- Output: `course/modules/M/M2/...`, `tests/labs/M2/lab-M2-Lnn-1.py` (and `lab-M2-project-n.py`). No `git commit`, no push.
  Report files written, the hours per lesson, the commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

## 13. After the builders

1. Orchestrator integrates; runs the §8 commands once; fixes cross-lesson defects (DAG, links, hours).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L06, L07-L12, L13-L18, L19-L24, project. The project verifier
   writes at least three mutants per round (VERIFIER_RULES §2.6). Failures return to a builder with only the failing rows.
3. Ledger at `ledgers/M2.verification.json`; scripts archived under `ledgers/M2/scripts/` (VERIFIER_RULES §3).
4. Merge only when the unit ledger is PASS, or its remaining gaps are named and agreed. Never merged incomplete.

## Architect decisions (2026-10-28, binding)
Q1: 24 x 10 h lessons with a 60 h project confirmed. Q2: Jacobian and Hessian are defined as arrays of partial derivatives in prose; no M3 concept link, no M3 prerequisite. Q3: Fubini is stated as a hypothesis-stated result without proof and without a citation locator; say it is not proved here. Q4: the envelope theorem is stated without Lagrange multipliers (no multiplier concept). Q5/Q6/Q7: continuity, undeclared terms and later-module concepts are plain prose with no dfn and no link. Q8: lab L23 previews duration and convexity as unlinked text. Q9: module `sensitivity_engine.py`; freeze the signatures in the plan before building. Q10: not adversarial, no question bank. Q11: `velleman2019prove` may be cited for proof technique only. Q12: bond prices in integer cents; sensitivities are floats with a stated tolerance. Q13: NumPy allowed (data-packages numpy). Q14/Q15: no registry action; one lab per lesson plus three project labs.
