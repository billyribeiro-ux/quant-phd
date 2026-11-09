# S2 build plan: Linear Regression (planner output, 2026-11-09)

Unit: **S2 · Linear Regression** · tier U · 120 h · prerequisites S1, M3 · no Atlas milestone · no debate key · grading `autograder`
(no rubric) · output directory `course/modules/S/S2/` (part code `S`, as S7) · lab twins `tests/labs/S2/` · solution file
`inference_engine.py` (unit-local, as M3 `covariance_doctor.py`).
Planner: Haiku (claude-haiku-5-5), plan only. Executors: Haiku builders A to E (and F for cards), then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger. No git operations, no commits, no pushes.

Evidence convention: every statement about the curriculum, the registry, the notation registry or a tool cites `file:line`
read during planning. Anything not found in those sources is marked **NOT IN CURRICULUM**, **NOT IN REGISTRY** or **NOT VERIFIED**.

Nearest built prerequisite, read in full for its structure and decisions: **M3** (`plans/M3-build-plan.md`; M3 is built at
`course/modules/M/M3/`). S1 is not built (`course/modules/S/` holds only S7), so S1 concepts are linked through
`concepts.html` anchors only, as E5 did for unbuilt E1.

**Status: BLOCKING ISSUES EXIST (§0.3). The hours are feasible and the unit needs no real data. The architect must decide
B1 (the statsmodels validation brief cannot run in the dual-mode grader), B2 (outside-closure concepts that are downstream of
S2 cannot be prerequisites), and B3 (three literature items have no registry record) before the builders start.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| S2 entry: id, title "Linear Regression" | `curriculum/01-foundations.yaml:661-662`; JSON `curriculum/curriculum.json:6956-6957` |
| Tier `U`, hours `120` | `01-foundations.yaml:663-664`; JSON `:6958-6959` |
| Prerequisites `[S1, M3]` | `01-foundations.yaml:665`; JSON `:6960-6963` |
| Core: "OLS geometry, Gauss–Markov, asymptotics, heteroskedasticity-robust and HAC errors, clustering, errors-in-variables, Stambaugh bias in predictive regressions." | `01-foundations.yaml:666-669`; JSON `:6964` |
| `introduces` has **12** concepts: ols-estimator, frisch-waugh-lovell-theorem, gauss-markov-theorem, coefficient-of-determination, ols-asymptotics, omitted-variable-bias, heteroskedasticity-robust-standard-errors, hac-standard-errors, clustered-standard-errors, two-way-clustering, errors-in-variables, stambaugh-bias | `01-foundations.yaml:670-682` (one per line 671-682); JSON `:6965-6978` |
| Sources: four strings: White (1980) Econometrica 48(4); Newey & West (1987) Econometrica 55(3); Petersen (2009) RFS 22(1); Stambaugh (1999) JFE 54(3) | `01-foundations.yaml:683-687`; JSON `:6979-6984` |
| Lab: "Stambaugh-bias Monte Carlo." | `01-foundations.yaml:688`; JSON `:6985` |
| Project "Inference engine"; brief: "Implement OLS with classical, White, Newey–West and two-way clustered standard errors, validated against statsmodels and by simulated coverage rates."; deliverable "Tested module plus a coverage study."; grading `autograder` | `01-foundations.yaml:689-696` (brief 691-694, deliverable 695, grading 696); JSON `:6986-6990` |
| No `debate:` key on S2 | `01-foundations.yaml:661-696` (absent); JSON `:6956-6992` (absent) |
| No `atlas:` key on the S2 project; no Atlas entry names S2 | `01-foundations.yaml:689-696`; `curriculum/curriculum.json` `atlas` array (planner check: no entry contains "S2") |
| S2 is required by the bachelor's credential BS-FIN | `curriculum/meta.yaml:63` |
| S2 is in the Regression & Econometrics course map (alone) | `curriculum/meta.yaml:68` |
| S2 is in the doctoral first-year sequence group Econometrics I–II | `curriculum/meta.yaml:131` |
| S2 is in the CFA topic "Quantitative Methods" | `curriculum/meta.yaml:154` |
| Rendered CURRICULUM.md agrees | `CURRICULUM.md:38` (course-map row, 120 h), `CURRICULUM.md:325-326` (core and introduces) |
| S1 prerequisites `[M4, S0]`; S1 id | `01-foundations.yaml:619` (id), `:623` (prereqs) |
| M3 id, tier F, prerequisites `[M1]` | `01-foundations.yaml:157` (id); M3 plan §0 |
| S3 is a dependent of S2: S3 prerequisites `[S2]` | `01-foundations.yaml:697` (id), `:701` (prereqs) |
| Other dependents of S2 (computed, closure contains S2): AC2, E8, F1, PR1, QR3, S3, S4, S5, S6, S7 | `tools/coursekit.py` `prerequisite_closure` run by the planner this session (see §4) |
| Prerequisite closure of S2 = **{CS1, M1, M2, M3, M4, P0.1, S0, S1}**; the usable concepts (sum of `introduces` over the closure modules) = **112** | `tools/coursekit.py` `prerequisite_closure("S2")` run by the planner; module introduces from `curriculum/curriculum.json` parts/modules |
| Concept owners used in §4 (module field of each concept) | `curriculum/curriculum.json` `concepts` dict (starts `:1172`; e.g. `central-limit-theorem` M4 at `:1737`, `ols-estimator` S2 at `:4133`) |
| Closure-relevant M4 concepts used by S2 (in closure): central-limit-theorem, law-of-large-numbers, expectation, variance, covariance-matrix, correlation, multivariate-normal, normal-distribution, student-t-distribution, conditional-expectation-elementary | `curriculum/curriculum.json` `concepts` (module M4) |
| Closure-relevant M3 concepts (in closure): orthogonal-projection, least-squares-projection, positive-semidefinite-matrix, spectral-theorem | `curriculum/curriculum.json` `concepts` (module M3) |
| Closure-relevant S1 concepts (in closure): estimator, estimator-bias-variance, consistent-estimator, delta-method, hypothesis-test, confidence-interval, coverage-probability, bootstrap, t-statistic (planner list) | `curriculum/curriculum.json` `concepts` (module S1) |
| Closure-relevant P0.1 concepts (in closure): identification, paper-anatomy | `curriculum/curriculum.json` `concepts` (module P0.1) |
| Closure-relevant CS1 concept (in closure): unit-test | `curriculum/curriculum.json` `concepts` (module CS1) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 120 h (`01-foundations.yaml:664`). The tool rules:

- lesson `data-hours` 6 to 12 (`tools/check_pages.py:227-228`);
- hub `data-hours-lessons + data-hours-project = 120` (`tools/check_pages.py:337-338`);
- project share 10 to 40 percent of 120, i.e. 12 to 48 h (`tools/check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split: **12 lessons × 7 h = 84 h; project 36 h (30.0%)**. 84 + 36 = 120. Feasible. **No STOP condition on hours.**
The lesson count matches the builder allocation in §1 (about three lessons per builder). Alternatives are in §12 Q2.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. The brief asks for validation against statsmodels, and no dual-mode runtime can run it.**
- The brief says "validated against statsmodels" (`01-foundations.yaml:693`; JSON `:6988`).
- The vendored Pyodide packages are exactly `[numpy, scipy, pytest]` (`tools/vendor_spec.yaml:59`). The grader must run identically
  in the browser and locally (BUILDER_RULES §5.3.4; BLUEPRINT §5.2), so a statsmodels test cannot run in the browser unless
  statsmodels is vendored. Whether Pyodide 314.0.7 ships statsmodels was **NOT VERIFIED** (the planner did not read the Pyodide lock).
- No tool or page in the repository mentions statsmodels (planner grep of `tools/`, `curriculum/`, `course/modules/S/`).
- **Plan's default:** validation against exact closed forms and against independent implementations in §5.4 (alternatives
  A1 to A5 are the independent implementations). The curriculum text is not edited by builders (BUILDER_RULES §1.9: no edits
  outside the output directory). The architect either (a) accepts the default and amends `yaml:693` by a curriculum
  change, or (b) adds statsmodels to `tools/vendor_spec.yaml` after verifying its Pyodide availability.

**B2. Four outside-closure concepts that S2 content naturally uses are downstream of S2 and cannot be prerequisites.**
- S3, S4, S5, S6 and S7 all list S2 in their prerequisite closure (computed, §0.1). Making any of their concepts a prerequisite
  of S2 creates a cycle. Their concepts include `stationarity`, `unit-root`, `autocorrelation-function`, `instrumental-variables`,
  `panel-fixed-effects` and `generalized-method-of-moments` (§4, D1 to D8).
- **Plan's default:** plain prose with no link and no `<dfn>` for each of those words (the E5 plan's "Architect decisions"
  block, 2026-10-28, sets this default for every module: concepts outside the closure are plain prose), and every assumption that depends on them written as a numbered Assumption (fixer-rules line 12). Confirm in §12 Q4.

**B3. Three literature items the lessons need have no registry record.**
- Two-way clustered variance (the curriculum concept at `01-foundations.yaml:680`): the multiway-clustering literature is **NOT IN
  REGISTRY**. Without it, L11 states the formula as a definition and makes no claim about its properties beyond the identities
  it proves (§3, L11).
- Errors-in-variables (`01-foundations.yaml:681`): no registry record for the measurement-error literature. L06 derives attenuation
  under stated assumptions (T) and cites no source for it.
- Frisch–Waugh–Lovell (`01-foundations.yaml:672`): the theorem is derived on the page (T), so no record is needed for the proof.
  A historical citation needs a registry record that does not exist. Lead-only REFERENCE_REQUEST (§7.2).

Non-blocking, the architect should see them:

- **N1. Petersen record: no conflict.** The curriculum says "Petersen (2009), RFS 22(1)" (`01-foundations.yaml:686`). The record
  `petersen2008estimating` (`references/references.json:19015`) has `print_year` 2009, volume 22, issue 1; its `year` field 2008 is the
  online year (`years` [2008, 2009]). Cite the key; the year in prose is 2009 (print year).
- **N2. No real data is needed.** The curriculum names no embedded dataset for S2 (`01-foundations.yaml:688`, `:689-696`). Every lab
  and the project use SIMULATED data (§6). No `DATA_REQUEST` is required.
- **N3. Notation conflict.** `T` is registered as "number of return observations (periods) in a sample", module S1
  (`notation/notation.json:112-115`). S2 uses `n` for sample size (§2.3; §12 Q3).
- **N4. Concept links to unbuilt S1 go to `concepts.html` only**, and M3 links may go to the built M3 hub.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

12 lessons × 7 h = 84 h; project 36 h; total 120 h. Twelve concepts (`01-foundations.yaml:671-682`), exactly one per lesson, in
the order below. The order is the dependency order: each lesson uses only earlier lessons, the closure, and §4 plain prose.

| Lesson | Title (working) | Concept it defines (`introduces`) | Lab (twin id, `tests/labs/S2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Ordinary least squares as orthogonal projection | `ols-estimator` (`yaml:671`) | `lab-S2-L01-1`: normal equations and the projection matrix on seeded integer-valued data, exact in `Fraction`; residual orthogonality checked exactly | 7 | Builder A |
| L02 | Partialling out: the Frisch–Waugh–Lovell theorem | `frisch-waugh-lovell-theorem` (`:672`) | `lab-S2-L02-1`: the coefficient of one regressor from the full regression equals the slope from residual-on-residual regression; difference printed exactly | 7 | Builder A |
| L03 | Fit and the coefficient of determination | `coefficient-of-determination` (`:674`) | `lab-S2-L03-1`: 1 − RSS/TSS equals the squared correlation of the actual and fitted values (intercept included), in `Fraction` | 7 | Builder A |
| L04 | Gauss–Markov: the best linear unbiased estimator | `gauss-markov-theorem` (`:673`) | `lab-S2-L04-1`: Monte Carlo variance of OLS against a second linear unbiased slope estimator on a fixed design (SIMULATED) | 7 | Builder B |
| L05 | Omitted-variable bias | `omitted-variable-bias` (`:676`) | `lab-S2-L05-1`: short-regression slope against β₁ + β₂δ on a seeded design; the exact identity checked, the Monte Carlo printed (SIMULATED) | 7 | Builder B |
| L06 | Errors-in-variables bias | `errors-in-variables` (`:681`) | `lab-S2-L06-1`: attenuation of a slope under classical measurement error against the reliability ratio (SIMULATED) | 7 | Builder B |
| L07 | The asymptotic distribution of OLS | `ols-asymptotics` (`:675`) | `lab-S2-L07-1`: coverage of the asymptotic t interval for n = 20, 80, 320 under non-normal errors (SIMULATED) | 7 | Builder C |
| L08 | Heteroskedasticity-robust (White) standard errors | `heteroskedasticity-robust-standard-errors` (`:677`) | `lab-S2-L08-1`: classical against White coverage when the error scale depends on x (SIMULATED) | 7 | Builder C |
| L09 | HAC (Newey–West) standard errors | `hac-standard-errors` (`:678`) | `lab-S2-L09-1`: the lag-zero identity to White exactly; coverage under AR(1) errors (SIMULATED) | 7 | Builder C |
| L10 | Clustered standard errors | `clustered-standard-errors` (`:679`) | `lab-S2-L10-1`: classical against cluster-robust coverage under a within-cluster correlation; the design effect printed (SIMULATED) | 7 | Builder D |
| L11 | Two-way clustered standard errors | `two-way-clustering` (`:680`) | `lab-S2-L11-1`: identical clusterings reduce exactly to one-way; coverage with firm and time effects (SIMULATED) | 7 | Builder D |
| L12 | Predictive regressions and Stambaugh bias | `stambaugh-bias` (`:682`) | `lab-S2-L12-1` (**the curriculum lab**, `:688`): the Stambaugh-bias Monte Carlo for a persistent predictor with correlated innovations (SIMULATED) | 7 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 84 / 36 | none | none | - | Builder A |
| project | Inference engine: four-rung ladder, autograder spec, hours | none | `lab-S2-project-1` (rung 1), `lab-S2-project-2` (rung 2, `class="lab completion"`), `lab-S2-project-3` (rung 3 check) | 36 | Builder E |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01 to L12 | none | none | - | Builder F (after A to D) |

Totals: lessons 7 × 12 = 84 h; project 36 h (30.0%, inside 10 to 40 percent); unit 120 h.
Per builder: A owns L01 to L03 and `index.html` (21 h); B owns L04 to L06 (21 h); C owns L07 to L09 (21 h); D owns L10 to L12,
including the curriculum lab (21 h); E owns `project.html`, `grader/`, the project labs and their twins (36 h, no lessons).

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes `index.html` last, after L01 to L03
exist, because the lesson map lists all twelve titles and each hub title must match its lesson's `<h1>` at integration
(precedent: CF1 KNOWN 3). Builder E does not depend on lesson text; its concept names come from §3.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4 for plain-prose uses):
- L01 uses M3 `least-squares-projection` and `orthogonal-projection`, and M3 `positive-semidefinite-matrix` for X'X (closure).
- L02 uses L01 (projection onto the complement of the other regressors).
- L03 uses L01 (fitted values) and M4 `correlation` (closure).
- L04 uses L01 to L03 and S1 `estimator-bias-variance` (closure).
- L05 uses L01, S1 `estimator` and `consistent-estimator` (closure), and P0.1 `identification` (closure; linked as
  `../../../concepts.html#identification`).
- L06 uses L05 (the same algebra) and M4 `variance` (closure).
- L07 uses M4 `law-of-large-numbers`, `central-limit-theorem`, `multivariate-normal` (closure), S1 `delta-method` (closure), and L04
  for the classical variance.
- L08 uses L04 (classical variance) and L07 (sandwich asymptotics).
- L09 uses L08 (the meat) and L07; its lag-zero identity is L08.
- L10 uses L08 (the meat with cluster sums) and M4 `covariance-matrix` (closure).
- L11 uses L10 (one-way cluster variance) only.
- L12 uses L05 (bias), L07 (asymptotic inference), S1 `coverage-probability` (closure) and S1 `confidence-interval` (closure).

Hours check: 7 × 12 = 84 (hub `data-hours-lessons="84"`); project 36 (hub `data-hours-project="36"`); 120 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to S2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `plans/E5-build-plan.md` (the structure template),
`plans/M3-build-plan.md` (the nearest built prerequisite, with its autograder precedent), `/Users/billyribeiro/.fanout/fixer-rules.md`,
`plans/FINAL-ARCHITECT-RULINGS.md`, this file. Study `course/modules/S/S7/` (an autograded module in part S: `grader/`, panel,
ladder) and `course/modules/M/M3/` for layout. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) where the claim
   is exact, and from unrounded floats where it is a Monte Carlo. Monte Carlo rates state their replications R and the
   binomial standard error sqrt(p(1−p)/R) (a derivation, grade T). Rounding is stated where a rounded figure is shown.
   Precedents: AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only what the
   printed numbers show, in the design the lab simulates. Precedent: M1 LESSON_TEXT_DEFECTS ("checked directly" with no lab).
3. **Attribute nothing unread.** Only the registry keys in §7.1 may be cited. A key is cited at paper level, with no locator, unless the
   builder has read the abstract (VERIFIER §2.1). **The registry stores no abstracts** (planner grep for `abstract` in
   `references/references.json` returned only URLs). So a builder who has not read an abstract writes a naming sentence only: the
   page cites the record and states that it makes no claim about its results (precedent: E3 L05 to L06, ruling 39). Builders record
   what they read in `plans/S2-open-items.md`. No page, table, equation or coefficient is typed from memory.
4. **Scope words need a computation or a stated assumption.** "every", "all", "always", "never", "any", "best", "unbiased",
   "efficient", "robust", "valid", "consistent", "exact" are used only where a derivation (named assumptions), a finite check or a
   lab computes the claim. "Robust" is always followed by the assumption it relaxes. Gauss–Markov's "best" is written
   "best among linear unbiased estimators under A1 to A4".
5. **Define before use.** Each of the 12 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its lesson, never
   before it. Terms outside the 12 (heteroskedasticity, autocovariance, residual, hat matrix, endogeneity, exogeneity,
   multicollinearity, cluster, intraclass correlation, F-test, chi-squared distribution, Wald statistic, stable AR(1), design effect)
   use a plain `<dfn>` with no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`, E5 §2.1 item 5).
6. **Proposition hypotheses explicit (numbered Assumptions).** Every Theorem, Proposition and Derivation block lists its numbered
   Assumptions (A1, A2, ...) before the statement. Required assumptions, stated in the lesson where first used:
   - OLS: X has full column rank (A1), n > k.
   - Gauss–Markov: linearity, E[ε | X] = 0, Var(ε | X) = σ² I, full rank (A1 to A4).
   - Asymptotics: i.i.d. draws, finite second moments, Q = E[x x'] positive definite, finite fourth moments for consistent variance.
   - HAC consistency: the lag growth and mixing conditions are **named as an Assumption and not proved** (the proof is a sketch
     labelled as one and names the steps it skips; fixer-rules line 12, "ASSUMED FACTS").
   - Cluster sandwich: independence across clusters, finite moments, a fixed number of clusters G ≥ 1.
   - Stambaugh: the stable AR(1) predictor (|ρ| < 1), the innovation covariance σ_uv stated, and the assumed start of the predictor.
7. **Grader rule.** Applies in full (§5.4). The rules of fixer-rules line 19 are binding: each condition the page names gets its own
   isolated test in both directions; no test demands an exception type the page does not name; failure messages never print the
   expected value (`__tracebackhide__`); the collect-only count is quoted on the page.
8. **Money.** S2 has no money output. Standard errors and coverage rates are floats with stated tolerances.
9. **No horizontal scroll at 360 px.** Matrix displays and code blocks sit in scroll containers; tables wrap; no element forces the
   page wider than 360 px (fixer-rules line 14: `wbr`, `table-wrap`, escape `\$` inside math). `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` and has no `if __name__ == "__main__":` guard.
    `run_labs.py` runs each twin as `python -I -W error <twin>` with no network (`tools/run_labs.py:1-20`; the M1 twin
    `tests/labs/M1/lab-M1-L04-1.py` is the model). `tests/test_labs.py` runs the same checks in CI.
11. **Basis-explicit rates and conventions.** Every rate, coverage, bias and standard error states its unit, its estimator, its
    replications and its seed. Autocovariances are written `\Gamma_j` (§2.3).
12. **Macros.** Real numbers are written `\R` (FINAL-ARCHITECT-RULINGS 1), never `\mathbb{R}`. Standard error is `\se`
    (registered, `notation/notation.json` macros). Variance and covariance are `\Var` and `\Cov`. Plims are written
    `\hat\beta \pto \beta` (registered `\pto`); no `\plim` macro is requested (§12 Q3).
13. **Honest-pending definitions.** A concept whose lesson defines it only in a model may carry a visible "definition pending" note
    (FINAL-ARCHITECT-RULINGS 14). No S2 concept should need one.
14. **T versus C for worked values** (FINAL-ARCHITECT-RULINGS 13). A value derived by hand in a numbered Example is grade T with the
    Example as basis. A value that appears only in lab output is grade C naming the lab.
15. **Process words.** No learner-visible "build", "builder", "round", "verifier", "REQUESTS", "unit report" (fixer-rules line 14).
16. **Lesson sizes.** Each lesson: `<html data-hours="7">`, at least 3 misconceptions (`tools/check_pages.py:279-280`), at least 3
    problems in each of Mechanics, Proof, Empirical and Research, each with a solution of at least 15 words
    (`tools/check_pages.py:290-295`), a retrieval quiz of 8 to 15 items each with an explanation (`:302-307`), and a
    `why-it-matters` paragraph of at most 120 words (`:243-244`).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded claim
  names its published counter-evidence (BUILDER_RULES §2.5). For S2 the counter-evidence candidates in the registry are the
  predictability-critique records in §7.1 (`welch2007comprehensive`, `campbell2007predicting`, `cochrane2007dog`), each to be read
  before a claim is made. Multiway-clustering and errors-in-variables counter-evidence has no record (B3, §7.2).
- Concepts: §1 table. `<dfn>` only for the 12 registered concepts plus plain `<dfn>` for other terms (§2.1 item 5).
- Prerequisite links: `href="../../../concepts.html#<id>"` for CS1, M1, M2, M3, M4, P0.1 and S1 concepts; `href="Lnn.html#def-<id>"`
  for earlier S2 lessons. A lesson never links a concept defined in a later lesson. No link to an unbuilt S1 hub.
- Labs: code lives once, in `tests/labs/S2/lab-S2-Lnn-1.py` (and `lab-S2-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-S2-<page>-<n>`
  (`tools/check_pages.py:258`). Standard library only: `fractions`, `math`, `random.Random(seed)` (decision in §12 Q11). Seeded RNG
  only; no network; under 10 s in Pyodide; no warnings under `-W error`.
- SIMULATED label: every lab and every figure that draws random data carries **SIMULATED** (BUILDER_RULES §1.7, BLUEPRINT §5.3).
  In S2 that is every lab, since the Monte Carlo and the seeded designs are generated (fixer-rules line 7: the label says what
  the code does).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py:58-74`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope", "left as an
  exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously",
  "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth rates are not used. Bias is stated in absolute units of the coefficient.
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in BUILDER_RULES §10.
- Process safety (FINAL-ARCHITECT-RULINGS 20): no process is killed by pattern (no pkill, no killall).

### 2.3 Notation (binding; `notation/notation.json`)

| Registered symbol or macro | Registered meaning (locator) | S2 rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation.json:112-115`, module S1) | **Not used in S2.** Sample size is `n`; time index `t`; number of regressors `k`. Newey–West lag bound is `L`. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and quantile (`notation.json:117`, module M4) | Not used. The t critical value is `t_critical(df)` in prose and code. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (`:122-127`, M4) | Not used. Autocovariances are `\Gamma_j` (capital Greek, unregistered), so `\gamma_j` never appears. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | AP1 symbols (`:129-`) | Not used. |
| `\E` | expectation operator (macro) | Use for E[ε | X] and E[x x']. |
| `\Var`, `\Cov`, `\Corr` | variance, covariance, correlation (macros) | Use. |
| `\se` | standard error (macro) | Use for standard errors. |
| `\pto`, `\dto` | convergence in probability and in distribution (macros) | Use for consistency and asymptotic normality. |
| `\iid`, `\Normal` | i.i.d. and normal distribution (macros) | Use. |
| `\R`, `\N` | real and natural numbers (macros) | Use `\R` only. |
| `\tr`, `\diag`, `\argmin`, `\indic` | trace, diagonal matrix, argmin, indicator (macros) | Use as registered. |

Local symbols (allowed; defined on the lesson where first used and never redefined): `X` design matrix (n × k), `y`, `\beta`
coefficient vector, `\varepsilon` error, `\hat\beta`, `e` residual vector, `H` the hat matrix (not a horizon), `P` a
projection (if used), `\sigma^2`, `\rho` the AR(1) coefficient of the predictor, `u` and `v` the two innovations of a predictive
system (L12), `\Gamma_j` the lag-j autocovariance (L09), `\lambda` the reliability ratio (L06), `G` the number of clusters, `L`
the Newey–West lag bound. `\rho` is not a registered symbol; the registry lists none.

NOTATION_REQUESTS: none (§12 Q3). Every symbol above is registered or local. No macro is requested.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson. Grades are the planned
grades; the verifier re-grades (BUILDER_RULES §2.2).

- **L01 `ols-estimator`.** The model in matrix form, the OLS criterion, the normal equations, the projection matrix H = X(X'X)^{-1}X'
  (T, derivation under A1). The residual is orthogonal to the columns of X (T). Lab: exact check on seeded integer data.
  Misconceptions: OLS requires a normal error (no); the residuals sum to zero only with an intercept (state it as T with the
  intercept column).
- **L02 `frisch-waugh-lovell-theorem`.** Partialling out: the coefficient of x₁ in the full regression equals the slope of the
  residual of y on the other regressors on the residual of x₁ on them (T, derivation from L01). Lab: exact `Fraction` equality.
  Misconception: partialling out changes the sample (it does not).
- **L03 `coefficient-of-determination`.** R² = 1 − RSS/TSS with an intercept; equals the squared correlation of y and ŷ (T).
  R² never falls when a regressor is added (T, from L01's projection property). Lab: the identity exactly. Where the canon breaks:
  R² is not a specification test. Misconception: a high R² means the coefficient is unbiased (no).
- **L04 `gauss-markov-theorem`.** Under A1 to A4 OLS has the smallest variance among linear unbiased estimators (T, the standard
  derivation: any other linear unbiased estimator has variance OLS plus a positive semidefinite matrix; the page proves it). Lab:
  Monte Carlo variance of OLS against the two-point slope on a fixed design (C, basis: lab). Where the canon breaks: heteroskedasticity
  (L08), dependence (L09), endogeneity (L05, L06). Misconception: unbiasedness needs normal errors (no).
- **L05 `omitted-variable-bias`.** With a relevant regressor omitted, the short-regression coefficient equals β₁ + β₂δ, where δ is the
  coefficient from regressing the omitted variable on the included ones (T, derivation). The sign table follows from δ and β₂
  (T). Lab: the identity checked exactly on the population design; the Monte Carlo bias printed (C). Uses `identification` (P0.1)
  as a plain link. Misconception: adding controls always reduces bias (no).
- **L06 `errors-in-variables`.** Under classical measurement error (the error is independent of the true regressor and of the
  equation error), the slope is attenuated by the reliability ratio λ = σ²_x/(σ²_x + σ²_u) (T, derivation under the stated
  assumptions). Lab: attenuation against λ on a large seeded design (C). Remedy outside S2: plain prose "an instrumental variable,
  developed later" (§4, D5). Shanken's correction is named at key level only (`shanken1992estimation`, §7.1). Misconception: measurement
  error in y biases the slope (no under the stated model; it inflates the variance).
- **L07 `ols-asymptotics`.** Under i.i.d. sampling, finite second moments and a positive definite Q, √n(β̂ − β) converges in distribution
  to a normal with covariance Q⁻¹ Ω Q⁻¹, where Ω = E[ε² x x'] under homoskedasticity reduces to σ² Q (T, derivation from LLN and CLT).
  Consistency of β̂ (T). The classical t interval's asymptotic validity (T under the stated model). Lab: coverage for n = 20, 80, 320
  under centred exponential errors (C). Uses M4 `law-of-large-numbers`, `central-limit-theorem` (closure), S1 `delta-method` (closure).
  Misconception: asymptotic normality needs normal errors (no).
- **L08 `heteroskedasticity-robust-standard-errors`.** The sandwich (X'X)⁻¹ (Σ e²ᵢ xᵢxᵢ') (X'X)⁻¹ (the HC0 form; the spec fixes HC0,
  §5.4); consistency of the meat under the fourth-moment assumption (T, derivation). The classical variance is correct only under
  homoskedasticity (T). Lab: classical against HC0 coverage under an error scale that depends on x (C). The estimator is named after
  White (1980); `white1980heteroskedastici` is cited at naming level (§2.1 item 3). Misconception: robust errors fix bias (no).
- **L09 `hac-standard-errors`.** The Newey–West meat with Bartlett weights 1 − j/(L+1) on the lag-j autocovariance sums (the
  formula is written in the lesson; the builder derives the weights from the stated construction). With L = 0 the estimator equals the
  HC0 meat exactly (T, identity). Positive semidefiniteness of the Bartlett-weighted meat is a derivation (T) or a labelled sketch
  naming the skipped steps (fixer-rules line 12). Consistency needs L to grow with n (Assumption; not proved here). Lab: lag-zero identity
  to 1e-12, and coverage under AR(1) errors (C). Remark: block resampling is an alternative, plain prose (§4, D10). Misconception:
  any lag choice gives a valid interval (no).
- **L10 `clustered-standard-errors`.** The cluster sandwich: the meat is the sum over clusters of the squared cluster scores (T,
  derivation under cluster-level independence). With within-cluster correlation, the observation-level meat is biased (T, shown
  by the lab's design). Lab: classical against cluster coverage under a planted intraclass correlation; the design effect printed
  as 1 + (m − 1)ρ_ic, with m the cluster size, stated as a derivation for equal sizes (T). Petersen (2009) is cited at paper level as
  the finance panel comparison (`petersen2008estimating`; no result stated unless read, §2.1 item 3). Misconception: clustering only
  matters when there are many clusters (the number of clusters matters for the reliability of the estimate; state it as a limit of the
  lab, C). The phrase "volatility clustering" is not used (§4, D8).
- **L11 `two-way-clustering`.** Definition: V = V_A + V_B − V_{A∩B} with V_A, V_B the one-way cluster variances and V_{A∩B} the one-way
  variance over the intersection cluster (plain definition, the formula the spec fixes). Identity: if A = B the formula equals V_A
  exactly (T). Lab: exact check on a seeded panel with firm and time effects; coverage (C). The claim that the two-way sum can be
  non-positive semidefinite is **not stated** unless a record is admitted (B3, §7.2); the lesson says so in one sentence. Misconception:
  two-way clustering is just clustering twice (the intersection term is subtracted).
- **L12 `stambaugh-bias`.** The predictive system y_{t+1} = α + β x_t + u_{t+1}, x_{t+1} = θ + ρ x_t + v_{t+1} with |ρ| < 1 (numbered
  Assumption, §2.1 item 6). The bias of the slope β̂ in finite samples with corr(u, v) ≠ 0 is derived to first order under the
  stated model (T as a derivation; the planner does not type the expression, the builder derives it and the lab checks its sign).
  The sign and size in the lab's design are C, basis: the lab (curriculum lab, `lab-S2-L12-1`, SIMULATED). Two-sided treatment (B-grade
  claims): Stambaugh (1999) is the source of the bias result (`stambaugh1999predictive`, naming level unless its abstract is read); the
  predictability debate is counter-evidence: `welch2007comprehensive`, `campbell2007predicting`, `cochrane2007dog` (each at naming
  level unless read). Where the canon breaks: the stable-AR(1) assumption, and the lab's single persistence value. Misconception: the
  bias vanishes with a large sample (it shrinks at a rate the lesson does not state; state only what the lab shows).

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- No lesson uses a term from S3 to S7 (stationarity, instrumental variables, GMM, panel fixed effects, time series models) as a
  concept; §4 lists the plain-prose words allowed.
- Every lesson states its assumptions as numbered Assumptions before the first Theorem, Proposition or Derivation (§2.1 item 6).

---

## 4. DAG problems (concepts that natural S2 content would use outside the closure)

Prerequisite closure of S2 (computed): **{CS1, M1, M2, M3, M4, P0.1, S0, S1}**, with 112 usable concepts (§0.1). Downstream status
below is computed (`tools/coursekit.py` `prerequisite_closure`, run this session): a module is **downstream** when its closure
contains S2, so none of its concepts can become a prerequisite of S2 without a cycle. Owners are from `curriculum/curriculum.json`
`concepts`.

| Ref | Concept (owner) | Downstream of S2? | Where natural S2 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `stationarity`, `unit-root` (S3) | yes (S3 prereqs `[S2]`, `01-foundations.yaml:701`) | L12: the predictor is a stable AR(1); the ρ → 1 boundary | Plain prose. The stability condition is numbered Assumption A(persist) in L12. No link. Cannot be a prerequisite (cycle). |
| D2 | `dickey-fuller-test`, `mean-reversion-half-life` (S3) | yes | L12 remark on near-unit-root predictors | Not used. L12 states only the ρ < 1 lab range. |
| D3 | `vector-autoregression` (S3) | yes | L12: the joint first-order system for (y, x) | Plain prose "two-equation first-order system". No link. |
| D4 | `autocorrelation-function` (S3) | yes | L09: residual autocovariances | Plain prose; symbol `\Gamma_j`. No link. |
| D5 | `instrumental-variables`, `weak-instruments` (S6) | yes | L06 remark: the remedy for errors-in-variables | Plain prose "an instrumental variable, developed later". No link. |
| D6 | `panel-fixed-effects` (S5) | yes | L10 and L11: the design's "firm effect" and "time effect" | Plain words in the design description. No estimator. No link. |
| D7 | `shanken-correction`, `generalized-method-of-moments` (S5) | yes | L06: Shanken correction named at key level | Key-only citation (`shanken1992estimation`, §7.1). No concept link. GMM not mentioned. |
| D8 | `volatility-clustering` (S4) | yes | name clash with "clustered" | The phrase "volatility clustering" is not used in S2. |
| D9 | `bias-variance-tradeoff` (QR3) | yes | L04 remark: biased estimators with lower variance | Plain prose. No link. |
| D10 | `stationary-bootstrap` (S7, downstream); `moving-block-bootstrap` (BK5, upstream) | S7 yes; BK5 no | L09 remark: block resampling as an alternative to Newey–West | Plain prose. BK5 as a prerequisite is not recommended (§12 Q6). |
| D11 | `out-of-sample-r-squared`, `dividend-price-regression` (AP5) | yes | L12 counter-evidence sentence | Plain prose, defined inside the sentence, no `<dfn>`. Not a concept link. |
| D12 | `linear-factor-model` (AP2) | no (upstream) | none planned | Not used. |
| D13 | `big-o-complexity` (CS2) | no | project runtime remark | Plain prose. |
| D14 | `cholesky-decomposition`, `ieee-754-floating-point`, `numerical-stability` (M8) | no | project solver and tolerance remarks | Plain prose. Do not name Cholesky, as M3 B4 required. Tolerances are stated as numbers. |
| D15 | Unregistered terms: heteroskedasticity, autocovariance, residual, hat matrix, endogeneity, exogeneity, multicollinearity, cluster, intraclass correlation, F-test, chi-squared distribution, Wald statistic, design effect | not concepts | the lessons | Plain `<dfn>` without `data-concept` where defined (§2.1 item 5). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§12 Q4 to Q6).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring, lines 1-12). An unlinked use of D1 to D14 passes the tool,
so the verifier reads every lesson for these words (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): autograded, ladder, spec, hours, grader design

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` requires the rung order, `:84-90` checks it)

Tier U: rungs 1 and 2 are full length (BLUEPRINT §4: the minimum applies from tier M).

1. **Rung 1, worked example** (`lab-S2-project-1`, SIMULATED): one fully solved, annotated run of the reference on one seeded
   instance (from `make_instance(0)`-shaped data generated inside the lab): the OLS fit, the classical and HC0 errors, the
   Bartlett weights for L = 1, the cluster sums. Each step has a "why" annotation. Title contains "worked example".
2. **Rung 2, completion** (`lab-S2-project-2`, `class="lab completion"`, SIMULATED): the same run with three blanks (`___`): the
   meat sum for HC0, the Bartlett weight, and the two-way combination V_A + V_B − V_{A∩B}. Graded instantly. Its twin is the completed
   solution; every page line equals the twin line or contains a blank (`tools/run_labs.py` docstring, FINAL-ARCHITECT-RULINGS 11).
   `check_projects.py:89-90` requires it.
3. **Rung 3, independent project** (autograded, §5.4): `inference_engine.py`, graded by `grader/test_project.py`. The
   coverage study is the function `coverage` (§5.4), not a memo. `lab-S2-project-3` is the rung-3 check: it prints the reference's
   values on the rung-1 instance so the student can compare their module on the same input.
4. **Rung 4, stretch** (optional, not graded, no ceiling): small-sample variants of the sandwich (HC2, HC3), or a comparison of
   cluster-robust and block-bootstrap intervals. Named only in plain prose (D10, §4). Not graded, so no tests.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** An analyst must compute regression inference by hand-built formulas: OLS coefficients, four kinds of standard errors,
  and the coverage of intervals built from them. The module must match the stated conventions exactly, because a different
  convention changes the numbers.
- **Inputs.** Generated instances from `grader/instance.py` (SIMULATED): a design matrix X (n × k, the first column is the intercept
  when the instance says so, otherwise the caller supplies X as given), a response y, a lag bound L (0 ≤ L ≤ n − 1), two cluster
  label lists, and the true coefficient for coverage. Values have two decimal places (exact `Fraction` conversion, §5.4 A4). No
  embedded dataset is read.
- **Required outputs.** The file `inference_engine.py` exposing the functions of §5.4.1 with the exact names and argument order. No
  printing and no mutation of arguments (BUILDER_RULES §5.3; the suite checks it).
- **Constraints.**
  - The conventions below are binding: the standard errors are square roots of the diagonal of the variance estimates.
  - A failing input raises `ValueError` only in the four cases named in §5.4.2. Every other invalid input is outside the spec.
  - Numerical tolerances: 1e-9 for coefficients and residual orthogonality; 1e-10 relative for standard errors (as the page states).
  - NumPy and SciPy are allowed (both vendored, `tools/vendor_spec.yaml:59`); the standard library is allowed.
  - Each test finishes in under 5 s in Pyodide; the suite in under 60 s (`tools/run_graders.py:40`, SUITE_LIMIT_S).
- **Conventions (the page states each as a formula):**
  - classical: σ̂² = RSS/(n − k); Var(β̂) = σ̂² (X'X)⁻¹.
  - White (HC0): (X'X)⁻¹ (Σᵢ eᵢ² xᵢ xᵢ') (X'X)⁻¹; no degrees-of-freedom factor.
  - Newey–West: the HC0 meat plus Σ_{j=1}^{L} (1 − j/(L+1)) Σ_{t=j+1}^{n} eₜ eₜ₋ⱼ (xₜ xₜ₋ⱼ' + xₜ₋ⱼ xₜ'), sandwiched the same way; no
    degrees-of-freedom factor.
  - Cluster (CR0): Σ_g s_g s_g' with s_g = Σ_{i∈g} eᵢ xᵢ, sandwiched; no degrees-of-freedom factor; G ≥ 1.
  - Two-way: V_A + V_B − V_{A∩B} with each term a CR0 variance over the stated grouping.
  - Coverage: a nominal 95 percent two-sided interval β̂ⱼ ± t_critical(n − k) × se_j for every method, the same critical value for
    all methods; a draw is covered when the true coefficient lies in the interval.
  - t_critical(df): the 97.5th percentile of the t distribution with df degrees of freedom.
- **Grading.** Autograder (`tools/check_projects.py:38, 41-45`: the spec's grading entry must contain the word "autograder").
  No rubric and no exemplars (the curriculum grades by autograder only, `01-foundations.yaml:696`).
- **Reading list.** `ol.reading-list` with `data-cite` on each item: `white1980heteroskedastici`, `newey1987simple`,
  `petersen2008estimating`, `stambaugh1999predictive` (registry keys only; §7.1). `angrist2009mostly` optional, book level, no locator.

### 5.3 Time budget (`<table id="hours">`; sums to 36 h; each row has a one-line rationale; `tools/check_projects.py:107-120`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate one run) | 2 | One seeded instance, each step annotated |
| Rung 2, completion problem (three blanks, instant check) | 3 | The meat sum, the Bartlett weight and the two-way combination |
| OLS, classical and HC0 errors (rung 3, part 1) | 6 | Normal equations, degrees-of-freedom factor, the sandwich |
| Newey–West with Bartlett weights (rung 3, part 2) | 6 | Lag-zero identity to HC0, lag-L direct sum, the lag bound |
| Cluster and two-way errors (rung 3, part 3) | 6 | Cluster sums, the identical-clustering identity, V_A + V_B − V_{A∩B} |
| Coverage and the critical value (rung 3, part 4) | 7 | t_critical from first principles, coverage on given draws |
| Self-check against the suite and the conventions page | 6 | Run the suite; confirm each convention against its test |
| **Total** | **36** | Equals `data-hours-project` on the hub |

Planner estimates: the component times were set by the planner from the steps each component needs (no estimate is typed from a
source). The verifier re-estimates them (VERIFIER §2.6, 30 percent tolerance).

### 5.4 Grader design (`grader/`, Builder E; BUILDER_RULES §5.3; FINAL-ARCHITECT-RULINGS 9, 10, 22; fixer-rules line 19)

**5.4.1 Frozen interface (proposal; the architect freezes it, §12 Q16).** Module `inference_engine.py` (student file, data-solution):

- `ols_beta(X: list[list[float]], y: list[float]) -> list[float]`: β̂ with full column rank X.
- `se_classical(X, y) -> list[float]`: the square roots of the diagonal of σ̂² (X'X)⁻¹ with the n − k factor.
- `se_white(X, y) -> list[float]`: HC0.
- `se_newey_west(X, y, lags: int) -> list[float]`: Bartlett-weighted HAC.
- `se_cluster(X, y, cluster: list) -> list[float]`: CR0 with one label per row.
- `se_two_way(X, y, cluster_a: list, cluster_b: list) -> list[float]`: V_A + V_B − V_{A∩B}.
- `t_critical(df: int) -> float`: the 97.5th percentile of the t distribution.
- `coverage(draws: list[dict], method: str, column: int) -> float`: the covered share of draws for `method` in
  {"classical", "white", "newey_west", "cluster"}; each draw carries X, y, the true coefficient vector, lags and cluster labels.
  Coverage is the only function that takes draws, so the draws come from `instance.py` and the rates are deterministic.

**5.4.2 The ValueError conditions the page names (the only ones a test may assert as ValueError; fixer-rules line 19):**
(E1) X does not have full column rank; (E2) n ≤ k; (E3) a length mismatch between y, X rows and any label list; (E4) lags is not
an integer in [0, n − 1]. Every other invalid input is outside the spec: no test asserts an exception type for it. Each condition
gets its own isolated test in both directions: E2 accepts n = k + 1 and rejects n = k; E4 accepts lags = n − 1 and rejects lags = n
and lags = −1; E1 rejects a duplicated column and accepts the same design with the column removed.

**5.4.3 Instances (`grader/instance.py`, SIMULATED).** `make_instance(seed: int) -> dict[str, Any]`: deterministic; generates
n in [40, 120], k in {2, 3, 4} (intercept included), two-decimal regressors and responses (exact in `Fraction`), a lag bound
L in {0, …, 4} with L < n, cluster labels with G in [8, 20] for both groupings, and a heteroskedastic, autocorrelated or clustered
error design chosen by seed. Every instance is valid under the spec. Seeds 0 to 49 give materially different designs: the
coefficient vectors and the standard errors change, not just the labels (BUILDER_RULES §5.3). `make_instance` also gives the coverage
draws (R = 100 replications per instance; §12 Q10).

**5.4.4 Reference and tests (`grader/reference.py`, `grader/test_project.py`).** The reference solves each function by the
conventions of §5.2 and passes all tests on seeds 0 to 49. The tests check properties and numbers, not one algorithm's output:
- OLS: X'e ≈ 0 to 1e-9; β̂ solves the normal equations to 1e-9 (a property of the output, not of the algorithm).
- Classical: equals the direct formula with n − k (the test computes the sum itself).
- HC0: equals a direct sum over observations computed in the test to 1e-10 relative.
- Newey–West: lags = 0 equals HC0 to 1e-10; lags = L equals a direct sum with Bartlett weights computed in the test; the matrix is
  symmetric; the meat's diagonal is nonnegative.
- Cluster: equals a direct sum over clusters computed in the test; on a design with planted within-cluster correlation it differs
  from HC0 by more than 1e-6 (the test checks the difference is nonzero, not its value).
- Two-way: identical clusterings equal the one-way cluster variance to 1e-10; the formula equals the direct sum on a seeded case.
- t_critical: equals scipy.stats.t.ppf(0.975, df) to 1e-9 for df in {1, 2, 5, 30, 100}, with the reference using the same
  definition; no hard-coded table.
- coverage: equals the reference rate on each seed's draws exactly (the draws are identical). No test asserts a particular coverage
  level: the designs include misspecified cases whose coverage differs from 95 percent by design, and L07 to L12 show it. The
  binomial standard error sqrt(p(1−p)/R) with R = 100 is printed by the labs, not tested here.
- Edge cases: k = 1 (intercept only) for all methods; G = 1 allowed; L = 0 for Newey–West.
- Failure messages name the violated property and the convention, and never print the expected value (`__tracebackhide__`).
- Collect-only count: `pytest --collect-only -q grader/test_project.py` count is quoted on the project page (fixer-rules line 19).
- The starter (`grader/starter.py`) fails the suite (`tools/run_graders.py` requires it, lines 162-166).

**5.4.5 Panel and paths.** The grader panel (BUILDER_RULES §5.3; precedent `course/modules/M/M3/project.html:276`):
`<section class="grader-panel" id="grader" data-unit="S2" data-grader="grader/" data-suite="test_project.py" data-support="instance.py"
data-solution="inference_engine.py" data-starter="starter.py" data-packages="numpy scipy">`. The `data-packages` value
format for two packages is NOT VERIFIED (the page_smoke parser at `tools/page_smoke.py:241` reads a list of packages per lab, and the
panel's parser was not read); a builder confirms it with `tools/run_graders.py` before writing the page.

**5.4.6 Mutants (ten student errors; `ledgers/S2/mutants/`, one file each, the first docstring line names the error;
FINAL-ARCHITECT-RULINGS 9, 19; `tools/mutate_graders.py:1-14`).** Each is a single-change copy of the reference and violates a
behaviour the page states:

| # | Student error (first docstring line) | Stated behaviour it violates | Test that kills it (expected) |
|---|---|---|---|
| m01 | `se_white` returns the classical variance (homoskedasticity assumed) | HC0 sandwich (§5.2) | HC0 direct-sum test on a heteroskedastic instance |
| m02 | `se_white` uses the absolute residual in the meat | the squared residual in HC0 | HC0 direct-sum test |
| m03 | Newey–West uses uniform weights (no Bartlett taper) | Bartlett weights (§5.2) | Newey–West direct-sum test with L ≥ 1 |
| m04 | Newey–West sums lags 1 to L + 1 | the lag bound L | lags = 0 identity and lags = L direct-sum test |
| m05 | cluster variance treats each observation as a cluster | CR0 over clusters (§5.2) | cluster direct-sum test and the planted-correlation test |
| m06 | two-way adds the intersection term instead of subtracting it | V_A + V_B − V_{A∩B} (§5.2) | identical-clustering identity test |
| m07 | `ols_beta` uses the transpose of X in the bread | the normal equations (§5.4.4) | OLS property test on n ≠ k instances |
| m08 | classical uses RSS/n instead of RSS/(n − k) | the degrees-of-freedom factor (§5.2) | classical direct-formula test (difference > 1e-10 for n − k ≤ 100) |
| m09 | `t_critical` returns the normal 1.96 for every df | the t critical value (§5.2) | t_critical equals scipy.stats.t.ppf to 1e-9 for df in {1, 2, 5, 30} |
| m10 | `coverage` returns the reference's answer for seed 0 by matching the first design | the coverage definition (§5.2) | coverage equals reference on a non-zero seed's draws |

None of m01 to m10 is equivalent under the stated conventions. If a verifier writes a mutant that differs only within a stated
tolerance, it goes to `ledgers/S2/equivalent/` with a README proof (FINAL-ARCHITECT-RULINGS 9, 22, 25), not to `mutants/`.

**5.4.7 Five correct alternatives (verifier-written, different styles, all must pass seeds 0 to 49; FINAL-ARCHITECT-RULINGS 10):**
- A1 NumPy normal equations with `numpy.linalg.solve`; vectorised sums.
- A2 QR-based: `numpy.linalg.qr` for β̂ and the bread, a different numerical path.
- A3 pure Python with Gaussian elimination and partial pivoting; no NumPy.
- A4 exact arithmetic: `fractions.Fraction` for X'X, X'y and every meat sum on the two-decimal inputs, converted to float at return.
  Runtime is the risk: if A4 cannot finish the suite under 60 s, the page's R and n bounds are the lever (§12 Q10), not the tests.
- A5 explicit observation loops for every sum; scipy.stats.t for t_critical.

Failure to pass any alternative is a finding against the spec or the tests (VERIFIER §2.6), not an edit to the alternative.

**5.4.8 Hours of the grader work.** Included in the 36 h budget (§5.3, rows 3 to 6).

---

## 6. Real-data policy

- **No real data.** The curriculum names no dataset for S2 (`01-foundations.yaml:688`; `:689-696`). No lab and no project input reads a
  snapshot. No `data-files` attribute is used on any S2 lab. No MANIFEST entry is added. No DATA_REQUEST is needed (N2, §0.3).
- **Simulated throughout.** Every lab and the project are SIMULATED and labelled (§2.2). The planner has not claimed any empirical
  magnitude from real finance data. Predictive-regression bias in real data is therefore **not** shown by S2; L12 says so in one
  sentence, and the lab's result is about its design only (fixer-rules line 7; FINAL-ARCHITECT-RULINGS 13).
- **Honest gap (stated on the hub and in L12):** the page does not show the size of Stambaugh bias in observed return data; the
  predictability literature is cited as counter-evidence at naming level only, until its abstracts are read.
- **Rung 4 real-data variant** is not planned (§12 Q8). Candidate embedded series (BLUEPRINT §5.3) are not cleared for any S2 use.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in S2 |
|---|---|---|---|
| `white1980heteroskedastici` | Econometrica, volume 48, issue 4, print year 1980, DOI 10.2307/1912934 (`references/references.json:22978`); `used_by: ["S2"]` | verified; source string matches `01-foundations.yaml:684` | L08 naming (paper level); reading list |
| `newey1987simple` | Econometrica, volume 55, issue 3, print year 1987, DOI 10.2307/1913610 (`:18060`); `used_by: ["S2", "S7"]` | verified; matches `:685` | L09 naming (paper level); reading list |
| `petersen2008estimating` | Review of Financial Studies, volume 22, issue 1, print year 2009, online year 2008, DOI 10.1093/rfs/hhn053 (`:19015`); `used_by: ["S2"]` | verified; matches `:686` on print year 2009 (N1) | L10 and L11 naming (paper level); reading list |
| `stambaugh1999predictive` | Journal of Financial Economics, volume 54, issue 3, 1999, DOI 10.1016/s0304-405x(99)00041-0 (`:21186`); `used_by: ["S2"]` | verified; matches `:687` | L12 bias result (naming unless read); reading list |
| `welch2007comprehensive` | Review of Financial Studies, volume 21, issue 4, pages 1455–1508, DOI 10.1093/rfs/hhm014 (`:22896`); `used_by: ["AP5"]` | verified | L12 counter-evidence (naming unless read) |
| `campbell2007predicting` | Review of Financial Studies, volume 21, issue 4, pages 1509–1531 (`:4566`); `used_by: ["AP5"]` | verified | L12 counter-evidence (naming unless read) |
| `cochrane2007dog` | Review of Financial Studies, volume 21, issue 4 (`:5632`); `used_by: ["AP5"]` | verified | L12 defence of predictability (naming unless read) |
| `angrist2009mostly` | Princeton University Press book, print year 2009 (`:853`); `used_by: ["S6"]` | verified (book) | optional, book level, no locator, for OLS interpretation in L01 |
| `shanken1992estimation` | Review of Financial Studies, volume 5, issue 1, 1992 (`:20502`); `used_by: ["S5"]` | verified | L06 naming only (errors-in-variables correction in beta-pricing), no claim |

Not curriculum-listed but used by S2: `welch2007comprehensive`, `campbell2007predicting`, `cochrane2007dog` (L12 counter-evidence),
`angrist2009mostly` (optional), `shanken1992estimation` (L06). `used_by` is not edited (the check does not require it:
`tools/check_pages.py` checks key existence and verification; M3 precedent, §12 Q12). The four curriculum sources resolve to four keys
with matching volume, issue and print year (N1); no DAG-style correction is needed.

### 7.2 REFERENCE_REQUESTS (lead only; no bibliographic record typed by the planner)

- {doi: null, authors: "not typed (lead only)", year: "not typed", title: "two-way and multiway clustered standard errors, the variance
  formula of L11 (lead only; record not typed)", venue: "not typed", needed_for: "L11 claim that the two-way sum can be non-positive
  semidefinite; any B- or C-graded claim about two-way inference", confidence: "the need is certain (`01-foundations.yaml:680`); no record
  is identified by this planner"}
- {doi: null, authors: "errors-in-variables literature (lead only; no author typed)", year: "not typed", title: "measurement-error models
  for regression (lead only; record not typed)", venue: "not typed", needed_for: "L06 counter-evidence and a textbook reference for the
  attenuation result (the derivation is T without it)", confidence: "the need is moderate; the derivation does not depend on it"}
- {doi: null, authors: "Frisch–Waugh–Lovell originals (names as in `01-foundations.yaml:672`; no record typed)", year: "not typed", title:
  "the original partialling-out papers (lead only)", venue: "not typed", needed_for: "historical attribution in L02 only; the theorem is
  derived on the page", confidence: "low need; optional"}
- {doi: null, authors: "not typed (lead only)", year: "not typed", title: "bandwidth choice for HAC estimators (lead only)", venue:
  "not typed", needed_for: "only if L09 states a bandwidth rule; the plan does not", confidence: "optional; default is no rule"}
- {doi: null, authors: "not typed (lead only)", year: "not typed", title: "small-sample and few-cluster inference for cluster-robust
  standard errors (lead only)", venue: "not typed", needed_for: "counter-evidence for any claim in L10 or L11 about the number of clusters",
  confidence: "the need is certain if such a claim is made; the default is no such claim"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until
resolved, the lessons teach the models with derivations and name the literature only as "the literature on X" with no claim, or
omit the claim.

---

## 8. Atlas milestone

None. No Atlas entry names S2 (§0.1), and the S2 project has no `atlas:` key (`01-foundations.yaml:689-696`). No
`atlas/S2.contract.md` is needed. `atlas/` holds `A8.contract.md` and `A15.contract.md` only (planner `ls`). The `data-solution` is
unit-local, not `atlas/`, as M3 did (`course/modules/M/M3/project.html:276`).

---

## 9. Cards builder (Builder F, after A to D)

- `course/modules/S/S2/cards.json`, ids `S2-c001` upward (non-sequential ids are not defects: FINAL-ARCHITECT-RULINGS 2), `lesson`
  in L01 to L12, one card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7).
- Grade T for every derived result, with `"basis"` naming the lab or derivation, for example `"basis": "Lab 2, Derivation 1 (exact)"`.
- Cite a registry key only for a naming or empirical claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED lab result name the SIMULATED lab in `basis` and carry grade C (FINAL-ARCHITECT-RULINGS 13: a card and the
  key-results row it mirrors carry the same grade and basis).
- `tools/check_pages.py` `check_cards` checks the id prefix, the lesson existence, the grades and the registry keys
  (`tools/check_pages.py:366-400`).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit S2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit S2
.venv/bin/python tools/check_projects.py --unit S2
.venv/bin/python tools/run_labs.py --unit S2               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/S/S2/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/S/S2/L02.html --refresh lab-S2-L02-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit S2 --seeds 0-49                               # Builder E, grader
.venv/bin/ruff check tests/labs/S2 course/modules/S/S2/grader && .venv/bin/ruff format --check tests/labs/S2 course/modules/S/S2/grader
.venv/bin/mypy tests/labs/S2                               # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit S2 --seeds 0-9` (ten mutants, §5.4.6),
`.venv/bin/python tools/page_smoke.py --unit S2` (timing-sensitive; not run by builders), and
`.venv/bin/python tools/verify_refs.py --unit S2` (the unit ledger's registry run, VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. The full gate is one run before a push, not per edit (user policy).

Flag checks: `tools/check_pages.py`, `tools/check_dag.py`, `tools/check_projects.py`, `tools/run_labs.py` and `tools/embed_labs.py`
accept `--unit` (or the page flags shown); `tools/run_graders.py` and `tools/mutate_graders.py` accept `--unit` and `--seeds`
(`tools/mutate_graders.py:1-14` usage line). The planner did not execute the builder commands; only the coursekit closure and the
concept owners were run (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone** (§8). `check_projects.py` skips the contract check (`tools/check_projects.py:144-146`).
2. **No debate.** S2 has no `debate:` key (`01-foundations.yaml:661-696`), so `check_pages.py` does not require a debate brief. The
   predictability and bias claims are contested, so the two-sided rule (BUILDER_RULES §2.5) applies anyway (L12).
3. **Autograder-only grading.** No rubric and no exemplars. `check_projects.py` runs the rubric checks only when grading is `rubric` or
   `both` (`tools/check_projects.py:138-139`). The spec's grading entry must name the autograder (`:38`, `:41-45`).
4. **Rung 2 must be graded instantly.** `check_projects.py:89-90` accepts a completion lab or a quiz. The plan uses a completion lab.
5. **One curriculum lab, twelve labs.** The curriculum names one lab (`01-foundations.yaml:688`). BUILDER_RULES §3.4 requires a numerical
   check per key formula; the plan adds one lab per lesson (E5 and M3 precedent) and makes L12's lab the curriculum lab.
6. **S1 is not built**, so S1 concepts link through `concepts.html` anchors only (no hub link). M3 is built (`course/modules/M/M3/`).
7. **`check_dag.py` sees linked uses only** (`tools/check_dag.py` docstring). The plain-prose words in §4 pass the tool; the verifier reads
   for them.
8. **Statsmodels** is not in the vendored Pyodide package list (`tools/vendor_spec.yaml:59`); B1.
9. **`data-packages` with two packages** is NOT VERIFIED for the panel parser (§5.4.5).
10. **Labs are stdlib-only** (§2.2), so no lab depends on NumPy or SciPy. The project depends on NumPy and SciPy through the panel.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **B1, statsmodels.** RECOMMENDED: accept the default: validation by exact closed forms and by the five independent alternatives
   (§5.4.7). Ask for a curriculum wording change at `01-foundations.yaml:693` (the builders may not edit it). Alternative: vendor
   statsmodels after its Pyodide availability is verified (not verified now).
2. **Lesson count and hours.** RECOMMENDED: 12 lessons × 7 h and a 36 h project (30 percent; §0.2, §1). Alternatives inside the rules:
   10 lessons × 8 h with a 40 h project (33 percent), or 11 lessons × 7 h with a 43 h project (36 percent). The 12-lesson split gives
   each of Builders A to D three lessons and gives E the project.
3. **Notation.** RECOMMENDED: `n` for sample size, `T` never used (`notation/notation.json:112-115`), `\Gamma_j` for autocovariances,
   `\pto` for plims, no NOTATION_REQUESTS (§2.3).
4. **B2, downstream concepts (D1 to D8).** RECOMMENDED: plain prose with no link, as §4. A prerequisite is impossible for every concept
   in S3 to S7, because each of those modules lists S2 in its closure (§0.3 B2).
5. **D9 to D11 (QR3, BK5, AP5 words).** RECOMMENDED: plain prose; no prerequisite changes.
6. **D12 to D14 (AP2, CS2, M8).** RECOMMENDED: plain prose; no prerequisite changes. An M8 prerequisite would not create a cycle (M8 is not
   downstream of S2) but adds closure weight for three remarks; not recommended.
7. **Scope.** RECOMMENDED: confirm S2's scope: the classical linear model under A1 to A4 and its named extensions (robust, HAC, cluster,
   two-way); no nonlinear models, no instrumental variables, no GMM, no time-series models (these are S3, S5, S6).
8. **Real-data variant.** RECOMMENDED: none (§6). Confirm.
9. **Two-way non-PSD behaviour (B3).** RECOMMENDED: the spec states the raw formula; the grader tests the formula only; the page does not
   claim the result can be non-positive semidefinite; no test asserts a behaviour on that case.
10. **Coverage study size and time.** RECOMMENDED: R = 100 replications per instance; the coverage tests compare to the reference on the
    same draws. If A4 (exact arithmetic) cannot finish the suite under 60 s, the lever is the instance bound (n ≤ 60 for every instance),
    not a shorter seed range; the verifier reports the measured time. Confirm.
11. **Labs stdlib-only.** RECOMMENDED: yes (E5 precedent). NumPy only in the project.
12. **Registry citations and `used_by`.** RECOMMENDED: cite the eight keys of §7.1 without editing `used_by` (M3 Q9 precedent). Builders
    read abstracts out of band and record them in `plans/S2-open-items.md`; where an abstract is not read, the sentence is a naming
    sentence only (ruling 39 precedent).
13. **Counter-evidence.** RECOMMENDED: name `welch2007comprehensive`, `campbell2007predicting` and `cochrane2007dog` as the two-sided
    counter-evidence in L12, once their abstracts are read. Confirm.
14. **Curriculum lab placement.** RECOMMENDED: the curriculum lab is `lab-S2-L12-1` (the Stambaugh design) and not L01, because the
    named lab is about the Stambaugh bias (`01-foundations.yaml:688`).
15. **Named ValueError list.** RECOMMENDED: exactly E1 to E4 of §5.4.2; no other exception type is asserted by any test.
16. **Solution file and frozen interface.** RECOMMENDED: `inference_engine.py` and the eight signatures of §5.4.1. The architect freezes them.
17. **Figures.** RECOMMENDED: none (E5 precedent: no live figures, no new JS kernel). Confirm.
18. **Gauss–Markov and the other derivations.** RECOMMENDED: T with the page's own proof; no source needed (§3, L04). Confirm.
19. **Glossary.** RECOMMENDED: the unregistered terms of §4 D15 are plain `<dfn>` with no `data-concept`; no GLOSSARY_REQUESTS.
20. **Hub placement quiz.** RECOMMENDED: at least two `data-skill` items test what rungs 1 and 2 teach (`tools/check_pages.py:353`), and the
    other items test the closure concepts (M3, M4, S1) as BLUEPRINT §5.1 and BUILDER_RULES §5.1 require.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L03, L04 to L06, L07 to L09, L10 to L12, and the project (autograder
   and the blind mutant and alternative runs). The project verifier writes ten mutants (or confirms the ten of §5.4.6) and runs the
   five alternatives on seeds 0 to 49. Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/S2.verification.json`, with slice fragments under `ledgers/S2/` and verifier scripts under `ledgers/S2/scripts/`
   (VERIFIER §3; the fragment convention of FINAL-ARCHITECT-RULINGS 30). Mutants in `ledgers/S2/mutants/`; equivalents, if any, in
   `ledgers/S2/equivalent/` with a README (FINAL-ARCHITECT-RULINGS 9).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 to B3 must be resolved or
   named as honest gaps first. Merging and pushing are separate acts (user policy).

Honest gaps the pages must state (planner's list, §0 to §7): B1 (statsmodels not validated in the browser unless §12 Q1 is changed);
the two-way non-PSD question (B3); the Stambaugh magnitude in observed data (no real data, §6); errors-in-variables and multiway
clustering literature (no records, §7.2); registry records lack abstracts, so unread papers are naming sentences only (§2.1 item 3).

Architect decisions: pending (§12). This plan is the planner's proposal.

---

## Could not establish (planner)

- Whether Pyodide 314.0.7 ships statsmodels (not in the repository; the Pyodide lock was not read).
- Whether the Bartlett weights and the HC0 and CR0 formulas of §5.2 match the papers' constructions: the planner did not read
  Newey–West (1987), White (1980) or Petersen (2009). They are conventions the spec defines; no lesson attributes them beyond naming.
- The `data-packages` value format for two packages in the panel parser (not read).
- The text of the abstracts of the cited records (the registry holds none; no paper was read).
- The number of usable concepts computed by `tools/coursekit.py` in the exact sense of the render tool; the planner's figure of 112
  is the sum of `introduces` over the closure modules.
