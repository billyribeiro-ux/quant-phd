# M4 build plan: Probability (2026-10-28)

Unit: **M4 · Probability** · tier F · 120 h · prerequisites M2 · no Atlas milestone · grading `both` (autograder for the
tail-risk simulator, rubric for the proof appendix) · output directory `course/modules/M/M4/` (part code `M`).
Planner: Haiku, plan only. No lesson content, no git operations. Executors: Haiku builders, then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence: every curriculum statement below carries `file:line` read during planning. Anything not in the curriculum is
marked **not in curriculum**. Shape and decisions follow `plans/M1-build-plan.md` and `plans/AC4-build-plan.md`.

## Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| M4 id, title "Probability", tier F, hours 120, prereqs [M2] | `curriculum/01-foundations.yaml:190-194` (id 190, tier 192, hours 193, prereqs 194) |
| Core text (distributions, expectation, MGFs and characteristic functions, multivariate normal, conditioning, LLN, CLT, heavy tails, failure of the CLT under infinite variance) | `curriculum/01-foundations.yaml:195-198` |
| M4 introduces 19 concepts, one entry each | `curriculum/01-foundations.yaml:199-218` |
| Sources: "Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)" (free text) | `curriculum/01-foundations.yaml:219-220` |
| Lab: "Sample-mean behaviour under Gaussian, Student-t(3) and Cauchy draws." | `curriculum/01-foundations.yaml:221` |
| Project "Tail-risk simulator": simulate portfolio losses under multivariate Gaussian vs multivariate Student-t returns with matched covariance; quantify the 99% loss estimate change; prove the moment conditions | `curriculum/01-foundations.yaml:222-227` |
| Deliverable "Simulator plus a proof appendix."; grading `both` | `curriculum/01-foundations.yaml:228-229` |
| M4 has no `debate` key, so no debate brief is required (`check_pages.py` line 412 keys on `u.entry.get("debate")`) | `curriculum/01-foundations.yaml:190-229` (absent) |
| No Atlas milestone names M4: the atlas block lists A1-A20; the only M-part module named there is GM4 (A20, module `GM4`) | `curriculum/meta.yaml:194-276` (A20 `module: GM4` at 276) |
| No studio requires M4 (STUDIO-M requires M7, M8) | `curriculum/01-foundations.yaml:73-76` |
| Prerequisite closure of M4 = {M2, M1, P0.1}; M3 is not in it | `curriculum/01-foundations.yaml:126` (M2 prereqs [M1]); M1 prereqs [P0.1]; computed from `curriculum/curriculum.json` `parts` (planner script, session) |
| JSON row for M4 mirrors the YAML (hours 120, prereqs, 19 introduces, sources, lab, grading both) | `curriculum/curriculum.json:6423` (`"id": "M4"`) |
| Concepts whose module is M4 in `curriculum.json` = the same 19 ids | planner script over `concepts` (session) |
| Registry key for Blitzstein exists: `blitzstein2019introduction`, verified, Crossref, DOI 10.1201/9780429428357, year 2019, `used_by: ["M4"]`, record has no edition field | `references/references.json` entry `blitzstein2019introduction` (grep at line 3127) |
| M6 requires M4 and M5 (dependents; no action for M4) | `curriculum/01-foundations.yaml:265` |

**Hours arithmetic (checked against the tool rules).** 120 h = lessons 90 h + project 30 h. Project 30/120 = 25%, inside
the 10-40% band (`tools/check_pages.py` line 339). Ten lessons of 9 h each give 90 h, inside the 6-12 h lesson band
(`tools/check_pages.py` line 227). **No conflict between the curriculum hours and the tool rules, so no STOP is needed.**

## Rules for every builder (binding; BUILDER_RULES adapted to M4)

- Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what will be
  checked), this file. Study `course/modules/M/M1/` (index, one lesson, project, grader panel, cards) and
  `course/modules/S/S7/` (rubric memo with exemplars) as worked examples. Imitate structure, not wording.
- **Evidence.** Every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key. The only registry key this
  unit may cite is `blitzstein2019introduction` (see §6). A locator (`data-locator`) is written only after the builder has
  opened the book (or a source that reproduces the result) and read the locator. Otherwise the claim is a derivation on
  the page (grade T, full proof) or is left out. Never type a theorem number, page, table, or bibliographic detail from
  memory.
- **Attribute nothing unread.** A sentence that says what a source shows is written only for a claim whose locator was
  read. "The book proves X" with no read locator fails.
- **Numbers from unrounded values.** Every displayed number is computed from the unrounded float or Fraction, then
  rounded for display only. A printed figure never feeds a later computation.
- **Lab statements match code and output.** The hypothesis sentence states what the twin prints and what the expected
  value is; the interpretation names only what the printed output shows. Re-check after `embed_labs.py`.
- **Scope words need a computation.** "Heavy", "fat", "rare", "most", "much larger", "converges quickly", "usually" are
  allowed only where a printed number on the same page supports the word. Otherwise delete the word.
- **Define before use.** Each concept in §2 is defined with `<dfn>` before any later use. Undeclared terms (§5) are
  defined inline by their formula at first use, in the lesson where first used, and never with `<dfn>`.
- **Proposition hypotheses explicit.** Every theorem and derivation lists its assumptions in the statement (finite
  variance, \(\nu > 2\), independence, identically distributed, and so on). A result used without its hypothesis fails.
- **Integer cents for money.** Any money value in a lab, the grader or the spec is an `int` number of cents. Losses are
  computed in float, then rounded to integer cents by the rule stated on the page (`round()`, half to even), once, at the
  output. No float money value leaves the simulator.
- **No horizontal scroll at 360 px.** Wide tables sit in a scrolling wrapper inside their own box; code blocks scroll
  inside `<pre>`; the page body never scrolls sideways. Checked by the verifier with `page_smoke.py` at 360 px.
- **Labs call `main()` at top level.** Each twin ends with an unguarded `main()` call at module top level. No
  `if __name__ == "__main__":` guard, because Pyodide runs the twin as a script with no such name.
- **Grader tests demand an exception type only for conditions the page names.** A test may assert `ValueError` only for
  an invalid input the spec lists by name (for example \(\nu \le 2\)). Other failures are asserted by value or property.
- **Five alternative correct implementations must pass the suite.** The grader tests check properties and values with
  tolerances, not one implementation's exact random stream. See §5.3 for the five variants and Q9 for where they live.
- Concepts: each of the 19 in §2 is defined exactly once, with `<dfn id="def-<id>" data-concept="<id>">`, in the lesson
  assigned below. Linked elsewhere with `<a class="concept" data-concept="<id>" href="Lnn.html#def-<id>">` for an earlier
  lesson of M4, or `href="../../../concepts.html#<id>"` for M1, M2 and P0.1 concepts. A lesson never links a concept
  defined in a later lesson (`check_dag.py`).
- Labs: code lives once, in the twin `tests/labs/M4/lab-M4-Lnn-1.py` (rung-1 and rung-2 twins `lab-M4-project-1.py` and
  `lab-M4-project-2.py`). The page carries `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py <page>` fills them.
  Never type expected output. Labs are seeded, use the standard library only (`random`, `fractions`, `math`, `statistics`,
  `itertools`; no NumPy), run under 10 s in Pyodide, and need no network. Lab ids must match `lab-M4-<page>-<n>`
  (`check_pages.py` line 258). Labs have no `data-files`.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `references/*.json`, `course/assets/data/*`, `MANIFEST.json`). Never edit `curriculum/*.yaml`.
- Do not run `page_smoke.py` (verifiers run it on a quiet machine). Targeted checks only (§Commands).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap or request in the
  BUILDER_RULES §10 output contract.
- Prose must not contain the strings banned by `check_pages.py` (`BANNED`, lines 58-74). Note `\.\.\.` is banned in
  visible prose: write "through" or use `\(\dots\)` inside math. `clearly` and `obviously` are banned.

## Outline and file ownership (fixed by this plan; do not move concepts between lessons)

Ten lessons. Each concept of the nineteen is assigned to exactly one row (verified in §2 coverage check).

| Lesson | Title (working) | Concepts it defines | Hours | Lab (twin id) | Owner |
|---|---|---|---|---|---|
| L01 | Random variables, distributions and quantiles | `random-variable`, `quantile-function` | 9 | `lab-M4-L01-1`: a finite discrete distribution as a table; its CDF and quantile function computed exactly with `Fraction` | Builder A |
| L02 | Expectation and variance | `expectation`, `variance` | 9 | `lab-M4-L02-1`: exact expectation and variance of a fair die and of a two-point loss; a sample check, seeded | Builder A |
| L03 | Skewness and kurtosis | `skewness`, `kurtosis` | 9 | `lab-M4-L03-1`: standardized third and fourth moments of a skewed discrete law, exact, then a seeded sample | Builder A |
| L04 | Independence and conditional expectation (elementary) | `independence`, `conditional-expectation-elementary` | 9 | `lab-M4-L04-1`: independence tested on a finite joint table; conditional expectation from the table | Builder B |
| L05 | Covariance, correlation and the covariance matrix | `correlation`, `covariance-matrix` | 9 | `lab-M4-L05-1`: sample covariance matrix of a seeded two-asset Gaussian draw against the generating matrix | Builder B |
| L06 | Normal and Student-t distributions | `normal-distribution`, `student-t-distribution` | 9 | `lab-M4-L06-1`: Student-t built from a normal over an independent chi-square; variance \(\nu/(\nu-2)\) checked for \(\nu > 2\) | Builder B |
| L07 | Moment-generating and characteristic functions | `moment-generating-function`, `characteristic-function` | 9 | `lab-M4-L07-1`: normal MGF checked by numerical integration against the closed form; characteristic function of a two-point law | Builder B |
| L08 | The multivariate normal | `multivariate-normal` | 9 | `lab-M4-L08-1`: linear image of a standard normal vector; sample covariance versus \(AA^{\top}\) | Builder C |
| L09 | Laws of large numbers and the central limit theorem | `law-of-large-numbers`, `central-limit-theorem` | 9 | `lab-M4-L09-1`: running sample mean of a finite-variance law; the standardized sample mean's tail probability against \(\Phi\) at seeded sample sizes | Builder C |
| L10 | Heavy tails and the failure of the CLT under infinite variance | `heavy-tailed-distribution`, `infinite-variance-clt-failure` | 9 | `lab-M4-L10-1` (**the curriculum lab**): sample means under Gaussian, Student-t(3) and Cauchy draws (`yaml:221`) | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 90 / 30 | none | - | none | Builder A |
| project | Tail-risk simulator (`both`) | none | 30 | `lab-M4-project-1` (rung 1), `lab-M4-project-2` (rung 2, completion), `lab-M4-project-3` (rung 3 check) | Builder D |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | - | none | Builder D |
| cards | `cards.json` from L01-L10 | none | - | none | Builder E (after A-C) |

Totals: lessons 10 x 9 = 90 h; project 30 h; unit 120 h = curriculum `yaml:193`.

**Concept coverage check.** 2+2+2+2+2+2+2+1+2+2 = 19, one row each, matching the 19 entries at `yaml:200-218`.

**Ordering check.** L02 uses L01's random variable; L03 uses L02's expectation and variance; L04 uses L01 and L02; L05 uses
L02 (covariance is an expectation of a product); L06 uses L02, L03 (the Student-t kurtosis is out of scope, §5), and L05
for the covariance matrix of a multivariate t in L08; L07 uses L02 and L06; L08 uses L05 and L07; L09 uses L02, L05 and
M2's `limit`; L10 uses L03, L06 and L09. No lesson links a later definition.

**Note on the core text.** "Conditioning" in the core (`yaml:197`) is taught only in its elementary discrete form (L04),
which is what `conditional-expectation-elementary` (`yaml:213`) names. Any general conditioning is **not in curriculum**
and is out of scope; the hub says so.

## Hub (index.html, Builder A)

- `<main data-hours-lessons="90" data-hours-project="30">` (sums to the curriculum 120).
- 4-8 measurable objectives (for example: compute the mean, variance and quantile of a finite law; state and check the
  hypotheses of the LLN and the CLT; decide when a sample mean is unreliable). Each uses a measurable verb.
- Prerequisites linked to M2 and M1 with their concept links (`limit` is M2's and usable, `exponential-and-logarithm` is
  M1's and usable).
- Placement: `<section class="quiz" id="placement" data-unit="M4" data-page="placement" data-mastery="0.8">`, the same bar
  as M1 and AP1. At least two `data-skill` items test what rungs 1-2 teach (the worked example's quantile calculation and
  the completion problem's missing step). The rest test M1 and M2 prerequisites.
- Lesson map linking L01-L10. Project ladder `ol#ladder` with four `rung-title` items in order.
- Tier F: rungs 1-2 keep full length (BLUEPRINT §4 minimum applies from tier M upward).
- Hub states plainly: no debate brief (none tagged), no Atlas milestone, no embedded data (SIMULATED throughout).

## Lesson content guidance (what each must establish; the builder decides the argument)

- **L01** `random-variable`: a function on a sample space with a distribution. `quantile-function`: the generalized
  inverse \(F^{-1}(p) = \inf\{x : F(x) \ge p\}\), with the left-continuity note; this is the convention the project uses
  (§4). Every example uses a finite table, computed with `Fraction`.
- **L02** `expectation`: finite sums first, then the integral form in M2's `definite-integral` (usable, M2 closure).
  `variance`: \(\operatorname{Var}(X) = E[X^2] - (EX)^2\), derived in full. Show the scale rule \(\operatorname{Var}(aX) = a^2 \operatorname{Var}(X)\).
- **L03** `skewness`: third standardized moment \(E[((X-\mu)/\sigma)^3]\); `kurtosis`: fourth, \(E[((X-\mu)/\sigma)^4]\). The
  word "moment" is defined inline here, first use (§5). Normal kurtosis = 3 is derived, not cited.
- **L04** `independence`: \(P(A \cap B) = P(A)P(B)\) for events; for variables, factorization of the joint table. Show that
  independence implies zero covariance and that zero covariance does not imply independence (a finite counterexample,
  computed). `conditional-expectation-elementary`: \(E[X \mid Y = y]\) from a finite joint table only.
- **L05** `correlation`: \(\rho = \operatorname{Cov}(X,Y)/(\sigma_X \sigma_Y)\), with \(|\rho| \le 1\) proved (Cauchy-Schwarz,
  stated with its hypothesis). `covariance-matrix`: \(\Sigma_{ij} = \operatorname{Cov}(X_i, X_j)\); show it is symmetric and
  positive semidefinite by \(w^{\top}\Sigma w = \operatorname{Var}(w^{\top}X) \ge 0\) (self-contained, §5, no M3 link).
- **L06** `normal-distribution`: density, standardization, \(E[X]=\mu\), \(\operatorname{Var}(X)=\sigma^2\). `student-t-distribution`:
  \(T = Z / \sqrt{W/\nu}\) with \(W\) chi-square, independent of \(Z\). Prove \(\operatorname{Var}(T) = \nu/(\nu-2)\) for \(\nu > 2\) and
  state that the variance is infinite for \(\nu \le 2\) (hypothesis explicit).
- **L07** `moment-generating-function`: \(M_X(t) = E[e^{tX}]\) with the domain stated; normal MGF \(e^{\mu t + \sigma^2 t^2/2}\)
  derived by completing the square. `characteristic-function`: \(\varphi_X(t) = E[e^{itX}]\), defined for every real \(t\);
  complex exponentials are defined inline (§5).
- **L08** `multivariate-normal`: \(X = \mu + AZ\) with \(Z\) i.i.d. standard normal; \(\operatorname{Cov}(X) = AA^{\top}\) derived. The
  density is stated for a positive definite \(\Sigma\) only; the determinant and inverse are used as plain prose (§5).
- **L09** `law-of-large-numbers`: weak law for i.i.d. finite-variance variables, via Chebyshev (both hypotheses stated).
  `central-limit-theorem`: statement for i.i.d. finite-variance variables; the standardized sample mean converges in
  distribution to \(N(0,1)\). Limits use M2's `limit`. The CLT is graded T only with a complete proof on the page (for example via characteristic functions, L07, with the finite-variance hypothesis stated). If the proof is not written in full, the statement is graded A or B with a read locator from `blitzstein2019introduction` (§6), or it is left out.
- **L10** `heavy-tailed-distribution`: defined by tail decay. The word "heavy" is used only with a computed tail ratio on the
  page (scope rule). `infinite-variance-clt-failure`: for Cauchy and Student-t(3), the sample mean does not settle; the
  claim is stated as a computed simulation result (grade T for the derivation of infinite variance, the simulation is a lab
  result, not a theorem about the CLT). The lab (`lab-M4-L10-1`) prints the running means and the variance of the
  standardized sample means. The stable-limit statement is **not** in the registry (§6, REFERENCE_REQUESTS), so the page
  states it as an assumption-marked remark with no citation, graded D until a source is admitted.

## Project ladder (Builder D), per BLUEPRINT §5 and the M1 example

Rung 1 · Worked example: `lab-M4-project-1`. A fully solved, annotated computation for one seeded instance: the Gaussian
portfolio loss distribution, its 99% quantile under the page's convention, and the matched Student-t scale factor
\((\nu-2)/\nu\) with each step explained.

Rung 2 · Completion problem: `lab-M4-project-2`, `class="lab completion"`. The same task with two lines blanked (`___`):
the matched-covariance scale factor and the quantile index. Graded instantly. The twin is the completed solution.

Rung 3 · Independent project: `tail_risk.py` (module name proposed, Q7) implementing the functions in §5.3, plus the proof
appendix (moment conditions of the matched Student-t). Graded by the autograder (the simulator) and the rubric (the
appendix). `lab-M4-project-3` is the rung-3 check.

Rung 4 · Stretch: open-ended, for the portfolio. Example directions, none graded: a skew-t margin, or a proof that
\(\operatorname{Var}\) of a sum of t variables is additive only under independence (with the hypothesis checked).

### Time budget (`<table id="hours">`, declared 30 h, every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 2 | Read and annotate one seeded computation, line by line |
| Rung 2 completion | 2 | Fill two blanks and run the instant check |
| Simulator: Gaussian and matched-t sampling, quantile, tests | 12 | Implement `simulate_losses` and `quantile_99`, then check against the properties in §5.3 |
| Proof appendix: moments of the Student-t and the matched scale | 8 | Write the derivations of L06 for the matched case, with hypotheses |
| Report and self-assessment against the exemplars | 4 | One-page results note; score the two exemplars and compare |
| Self-check against the grader | 2 | Run the local suite, fix property failures |
| **Total** | **30** | Equals `data-hours-project` on the hub |

## Grader design (Builder D)

Grading is `both`. The spec's grading entry must name both "autograder" and "rubric" (`tools/check_projects.py` lines 41-50).
The project page carries `section.grader-panel` with `data-unit="M4" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="tail_risk.py" data-starter="starter.py"`
(`check_projects.py` lines 122-135). Standard library only: `data-packages` is empty.

### 5.1 Instances (`grader/instance.py`)

- `make_instance(seed: int) -> dict[str, Any]`. Deterministic per seed. Generates a valid instance only: 2 or 3 assets; a
  positive definite covariance built from a seeded lower-triangular factor with a positive diagonal; integer position
  values in cents (positive); a Student-t degrees-of-freedom \(\nu\) in \(\{3,\dots,8\}\) (\(\nu > 2\) always); a sample size from a fixed set
  bounded for Pyodide timing (§5.4).
- Docstring and the page label every instance **SIMULATED** ("generated inputs, not market data").
- Seeds 0-49 give materially different answers (the losses change, not only the labels).

### 5.2 Reference (`grader/reference.py`) and starter (`grader/starter.py`)

- `reference.py` is the full solution. It must pass every test on seeds 0-49 (`run_graders.py --unit M4 --seeds 0-49`).
- `starter.py` raises `NotImplementedError` in every function. The suite must fail on it (`run_graders.py` checks this).

### 5.3 Frozen interface (proposal, Q7) and tests

`tail_risk.py` exposes exactly these, frozen in the spec:

- `matched_scale(nu: int) -> float`: returns \((\nu-2)/\nu\). Raises `ValueError` when \(\nu \le 2\) (named on the page, so allowed).
- `simulate_losses(position_cents: list[int], cov: list[list[float]], n_draws: int, seed: int, family: str, nu: int | None) -> list[int]`:
  one loss per draw in integer cents, \(\text{loss} = -\sum_i w_i r_i\) with \(w_i\) the position in cents, \(r_i\) the return.
  `family` is `"gaussian"` or `"student_t"`; `nu` is required for `"student_t"` and must be `None` for `"gaussian"`.
  Rounding: `round()` of the float loss, once, at output.
- `quantile_99(losses_cents: list[int]) -> int`: the \(\lceil 0.99\,n\rceil\)-th smallest loss (order statistic, the
  convention of L01's \(F^{-1}\)). Raises `ValueError` for an empty list (named on the page).

Test properties (no hard-coded answers; each check uses the instance's own parameters):

1. Matched covariance: the sample covariance of the Student-t losses' underlying returns is within a stated tolerance of
   \(\Sigma\), using the matched scale; and the Gaussian sample covariance matches \(\Sigma\) to the same tolerance.
2. Sign convention: a long-only position with a positive mean return has a negative mean loss.
3. Quantile convention: `quantile_99` equals the order statistic on the list, exactly (integer comparison).
4. Integer cents: every element of the output is `int` (type and value), not `float`.
5. Edge cases: `nu` equal to 2 raises `ValueError`; `family="gaussian"` with a non-None `nu` is rejected with `ValueError`
   (only if the spec names it; it does, §5.3).
6. Determinism: the same seed returns the same list.
7. Runtime: the whole suite under 60 s; each test under 5 s in Pyodide.

Failure messages name the violated property and give a concept hint. They never print the answer.

### 5.4 Pyodide timing

Each simulation call uses `n_draws` no greater than 20,000 in tests (so the suite meets the 5 s per-test limit in
Pyodide). The verifier times this in `page_smoke.py`. (Q12.)

### 5.5 Five alternative correct implementations (must pass the suite)

The suite must pass five independently written correct implementations, not only `reference.py`:

1. Box-Muller for normal draws (instead of `random.gauss`).
2. Polar (Marsaglia) method for normal draws.
3. Cholesky factor computed row by row for \(\Sigma\).
4. A chi-square draw as a sum of \(\nu\) squared normals (integer \(\nu\)) instead of a gamma draw.
5. Quantile by full sort versus `heapq.nsmallest`, same order statistic.

Each differs in its random stream, so the suite's tests must be property-based (§5.3), never exact-draw comparisons. The
five files live under `tests/graders/M4/` (Q9); `run_graders.py` does not run them (§Tooling).

### 5.6 Mutants (verifier writes at least three; each must be killed)

1. Covariance not rescaled: uses \(\Sigma\) instead of \(\frac{\nu-2}{\nu}\Sigma\) for the t draws (wrong matched covariance).
2. `matched_scale` accepts \(\nu = 2\) (no guard).
3. Quantile off by one order statistic (uses \(\lfloor 0.99\,n\rfloor\)).
4. Losses returned as floats, not integer cents.
5. Sign flip: gains reported as losses.
6. A hard-coded answer for seed 0.

### 5.7 Rubric (proof appendix, the `both` rubric half)

- 4-7 criteria, four observable levels each. Example criteria: (1) the moment of \(T\) is derived with its hypothesis
  \(\nu > 2\) stated; (2) the matched scale is derived, not asserted; (3) the \(\nu \le 2\) case is shown to have infinite
  variance with the integral named; (4) the report ties each quoted loss to a printed line; (5) every displayed number
  is from unrounded values; (6) scope words in the report are backed by a number.
- Exemplars at level 4 and level 2, fully written, with annotations mapping each passage to descriptors met or missed.
- Self-assessment form; the page shows where the student's scoring diverged from the exemplar scoring.
- No question bank (the appendix is not an adversarial defence, Q13).

## Cards builder (Builder E, after A-C)

- `course/modules/M/M4/cards.json`, ids `M4-c001` upward, `lesson` in L01-L10 (each lesson at least one card:
  `check_pages.py` `check_cards`). One card per definition, theorem statement, key formula, key result and misconception.
- Theorems and derivations are grade **T** and need no cite. A non-T card needs a `cite` (registry key) or a `basis`
  naming the lab or problem where the lesson itself establishes it, for example `"basis": "Lab 10, Problem E2 (simulation)"`.
- `cite` may contain only `blitzstein2019introduction`, and only where its locator has been read (§6).
- Cards test one fact each, and each back is checkable against the lesson text (BUILDER_RULES §7).

## Registry keys the module may cite (verified in `references/references.json`)

| Key | Status (read) | Use in M4 |
|---|---|---|
| `blitzstein2019introduction` | verified, Crossref book, DOI 10.1201/9780429428357, year 2019, `used_by: ["M4"]` | the curriculum source (`yaml:219-220`). Cite a locator only after reading it in the book. The record has no edition field, so "2nd ed." is not verified by the registry (Q6) |

No other key is cited by M4 without architect approval (§6). `velleman2019prove` (M1's key) is not a curriculum source for M4 and
is not used.

## REFERENCE_REQUESTS

Planner does not type bibliographic data from memory, so these are needs only:

1. **Stable-limit / infinite-variance CLT source.** `infinite-variance-clt-failure` is named in the curriculum (`yaml:218`), and
   the only curriculum source is `blitzstein2019introduction`. No verified registry entry establishes the stable limit of
   sample means under infinite variance. Needed for: the L10 remark. Confidence: none (the planner has no candidate).
   Architect to nominate a source with a DOI or ISBN for `add_reference.py`.
2. **Locator confirmation for `blitzstein2019introduction`.** Needed for every cited Blitzstein claim (L01-L09). Builder
   reads the book; if the book cannot be read, claims stay derivations (grade T with full proofs) or go unlocated.

## Registry candidates NOT curriculum-listed for M4 (architect decision, Q14)

- `billingsley2012probability` (verified, `used_by: ["M6"]`), a measure-theoretic probability text; not for M4 without approval.
- `gine1997student` (verified, `used_by: ["S7"]`), on when the Student-t statistic is asymptotically standard normal; relevant
  to L09-L10 only with approval and a read locator.
- Heavy-tail and fat-tail records under `S7` (for example `kao2025estimated`, `wang2023catoni`) are for a later unit; not used.

## Real-data policy

- **No real data.** The curriculum names no dataset for M4 (`yaml:219-221`). No lab, figure or grader reads a snapshot. The
  lab and grader inputs are generated from formulas and seeds, labelled **SIMULATED** on every page, figure and in the grader
  docstring (BLUEPRINT §5.3).
- No `data-files` attribute on any lab; no MANIFEST entry; no `DATA_REQUESTS`.
- Any figure is labelled "computed from the formula or a seeded simulation; no data", and its source line says so.

## Atlas

**No Atlas milestone.** No atlas entry names M4 (`curriculum/meta.yaml:194-276`), and the project has no `atlas:` key
(`yaml:222-229`). No `atlas/A*.contract.md` is needed or drafted. The grader's solution file is unit-local
(`tail_risk.py`), as in the AP1 and AC4 pattern.

## Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit M4            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit M4
.venv/bin/python tools/check_projects.py --unit M4
.venv/bin/python tools/embed_labs.py course/modules/M/M4/L01.html   # per page, after each twin is written; --refresh <lab-id> after a twin edit
.venv/bin/python tools/run_labs.py --unit M4              # --page L10 for one lesson
.venv/bin/python tools/run_graders.py --unit M4 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit M4 --seeds 0-9   # verifier only
.venv/bin/ruff check tests/labs/M4 course/modules/M/M4 && .venv/bin/ruff format --check tests/labs/M4
.venv/bin/mypy                                            # strict, repo configuration (the project gate)
```

Notes:
- `check_pages`, `check_dag`, `check_projects` take `--unit` (`tools/check_pages.py` line 429, `tools/check_dag.py` line 89,
  `tools/check_projects.py` line 159). `run_labs.py` takes `--unit` and `--page`; `run_graders.py` takes `--unit` and `--seeds`
  (lines 129-131); `mutate_graders.py` takes `--unit` and `--seeds`.
- Not run by builders: `page_smoke.py` (verifiers, quiet machine). Repo-wide gates (`check_pages.py --all`,
  `build_site.py --check`, `render_curriculum.py`) are the architect's, once, before merge.
- The `tests/graders/M4/` alternatives (§5.5) need their own runner (Q9); no listed command runs them.

## Tooling assumptions that do not hold for M4 (flagged)

1. **`run_graders.py` runs only `grader/reference.py`.** `grade()` calls `workspace(u, grader / "reference.py", cfg)`
   (`tools/run_graders.py`, inside `grade()`), so the `data-solution` file and any alternative implementation are never run. The
   five alternatives (§5.5) therefore need a separate runner or a pytest module under `tests/` (Q9).
2. **`run_graders.py` imports NumPy at top level** (`tools/run_graders.py` line 35). The runner needs NumPy in `.venv`; the
   grader and its suite do not (standard library only).
3. **Banned-phrase scan covers visible prose.** `visible_text` removes `<code>`, `<pre>`, and `\(...\)`/`\[...\]` math
   (`tools/coursekit.py` lines 336-352), but a bare `...` in prose fails `check_pages.py`. Use words or `\(\dots\)`.
4. **Rung 2 needs a completion lab or a quiz** (`check_projects.py` line 90). The completion lab is `section.lab.completion`.
5. **The rubric check counts `table.rubric` rows** (`check_projects.py` lines 66-75): one header row, then 4-7 criteria, each
   with exactly four `td` cells. The exemplars need `data-level` 1-4 and at least two distinct levels.
6. **No debate, no Atlas, no `data-files`.** The debate check (`check_pages.py` line 412), the Atlas check (`check_projects.py`
   lines 145-146) and the data-file check do not apply.
7. **Lesson hours.** Each lesson declares `data-hours="9"`; the hub's `data-hours-lessons` must equal their sum (90).
8. **Cards.** `check_cards` needs at least one card per lesson and rejects a non-T card with neither `cite` nor `basis`.

## DAG check (prerequisite closure {M1, M2, P0.1})

- **Usable and linkable:** M2 `limit`, `derivative`, `definite-integral`, `multiple-integral`, `taylor-theorem`,
  `partial-derivative`; M1 `exponential-and-logarithm`, `geometric-series`, `quantifiers`, `direct-proof`,
  `proof-by-contradiction`, `mathematical-induction`, `present-value`, `discount-factor`, and the other M1 concepts;
  P0.1 `evidence-grade`, `robustness-check`, etc. (not needed on M4 pages).
- **Outside the closure (DAG_DEFECT if linked, Q2):** M3's `vector-space`, `linear-map`, `eigendecomposition`,
  `spectral-theorem`, `positive-semidefinite-matrix`, `singular-value-decomposition`, `orthogonal-projection`,
  `least-squares-projection`, `principal-component-analysis`, `eigenvalue-clipping`, `nearest-correlation-matrix`. M4's
  `multivariate-normal` and `covariance-matrix` need matrix facts (positive semidefiniteness, the determinant and the
  inverse of \(\Sigma\), a Cholesky-type factor \(A\)). Plan: no M3 link; positive semidefiniteness is derived in L05 from
  \(w^{\top}\Sigma w = \operatorname{Var}(w^{\top}X)\); matrix inverse and determinant are plain prose; the factor \(A\) is
  introduced as "any matrix with \(AA^{\top} = \Sigma\)" in L08.
- **Undeclared terms, prose only, never `<dfn>` (check_dag would reject a dfn for a non-introduced concept):** moment (used
  before L03 for skewness and kurtosis, defined inline there), chi-square distribution, Cauchy distribution, complex-valued
  exponential, determinant, matrix inverse, Cholesky-type factor, stable law, order statistic. Q3.
- Nothing in M4 links an M5 or later concept. M4 is in the prerequisite closure of M6 (`yaml:265`), so M4 must not use M5 or M6 concepts.

## Open questions for the architect (numbered)

1. **Hours split.** Ten lessons of 9 h plus a 30 h project (25%) is proposed. Alternative: nine lessons (for example 10 h each)
   with the same 30 h project. Confirm, or pick another split within 10-40%.
2. **Matrix facts outside the closure.** M3 is not a prerequisite of M4 (`yaml:194` lists only M2). Options: (a) the plan above
   (self-contained derivations, no M3 link, matrix terms in prose); (b) a curriculum change making M3 a prerequisite (not
   proposed here, and a human decision). Planner recommends (a).
3. **Undeclared terms.** Confirm the list in the DAG section stays prose (no `<dfn>`), each defined inline at first use, as
   decided for M1 (Q3) and AC4 (Q4).
4. **Curriculum lab placement.** `yaml:221` names one lab. Proposed: it is `lab-M4-L10-1` (L10 holds the heavy-tail and CLT-failure
   concepts, and Cauchy and Student-t(3) are defined by then). One lab per lesson (M1 Q2 precedent), so there are ten lesson
   twins plus three project twins. Confirm.
5. **Sources.** Only `blitzstein2019introduction` (M1 Q4 precedent). The stable-limit claim has no source (REFERENCE_REQUESTS 1).
   Confirm the claim stays a no-citation remark graded D, or that the architect nominates a source.
6. **Edition string.** The curriculum says "2nd ed. (2019)" (`yaml:220`); the record has year 2019 and no edition field. Confirm
   the key may be cited, or correct the registry through the registry tools (the builder does not change the key).
7. **Module and frozen signatures.** Proposed `tail_risk.py` with the three functions of §5.3 (AC4 Q7 precedent). Confirm the name
   and freeze the signatures in the spec before builders start.
8. **Money.** Integer cents for losses and positions, `round()` once at output (M1 and AC4 Q9/Q10 precedent). Confirm.
9. **Five alternatives and their location.** `run_graders.py` does not run them (Tooling 1). Proposed: `tests/graders/M4/alt_1.py`
   to `alt_5.py`, run by a pytest module under `tests/` that the verifier adds. Confirm, or name another runner.
10. **Quantile convention.** Proposed \(\lceil 0.99\,n\rceil\)-th order statistic, exact integer comparison. Confirm, or accept a
    tolerance of one order statistic.
11. **Degrees of freedom.** Proposed \(\nu\) drawn per seed from \(\{3,\dots,8\}\). Note \(\nu = 3\) has finite variance but infinite
    kurtosis (a hypothesis-dependent fact the proof appendix must state). Confirm the set.
12. **Pyodide timing.** `n_draws` capped at 20,000 in tests. Confirm, or name the cap.
13. **Adversarial.** The proof appendix is not an IC defence; no 15-angle question bank (`check_projects.py` applies it only to a
    `question-bank` section). Confirm.
14. **Non-curriculum registry candidates.** Confirm that `billingsley2012probability` (M6) and `gine1997student` (S7) stay unused by
    M4, or approve adding M4 to their `used_by` after a read locator.
15. **Cauchy and chi-square as prose.** Confirm that the Cauchy distribution is written as the Student-t with \(\nu = 1\) in L10
    (the \(\nu \ge 1\) definition of L06 is then needed) or defined inline as a ratio of independent normals. Planner prefers the
    ratio definition, which needs no extension of L06.

## Architect decisions (2026-10-28, binding)
Q1: 10 x 9 h and a 30 h project. Q2: self-contained derivation; no M3 prerequisite; matrix facts proved from the quadratic form. Q3: moment, chi-square, Cauchy, determinant, order statistic stay plain prose. Q4: curriculum lab in L10. Q5: Blitzstein is the only source; the stable-limit claim is stated as unproved, uncited and ungraded, listed as a REFERENCE_REQUEST. The project's five alternative implementations are written by the project builder in tests/graders-style scratch files under ledgers/M4/scripts/ and run by the verifier. Remaining questions: follow the plan's recommendation.
