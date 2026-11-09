# S3 build plan: Time Series (2026-11-09)

Unit: **S3 · Time Series** · tier M · 130 h · prerequisite S2 (only) · no Atlas milestone · no debate key · grading `both`
(autograder and rubric) · output directory `course/modules/S/S3/` (part code `S`) · lab twins `tests/labs/S3/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to E, then F for
cards, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Structure template: `plans/E5-build-plan.md`, sections 0 to 13, copied in order and adapted to S3. Nearest built prerequisite
plan: `plans/M3-build-plan.md` (M3 is a direct prerequisite of S2, and S2 is S3's only direct prerequisite; M3 is built at
`course/modules/M/M3/`). Closest built analogue for grading `both` with a grader and a rubric: S7 (`course/modules/S/S7/`,
`grader/`, `plans/S7-closure-plan.md`).

Evidence convention: every statement about the curriculum, the registry, the notation registry or a data file cites
`file:line` read during planning. Statements computed with the repository tools are marked "planner run": the only tool
functions used were `tools/coursekit.py` `prerequisite_closure`, `unit`, `concept_owner` (run through `.venv/bin/python -I`).
Anything not in the curriculum or the registry is marked **NOT IN CURRICULUM** or **NOT IN REGISTRY**.

**Status: no hard blocker. Seven decisions (section 12, Q1 to Q7) are needed before the builders start. The registry gaps
are REFERENCE_REQUESTS (section 7.2) and are honest gaps, not blockers.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| S3 id `S3`, title "Time Series" | `curriculum/01-foundations.yaml:697-698`; `curriculum/curriculum.json:6995` (JSON row matches the YAML) |
| Tier `M`, hours `130` | `curriculum/01-foundations.yaml:699-700` |
| Prereqs `[S2]` (only) | `curriculum/01-foundations.yaml:701` |
| Core: "Stationarity, ARMA, Wold, unit roots, spurious regression, cointegration, VARs and identification, state space and the Kalman filter, Markov switching." | `curriculum/01-foundations.yaml:702-704` |
| `introduces`: 16 concepts (list in section 1) | `curriculum/01-foundations.yaml:705-721` |
| Sources: seven free-text strings (Hamilton 1994 book; Dickey & Fuller 1979; Granger & Newbold 1974; Engle & Granger 1987; Johansen 1991; Sims 1980; Hamilton 1989) | `curriculum/01-foundations.yaml:722-729` |
| Lab: "Spurious-regression generator." | `curriculum/01-foundations.yaml:730` |
| Project "Pairs-trading audit"; brief: "Test claimed cointegrated pairs on open data with correct critical values, measure half-life stability out of sample, and show how many pairs survive."; deliverable "Analysis plus verdict memo."; grading `both` | `curriculum/01-foundations.yaml:731-737` (brief 733-735, deliverable 736, grading 737) |
| No `debate:` key and no `atlas:` key on S3 | `curriculum/01-foundations.yaml:697-737` (absent) |
| No Atlas entry names S3 (Atlas entries name CS3 for A2 "Data layer" and MS3 for A10; none names S3) | `curriculum/curriculum.json` `atlas` array (planner read) |
| S3 is a direct prerequisite of S4, S5, S7, AP5, CR3, E6, F7, FI3, GM1, X1 (downstream) | planner run over `curriculum/curriculum.json` `parts[].modules[].prereqs` |
| S3 is in the studio STUDIO-S requires list `[S2, S3, S7]` | `curriculum/01-foundations.yaml:576` |
| S3 is in the Master's credential requires list and in the Financial Econometrics course map | `curriculum/meta.yaml:98`, `curriculum/meta.yaml:105` |
| S3 is also in the "First-year sequence" group (Econometrics I-II) and the Quantitative Methods topic | `curriculum/meta.yaml:131`, `curriculum/meta.yaml:154` (grouping only; no action, see section 11) |
| Prerequisite closure of S3 (planner run): **{CS1, M1, M2, M3, M4, P0.1, S0, S1, S2}**; 124 usable concepts in the closure (sum of `introduces` over the nine units) | planner run, `tools/coursekit.py` `prerequisite_closure("S3")` |
| Built status of the closure: M1, M2, M3, M4 are built; S0, S1, S2, CS1, P0.1 are NOT built (no `course/modules/S/S0..S2`, no `CS1`) | `ls course/modules` (planner run); `tools/coursekit.py` `built_units` |
| S7 (built) lists S3 as a prerequisite and cites three S3 concepts with links | `curriculum/curriculum.json` (S7 prereqs `[S1, S2, S3]`); `course/modules/S/S7/index.html:69` (links `stationarity`, `autocorrelation-function`, `arma-model`); `course/modules/S/S7/L04.html:130` (AR(1) with coefficient \(\phi\), innovations \(e_t\)) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 130 h (`curriculum/01-foundations.yaml:700`). The tool rules (checked by reading `tools/check_pages.py`):

- lesson `data-hours` 6 to 12 (`tools/check_pages.py:219-227`, the hours read at line 221 and the message at line 225);
- hub `data-hours-lessons + data-hours-project = 130` (`tools/check_pages.py:325-342`, the hub's `<main>` read at 332-335);
- project share 10 to 40% of 130, i.e. 13 to 52 h (BUILDER_RULES 4.3, `BUILDER_RULES.md:168-173`);
- lessons sum to the hub's lessons figure (same hub check).

Chosen split: **10 lessons × 10 h = 100 h; project 30 h (23.1%)**. 100 + 30 = 130. Feasible. No STOP condition on hours.
The 16 concepts are spread over 10 lessons with no lesson left without a concept (section 1).

### 0.3 Blocking issues and what is not blocking

**No hard blocker.** The items below need the architect's decision (section 12) before the builders start.

- **D-S3-1. The project's data.** The curriculum says "open data" (`curriculum/01-foundations.yaml:734`). The only embedded
  redistributable series are the Federal Reserve H.10 and H.15 snapshots (`tools/data_sources.yaml:19-116`). The H.10
  daily FX series `fx_daily` is cleared for embedding (licence quote at `tools/data_sources.yaml:23-26`; the planner did not
  open `licence_url`, and the verifier must, BUILDER_RULES 6.6 step 1). It is used as the project's real data (section 6).
  Decision Q1.
- **D-S3-2. Claimed pairs.** The brief says "claimed cointegrated pairs" (`curriculum/01-foundations.yaml:734`), but no
  published claim about any pair is in the registry, and none is named by the curriculum. Using invented claims would be a
  fabricated-data defect (BUILDER_RULES 1.7). The default is the full 15-pair universe of the six embedded currencies, and
  the page says that no published claim is tested. Decision Q2.
- **D-S3-3. Critical values.** The brief asks for "correct critical values" (`curriculum/01-foundations.yaml:734`). The
  Engle-Granger critical values are not in the registry (no MacKinnon record; section 7.2, R3). The default is that
  critical values are precomputed by a seeded Monte Carlo at build time, stated on the page, and supplied to the autograder
  inside each instance. Decision Q3.
- **D-S3-4. Sources not in the registry.** Several results the core needs (Kalman filter original, the general Wold theorem,
  Phillips's spurious-regression asymptotics, Engle-Granger critical values, structural VAR identification beyond Cholesky,
  pairs-trading evidence) have no record. Each becomes a REFERENCE_REQUEST (lead only). Until resolved the lessons teach the
  models by derivation or by lab (grade T or C with the lab named) and state the gap (section 7.2).
- **D-S3-5. The prerequisite S2 is unbuilt, and S7 is built.** S7 (built) requires S3, which is not built, and S7 pages
  already cite S3 concepts (section 0.1). This is a build-order fact, not a defect of S3. It is recorded for the architect
  (Q15).

Non-blocking:

- **B4-S3. Hamilton 1994 record.** The record `hamilton1994time` (`references/references.json:11346`) has type
  `edited-book` and `years` [1994, 2020]. Cite the key at book level, with no year or edition typed in prose.
- **Dickey-Fuller issue string.** The curriculum says "JASA 74(366)" (`curriculum/01-foundations.yaml:724`); the record
  `dickey1979distribution` (`references/references.json:6895`) has issue "366a" and pages 427-431. Cite the key only.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

10 lessons × 10 h = 100 h; project 30 h; total 130 h. The 16 concepts of `curriculum/01-foundations.yaml:706-721` are each
introduced in exactly one row. Concept counts per row: 2+2+2+1+1+2+2+1+2+1 = 16.

| Lesson | Title (fixed; the hub copies it) | Concepts it defines (`<dfn>`, `introduces`) | Lab twin (`tests/labs/S3/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Stationarity and the autocorrelation function | `stationarity`, `autocorrelation-function` | `lab-S3-L01-1`: sample ACF of a seeded AR(1) against \(\phi^{h}\) (SIMULATED) | 10 | Builder A |
| L02 | ARMA models and the Wold decomposition | `arma-model`, `wold-decomposition` | `lab-S3-L02-1`: ARMA(1,1) autocovariances from the closed form against simulation; root conditions (SIMULATED) | 10 | Builder A |
| L03 | Unit roots and the Dickey-Fuller test | `unit-root`, `dickey-fuller-test` | `lab-S3-L03-1`: Dickey-Fuller t-statistic under a unit root, empirical 5% quantile (SIMULATED) | 10 | Builder A |
| L04 | Spurious regression | `spurious-regression` | `lab-S3-L04-1` (**the curriculum lab**, `curriculum/01-foundations.yaml:730`): spurious-regression generator on independent random walks (SIMULATED) | 10 | Builder B |
| L05 | Cointegration and error correction | `cointegration` | `lab-S3-L05-1`: a seeded cointegrated pair; stationarity of the spread; the error-correction coefficient (SIMULATED) | 10 | Builder B |
| L06 | The Engle-Granger test and the half-life of mean reversion | `engle-granger-test`, `mean-reversion-half-life` | `lab-S3-L06-1`: half-life exact on a noiseless path; OLS half-life on a seeded AR(1) (SIMULATED) | 10 | Builder B |
| L07 | Vector autoregressions and the Johansen test | `vector-autoregression`, `johansen-test` | `lab-S3-L07-1`: VAR(2) by OLS on a seeded system; companion eigenvalues (SIMULATED) | 10 | Builder C |
| L08 | Structural VAR identification | `structural-var-identification` | `lab-S3-L08-1`: Cholesky identification; orthogonal shocks; two orderings (exact) | 10 | Builder C |
| L09 | State-space models and the Kalman filter | `state-space-model`, `kalman-filter` | `lab-S3-L09-1`: scalar local-level filter against the steady-state gain; a two-step exact check in `fractions.Fraction` | 10 | Builder D |
| L10 | Markov-switching models | `markov-switching-model` | `lab-S3-L10-1`: two-state stationary distribution (exact); regime frequencies and filter probabilities on a seeded path (SIMULATED) | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, project ladder, hours 100 + 30 | none | none | - | Builder A (after L01-L03 exist) |
| project | Pairs-trading audit (`both`): ladder, spec, grader panel, rubric, exemplars | none | `lab-S3-project-1` (rung 1, SIMULATED), `lab-S3-project-2` (rung 2, `class="lab completion"`, SIMULATED), `lab-S3-project-3` (rung-3 check on `fx_daily`) | 30 | Builder E |
| grader | `grader/instance.py`, `grader/reference.py`, `grader/starter.py`, `grader/test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01-L10 | none | none | - | Builder F (after A-E) |

Builder ownership: A writes L01, L02, L03 and `index.html` (the hub uses the ten titles above, which are fixed here). B
writes L04, L05, L06. C writes L07, L08. D writes L09, L10. E writes `project.html`, the whole `grader/` directory and the
three project labs. F writes `cards.json`. Each builder writes only its own files and twins.

Ordering (no lesson links a later definition; `check_dag.py` checks linked uses, section 7):
- L02 uses L01 (`stationarity`, `autocorrelation-function`) and M1 `geometric-series` (\(\sum \phi^j\)).
- L03 uses L02 (`arma-model`, the AR(1) and AR(p) forms) and S1 `t-statistic`, `hypothesis-test`.
- L04 uses L03 (`unit-root`); the curriculum lab is here.
- L05 uses L03 (`unit-root`) and L04 (`spurious-regression`) to motivate it.
- L06 uses L05 (`cointegration`), L03 (`dickey-fuller-test`) and S2 `ols-estimator`.
- L07 uses L02 (`arma-model`), M3 `eigendecomposition` (companion-matrix stability) and L05 for the error-correction form.
- L08 uses L07 (`vector-autoregression`) and M3 `singular-value-decomposition` (for Cholesky-type factors: prose only).
- L09 uses L02 (ARMA as state space), M4 `multivariate-normal`, `conditional-expectation-elementary`.
- L10 uses L09 (`state-space-model`, filtering), L02 (AR(1) mean-switching form) and M4 `normal-distribution`.

Hours check: 10 × 10 = 100 (hub `data-hours-lessons="100"`); project 30 (hub `data-hours-project="30"`); 130 total.

Lesson-level minimum content (BUILDER_RULES 4.2): each lesson has at least 3 problems in each of the four tiers, which is
at least 12 problems with worked solutions in 10 h. This is a feasibility risk, recorded as Q12 (the architect may accept
a smaller minimum only through a rule change, not by the builder).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to S3)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` sections 3 to 8, `plans/E5-build-plan.md` (structure),
`plans/M3-build-plan.md` section 1.1 (lessons learned) and its Architect decisions, `plans/FINAL-ARCHITECT-RULINGS.md`,
and this file. Study `course/modules/S/S7/` for the S-part layout and grader grammar (S7 is the reference instance; its
index links the three S3 concepts that S3 must define). `course/templates/` holds the skeletons.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or from
   the lab's unrounded floats, and rounded only at display, with the rule stated (precedent: M3 section 1.1 item 1; CF1 L01).
   This covers every autocorrelation, half-life, t-statistic and critical value.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show (precedent: M3 section 1.1 item 2; M1 LESSON_TEXT_DEFECTS).
3. **Attribute nothing unread.** Only the registry keys in section 7.1 may be cited. A key is cited at paper or book level,
   with no page, table, equation, coefficient, edition or year typed from memory. A result attributed to a paper must be read
   in its abstract (VERIFIER 2.1). A claim the lesson derives is grade T with the derivation as basis (fixer rule: "unread
   standard/book content is ungraded or removed").
4. **Scope words need a computation.** "every", "all", "always", "never", "any", "stable", "robust", "for every process",
   "standard result" are used only where a derivation, a finite check or a lab computes the claim. The tested scope is
   written in the sentence (precedent: M3 section 1.1 item 4).
5. **Define before use.** Each of the 16 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the 16 (weak stationarity's mean, lag operator, innovation, causal, invertible,
   impulse response, half-life as a number of periods, regime, hedge ratio, spread) are defined in prose at first use with a
   plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions
   (A1, A2, ...) before the statement. Examples the builders must state: the AR(1) autocovariance needs \(|\phi| < 1\) and
   \(\sigma^2 > 0\); the ARMA(1,1) autocovariance needs causality and invertibility; the Dickey-Fuller regression needs
   the null \(\gamma = 0\) and iid innovations (A); the half-life formula needs \(0 < \phi < 1\); the Kalman update needs
   jointly Gaussian, linear, zero-mean errors with known covariances; the Cholesky identification needs a recursive
   ordering (an assumption, not a result).
7. **Grader rule (applies: S3 has an autograder).** A grader test asserts an exception type only for a condition the page
   names (section 5.2, the four or five named conditions). A correct implementation may raise a different exception only if
   the page does not name the condition (fixer rule 19; M3 section 1.1 item 7).
8. **Money.** S3 has no money output. The FX series are rates, not money amounts; no integer-cent rule is triggered. If a
   P&L appears, it is out of scope (Q10).
9. **No horizontal scroll at 360 px.** Matrices, companion forms and long equations sit in boxes that wrap or scroll inside
   themselves. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level** with no `if __name__ == "__main__":` guard (`tests/labs/M1/lab-M1-L04-1.py` is the
    model; M3 section 1.1 item 11). `run_labs.py` runs each twin under `python -I -W error`.
11. **Rates are basis-explicit.** Any rate or yield states its unit (percent per year or decimal), its compounding and its
    source. `tbill_3m` is a discount-basis rate (`tools/data_sources.yaml:101-102`); if `ust_daily` is used, the page says so.
12. **Tolerance versus stated accuracy (fixer ruling 22; ruling 25).** Every tolerance in a grader test is at or inside the
    accuracy the page states. A mutant that differs only inside a stated tolerance is equivalent and goes to
    `ledgers/S3/equivalent/` with its proof (ruling 9).
13. **Worked values (fixer ruling 13).** A value derived by hand in a numbered Example with its hypotheses is grade T with
    the Example as basis. A value that appears only in lab output, or rests on SIMULATED data, is grade C naming the lab.
14. **Autograder seeds (fixer rule 19; ruling 10).** Five alternative correct implementations must pass seeds 0-49. If the
    runtime makes that impossible in Pyodide, the page states the reduction and Q13 records it.
15. **Blind scoring (fixer ruling 15 and 23).** The two exemplars are scored blind by a separate scorer that never opens the
    project page and reads only a stripping script's output.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT section 3) and a registry key or a derivation. A B or C
  claim names its published counter-evidence (BUILDER_RULES 2.5). Attribution is at paper level only (section 7.1).
- Concepts: the section 1 table. Plain `<dfn>` for other terms. No `<a class="concept">` for any concept outside the
  prerequisite closure {CS1, M1, M2, M3, M4, P0.1, S0, S1, S2} (section 4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for concepts of closure units; `href="Lnn.html#def-<id>"` for
  earlier S3 lessons. A lesson never links a concept defined in a later lesson. S7 is not a prerequisite and is never linked
  as one.
- Labs: code lives once in `tests/labs/S3/lab-S3-Lnn-1.py` (and `lab-S3-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-S3-<page>-<n>`
  (`tools/check_pages.py:258-259`). Seeded RNG only (`random.Random(seed)`, or `numpy.random.default_rng(seed)` if NumPy is
  used). No network. Under 10 s in Pyodide. No warnings (`-W error`).
- NumPy. The runtime vendors NumPy, SciPy and pytest (`tools/vendor_spec.yaml:59`). A lab that uses NumPy declares
  `data-packages="numpy"` (AP1 pattern as recorded in `plans/M3-build-plan.md` section 1.2, which cites `course/modules/AP/AP1/project.html:53`; not re-read by the planner). The grader is pure Python
  (standard library only) so the grader panel stays light (Q6).
- SIMULATED label: on every lab or figure that uses generated data (L01-L07, L09-L10 simulated parts, project rung 1 and
  rung 2). Exact checks (L02 closed forms, L06 noiseless half-life, L08 Cholesky, L09 Fraction check, L10 stationary
  distribution) are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments (precedent: M1 "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py:58-72` `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis outside code.
- Percent changes state the base and the direction. Growth rates and autocorrelations state the convention (log or simple,
  per period).
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES 10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros and symbols that S3 must not give a different meaning (`notation/notation.json` `macros` object, and the
`symbols` array at lines 112-132):

| Registered symbol | Registered meaning (locator) | S3 rule |
|---|---|---|
| `T` | "number of return observations (periods) in a sample" (`notation/notation.json:112`, module S1) | **Conflict risk.** S3 needs a sample length for generic series, not only returns. Default (Q5): `T` is used for the number of periods in the sample, and the page says "T is the number of periods in the sample, as S1 registers it". No other meaning for `T`. The VAR lag order is `p`, not `T`. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`notation/notation.json:117`, M4) | **Conflict.** Never use `\Phi` for ARMA, VAR or companion polynomials. ARMA polynomials are `\phi(L)` and `\theta(L)`; VAR polynomials are `A(L)`; the VAR coefficient matrices are `A_1 ... A_p`. Use `\phi` for an AR coefficient (matches S7, `course/modules/S/S7/L04.html:130`). |
| `\gamma_3`, `\gamma_4` | skewness and kurtosis (`notation/notation.json:122`, M4) | Autocovariances are written `\gamma(h)`, as S7 writes them (`course/modules/S/S7/L04.html:130`). Never `\gamma_h`. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | AP1 symbols (`notation/notation.json:132` on) | Not used. Noise covariances are `\Sigma_{\eta}` and `\Sigma_{\varepsilon}`; the Markov transition probabilities are `p_{ij}`, not `\pi_{ij}`; no measure is named `\mathbb{Q}`. |
| `\E`, `\Var`, `\Cov`, `\Corr` | expectation, variance, covariance, correlation (`notation/notation.json` `macros`) | Use the macros. Write `\E[\,\cdot\,]`, not `\mathbb{E}`. |
| `\Normal`, `\iid`, `\dto`, `\pto` | normal distribution, iid, convergence in distribution and in probability | `\dto` for the Dickey-Fuller limit statements; `\Normal(\mu,\sigma^2)`; `\iid` for innovation assumptions. |
| `\se`, `\tr`, `\diag`, `\argmin`, `\argmax`, `\indic`, `\R`, `\N` | standard error, matrix trace, diagonal matrix, arg-optimum, indicator, reals, naturals | Used as registered. The Johansen "trace statistic" is named in words; `\tr` is only the matrix trace. |

Local symbols (allowed; each defined on the lesson where first used, never redefined): `y_t`, `x_t` series; `\phi`, `\theta`,
`\mu`, `\sigma`, `\alpha`, `\beta` (regression intercept and slope, and the hedge ratio), `\lambda` (Johansen eigenvalues),
`\Pi` and `\Gamma_i` (VECM matrices), `\Sigma` (covariance), `\kappa` (Kalman gain), `F`, `H` (state-space matrices), `s_t`
(the spread), `h` (lag or horizon, a period count; the half-life is `h^{\ast}`, not `T_{1/2}`), `p` (lag order, also used for
transition probabilities only in L10 with `p_{ij}` written out).

NOTATION_REQUESTS: none. The plan uses only local symbols and registered macros. Any symbol that clashes with the table is
renamed consistently across lesson, lab docstring, twin code, project page, grader docstrings and cards (fixer rule 15).

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the section 2.2 structure (BUILDER_RULES 4.2): why it matters (at most 120 words); core
content with Definition, Theorem, Proof, Example and Remark blocks; inline lab; "Where the canon breaks"; no debate brief
(no debate key, section 11); at least 3 misconceptions; problem sets (at least 3 in each tier, with worked solutions in
`<details class="solution">`); a key-results table; a retrieval quiz of 8 to 15 items. The grades below are the planner's
proposal; the builder re-grades every claim under BLUEPRINT section 3 and the verifier re-grades them independently.

- **L01 `stationarity`, `autocorrelation-function`.** Weak stationarity: constant mean, constant finite variance, and an
  autocovariance \(\gamma(h)\) that depends only on the lag \(h\) (definition, T). The autocorrelation \(\rho(h) = \gamma(h)/\gamma(0)\).
  The AR(1) with \(|\phi| < 1\) has \(\rho(h) = \phi^{|h|}\) (T, derived from the stationary variance \(\sigma^2/(1-\phi^2)\),
  with the assumptions listed). A random walk is not weakly stationary: its variance grows with \(t\) (T). Lab 1: the sample
  ACF of a seeded AR(1) against \(\phi^{h}\) (SIMULATED; the interpretation states only what the printed run shows). Where the canon breaks: finite-sample ACFs are biased; the Gaussian and iid cases are
  not the general case. Misconceptions: a stationary series has no trend in a plot; a large ACF means a unit root; the
  sample ACF is unbiased.
- **L02 `arma-model`, `wold-decomposition`.** AR(p), MA(q) and ARMA(p,q) with lag polynomials; causality (roots of
  \(\phi(z)\) outside the unit circle) and invertibility (roots of \(\theta(z)\) outside it), proved for ARMA(1,1) (T). The
  ARMA(1,1) autocovariances from the closed form (T, derived). For a causal ARMA the \(\psi\)-weights of the MA(\(\infty\))
  representation (T for ARMA(1,1)). The general Wold theorem (every weakly stationary zero-mean process is an MA(\(\infty\))
  of its one-step prediction errors plus a deterministic part): stated as "not proved here" and not graded (fixer rules, "GRADES for unread standards";
  Hamilton 1994 at book level, `hamilton1994time`). Lab 2: ARMA(1,1) autocovariances from the closed form against a seeded
  simulation; the root check (SIMULATED for the simulation part, exact for the root check). Where the canon breaks: linear
  projections are not conditional means; ARMA cannot represent regime change (L10).
- **L03 `unit-root`, `dickey-fuller-test`.** The unit root \(y_t = y_{t-1} + \varepsilon_t\) (definition); the Dickey-Fuller
  regression \(\Delta y_t = \alpha + \gamma y_{t-1} + \varepsilon_t\) with the null \(\gamma = 0\) (T for the algebra). The
  t-statistic under the unit root is not Student's t and has no closed form stated here (not graded; the Dickey-Fuller
  distribution is stated in words and checked in the lab). Dickey and Fuller (1979) is cited at paper level for the test
  (`dickey1979distribution`). Augmented DF with lagged differences (T for the regression). Lab 3: the DF t-statistic under a
  seeded unit root and its empirical 5% quantile against the nominal normal quantile (SIMULATED; grade C naming the lab).
  Where the canon breaks: the iid assumption on \(\varepsilon_t\); structural breaks lower the power. Misconceptions: a
  failure to reject proves a unit root; the DF test is the t-test with normal critical values; differencing always fixes
  a series.
- **L04 `spurious-regression`.** Regressing one independent random walk on another. The nominal t-test rejects far more
  often than 5%, and \(R^2\) is spuriously large (C, with lab 4 named as the basis). The phenomenon is attributed to Granger
  and Newbold (1974) at paper level only (`granger1974spurious`); no number from that paper is typed. Remedies: differencing
  (loses the long-run link) or cointegration (L05). Lab 4 (the curriculum lab, `curriculum/01-foundations.yaml:730`): a
  spurious-regression generator on seeded independent random walks: the rejection rate of the nominal 5% slope test across
  replications, and the distribution of \(R^2\) (SIMULATED). Misconceptions: a high \(R^2\) shows a relationship; differencing
  is always right; the nominal t-test is valid for trending series.
- **L05 `cointegration`.** Two I(1) series are cointegrated with vector \((1,-\beta)\) when \(y_t - \beta x_t\) is
  stationary (definition, T). Two-series error-correction form for the simple case (T for the algebra with the stated
  assumptions). The Granger representation theorem is not stated (NOT IN REGISTRY as a record; Engle and Granger (1987) at
  paper level, `engle1987co`, for the two-step idea). Lab 5: a seeded cointegrated pair; the spread's variance over blocks
  stays constant; the error-correction coefficient recovered by OLS (SIMULATED). Where the canon breaks: a constant \(\beta\)
  is assumed; a structural break in \(\beta\) breaks the spread. Misconceptions: cointegration is correlation of levels;
  two random walks are never cointegrated; a stationary spread is a profitable trade.
- **L06 `engle-granger-test`, `mean-reversion-half-life`.** The Engle-Granger two-step test: OLS of \(y_t\) on \(x_t\), then
  the ADF on the residuals with no intercept; the residual test uses different critical values from the DF test (the
  reason is stated, not derived; grade C naming lab 6 and `engle1987co` at paper level). The half-life: for an AR(1) spread
  with \(0 < \phi < 1\), \(\E[s_{t+h}] - \mu = \phi^h (s_t - \mu)\) and the half-life is \(h^{\ast} = \ln 2 / (-\ln \phi)\)
  (T, derived with the assumptions). The estimator: OLS of \(s_t\) on \(s_{t-1}\) with an intercept. If \(\hat\phi \ge 1\) the
  half-life is infinite; if \(\hat\phi \le 0\) it is undefined (the spec names the ValueError). Lab 6: the formula exact on a
  noiseless path \(s_t = 0.9^t\), and the OLS half-life on a seeded AR(1) (SIMULATED). Misconceptions: the half-life is the
  lag-one autocorrelation; a half-life in periods equals a half-life in years; a short half-life means a tradable spread.
- **L07 `vector-autoregression`, `johansen-test`.** VAR(p) in levels and the companion form (T); stability as eigenvalues of
  the companion matrix inside the unit circle (T, uses M3 `eigendecomposition`, in the closure). The VECM
  \(\Delta Y_t = \Pi Y_{t-1} + \sum_i \Gamma_i \Delta Y_{t-i} + \varepsilon_t\) (T for the algebra); the rank of \(\Pi\) is the
  number of cointegrating vectors (T for the rank statement under the stated assumptions). The Johansen trace procedure is
  described (reduced-rank regression, the trace statistic) and attributed at paper level (`johansen1991estimation`). Its
  critical values are NOT stated here; the lesson says so and points to the project's precomputed table (none for Johansen:
  the project uses Engle-Granger). Lab 7: VAR(2) by OLS on a seeded system against the true coefficients; companion
  eigenvalues (SIMULATED). Where the canon breaks: fixed lag order; linear dynamics. Misconceptions: a VAR is a structural
  model; \(\Pi\) full rank means cointegration; the Johansen test needs normal errors.
- **L08 `structural-var-identification`.** The reduced-form residual covariance \(\Sigma_u\) and the structural shocks
  \(\varepsilon_t\) with \(u_t = B \varepsilon_t\) (definition). Identification needs restrictions (an assumption; the
  count of restrictions is derived, T). Cholesky identification: \(\Sigma_u = PP^{\top}\) with \(P\) lower-triangular; the
  recursive ordering is an assumption (A). Impulse responses from \(P\) (defined in plain prose: "impulse response", no
  `data-concept`). Sims (1980) is cited at paper level for the VAR approach (`sims1980macroeconomics`). Lab 8: \(PP^{\top}
  = \Sigma_u\) to 1e-12 for a seeded system; the responses under two orderings differ (exact; both printed). Where the canon
  breaks: the ordering encodes a contemporaneous assumption; sign and long-run restrictions are not taught here (REFERENCE_REQUEST
  R5 is the lead). Misconceptions: Cholesky identifies the economics; the ordering does not matter; the orthogonal shocks are
  the true shocks.
- **L09 `state-space-model`, `kalman-filter`.** The linear Gaussian state-space model \(x_{t+1} = F x_t + \eta_t\),
  \(y_t = H x_t + \varepsilon_t\) with noise covariances \(\Sigma_{\eta}\), \(\Sigma_{\varepsilon}\) (definition). An AR(p) as a
  state-space model (T, with the companion state). The Kalman recursions, prediction and update, derived from Gaussian
  conditioning (T, uses M4 `multivariate-normal` and `conditional-expectation-elementary`, both in the closure; the L2
  projection view is not used, Q4). The steady-state gain for a scalar local-level model (T). Lab 9: the scalar local-level
  filter against the steady-state gain (SIMULATED for the seeded path, exact for the gain); a two-step example in
  `fractions.Fraction` checked against direct Gaussian conditioning (exact). Attribution of the filter to its original paper:
  REFERENCE_REQUEST R1, so the lesson says "the filter is derived here" and cites no paper. Where the canon breaks:
  linearity and Gaussianity; misspecified noise variances; initialisation. Misconceptions: the filter gives the true state;
  a higher gain is always better; the Kalman filter is only for finance.
- **L10 `markov-switching-model`.** A finite-state Markov chain with transition probabilities \(p_{ij}\) (plain-prose definition
  with the Markov property stated in words, Q4). The two-state stationary distribution: with \(a = p_{12}\) and \(b = p_{21}\),
  \(\pi_1 = b/(a+b)\) (T, derived). The Markov-switching mean model \(y_t = \mu_{S_t} + \phi(y_{t-1} - \mu_{S_{t-1}}) + \varepsilon_t\)
  (definition). The Hamilton filter recursion for the regime probabilities (T, derived from Bayes' rule with the stated
  assumptions); Hamilton (1989) at paper level (`hamilton1989new`). Lab 10: \(\pi_1 = b/(a+b)\) exact against the simulated
  frequency of state 1 (SIMULATED); the filter probabilities against the true regimes on a seeded path (SIMULATED). Where the
  canon breaks: the number of regimes is fixed; the filter depends on parameters that must be estimated (estimation is not
  taught; the lesson says so). Misconceptions: the filter probability is a regime forecast; regimes are observed; a
  two-state model captures every business cycle. Any claim about business-cycle dating is grade B or C with two-sided
  counter-evidence (REFERENCE_REQUEST R7 leads only), or is not made.

Lesson-level constraint: each "Where the canon breaks" names at least one model limit and what changes without it.

---

## 4. DAG problems (concepts that natural S3 content would use outside the closure)

Prerequisite closure of S3 (planner run): **{CS1, M1, M2, M3, M4, P0.1, S0, S1, S2}**, 124 usable concepts. Owners below are
from `tools/coursekit.py` `concept_owner` (planner run). The architect's standing default (2026-10-28 decisions in
`plans/E5-build-plan.md`) applies: an outside concept is plain prose with no link and no `<dfn>` with `data-concept`. Each row
is listed in the output contract's DAG_DEFECTS field as "plain prose, non-blocking", so the architect can object.

| Ref | Concept(s) | Owner (outside closure) | Where natural S3 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `martingale`, `martingale-convergence-theorem` | M6 | "innovation has zero conditional mean" (L02, L03, L09) | Plain prose: "innovations with zero conditional mean". No link. Architect may add M6 (Q4). |
| D2 | `conditional-expectation-l2`, `probability-space` | M6 | the Kalman update as an L2 projection (L09) | Not used. The update is derived by Gaussian conditioning, which uses M4 `multivariate-normal` (in closure). |
| D3 | `brownian-motion`, `markov-property`, `continuous-time-martingale` | SC1 | Dickey-Fuller limit distribution in words (L03); the Markov property of the chain (L10) | Plain prose. The limit is stated in words and checked by lab 3; the Markov property is stated in words in L10. |
| D4 | `ornstein-uhlenbeck-process`, `ito-integral` | SC2 | continuous-time half-life analogue (L06) | Not used. The half-life is discrete (section 3, L06). |
| D5 | `impulse-response-function`, `local-projections`, `narrative-shock-identification` | E6, E7 | impulse responses (L08); local projections as an alternative (not needed) | Impulse response defined in plain prose in L08 (no link). Local projections and narrative identification are not used; they are named as limits only if needed, with no content claim (Q9). |
| D6 | `non-stationarity` | QR3 | the phrase "non-stationary series" (L03, L05) | Plain prose adjective "non-stationary", not the concept. |
| D7 | `random-walk-fx-benchmark`, `ppp-half-life` | X1 | FX context for the project memo | Not used. The memo makes no purchasing-power or random-walk benchmark claim (Q10). |
| D8 | `moving-block-bootstrap`, `stationary-bootstrap`, `false-coverage-statement-rate` | BK5, S7 | bootstrap for dependent data (L01 caveat) | Not used. S3 uses no bootstrap. |
| D9 | `newtons-method`, `numerical-stability`, `monte-carlo-integration` | M8 | numerical optimisation in ML estimation (L09, L10) | Plain prose "a numerical optimiser". No link. |
| D10 | `lagrange-multiplier`, `lagrangian-duality` | M7 | constrained estimation (none needed) | Not used. |
| D11 | `dynamic-factor-model` | GM1 | none | Not used. |

Closure concepts that S3 may link without a DAG question (verified owners, planner run): M1 `geometric-series`,
`exponential-and-logarithm`; M2 `derivative`, `implicit-function-theorem`; M3 `vector-space`, `linear-map`,
`eigendecomposition`, `spectral-theorem`, `positive-semidefinite-matrix`, `singular-value-decomposition`,
`orthogonal-projection`, `least-squares-projection`; M4 `random-variable`, `expectation`, `variance`, `correlation`,
`covariance-matrix`, `normal-distribution`, `multivariate-normal`, `conditional-expectation-elementary`,
`law-of-large-numbers`, `central-limit-theorem`; S1 `estimator`, `consistent-estimator`, `maximum-likelihood-estimation`,
`mle-asymptotic-normality`, `fisher-information`, `hypothesis-test`, `likelihood-ratio-test`, `t-statistic`, `p-value`,
`confidence-interval`, `bootstrap`, `sharpe-ratio` (not needed); S2 `ols-estimator`, `hac-standard-errors`,
`gauss-markov-theorem`; P0.1 `identification`.

`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring). An unlinked use of D1 to D11 passes the tool, so the
verifier reads every lesson for these names (VERIFIER 2.9).

---

## 5. Project (`project.html`, Builder E): autograder and rubric, ladder, spec, rubric

### 5.1 Ladder (BLUEPRINT section 5.1; `tools/check_projects.py:33` requires the order)

Tier M: rungs 1 and 2 are kept to the minimum (BUILDER_RULES 5.1, `BUILDER_RULES.md:188`).

1. **Rung 1, worked example** (`lab-S3-project-1`, SIMULATED): one fully solved, annotated audit of one seeded instance: the
   adjusted DF statistic, the Engle-Granger statistic on the formation window, the half-life of the trading-window spread,
   and the survival decision. Each step has a "why" note. Minimal length.
2. **Rung 2, completion** (`lab-S3-project-2`, `class="lab completion"`, SIMULATED): the half-life line and the survival
   line are replaced by `___`. Graded instantly. The twin is the completed solution; each non-blank page line equals the
   twin's line or contains a blank (`tools/run_labs.py` docstring; fixer ruling 11). `tools/check_projects.py:89-90`
   requires a completion lab or a quiz.
3. **Rung 3, independent project** (graded). (a) The autograded engine `grader/reference.py` mirrored by the student's
   `pairs_audit.py` (section 5.2 and 5.4). (b) The memo, rubric-graded (section 5.5). `lab-S3-project-3` is the rung-3 check:
   it reads `data/fx_daily.csv`, applies the same rules to the 15 pairs with the precomputed critical value, and prints the
   table the memo must show (`data-files="fx_daily.csv"`).
4. **Rung 4, stretch** (optional, not graded): a Johansen trace test on a three-currency triple, or the pairs audit with
   `ust_daily` (`tbill_3m`, `cmt_10y`) as a term-spread pair, with the basis stated.

Time budget (`<table id="hours">`, sums to 30 h; each row has a one-line rationale; `tools/check_projects.py` checks the
total against `data-hours-project`):

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED instance, annotated line by line |
| Rung 2, completion problem | 3 | Fill the half-life line and the survival line, then run the instant check |
| Data intake: `fx_daily` schema, sample split, the formation rule, the spot-rate caveat | 5 | Document the file, the 60% formation rule, the six currencies, and the convention for log USD-per-unit rates |
| Engine: `adf_t`, `eg_t`, `alpha_beta`, `trading_spread`, `half_life`, `survives` (rung 3a) | 9 | Six functions with named ValueError conditions, tested against the reference |
| Audit of the 15 pairs and the half-life table (rung 3a, second part) | 6 | Run the engine on the universe and produce the table the memo cites |
| Memo and self-assessment against the exemplars (rung 3b) | 5 | One-page memo against the rubric; score two exemplars, then compare |
| **Total** | **30** | Equals `data-hours-project` on the hub |

### 5.2 Spec (`project.html`; `tools/check_projects.py` requires context, inputs, required outputs, constraints, grading)

- **Context.** An analyst must test whether pairs of exchange rates are cointegrated on a formation window, measure the
  half-life of the spread on a later trading window, and report how many pairs pass. The memo must cite the numbers it uses.
- **Inputs.** (a) `fx_daily.csv` (`data/fx_daily.csv`): daily noon rates, USD per unit of foreign currency, six currencies
  (AUD, CAD, CHF, EUR, GBP, JPY), 6,706 rows from 2000-01-03 to 2026-09-30, no missing entries (planner check, section 6).
  Use log rates. (b) Seeded SIMULATED instances from `grader/instance.py` for the autograder.
- **Fixed rules (the spec states them; the reference implements them).**
  - Formation window: the first `split = floor(0.6 n)` observations; trading window: the rest.
  - Lag augmentation in every ADF and residual ADF: `lags = 1`, fixed (no lag selection), so the critical values match.
  - Adjusted DF statistic: `adf_t(series, lags)` is the t-statistic of \(\gamma\) in \(\Delta y_t = \alpha + \gamma y_{t-1} + \sum_{j=1}^{\text{lags}} \delta_j \Delta y_{t-j} + \varepsilon_t\) (intercept, no trend).
  - Engle-Granger residual test: `eg_t(y, x, split, lags)` fits \(y_t = \alpha + \beta x_t + u_t\) on the formation window, then
    the ADF on the residuals with **no intercept** and the same lag augmentation.
  - Survival: a pair survives iff its EG statistic is below its 5% EG critical value for the formation length **and** its
    trading-window half-life is finite.
  - Half-life: `half_life(spread)` fits \(s_t = c + \phi s_{t-1} + e_t\) by OLS; returns \(\ln 2/(-\ln\hat\phi)\) for
    \(0 < \hat\phi < 1\), `math.inf` for \(\hat\phi \ge 1\); raises ValueError for \(\hat\phi \le 0\). Units: business days.
  - Critical values: the 5% EG and DF values for the sample length come from the table in section 6 (precomputed, seed 0,
    20,000 replications, stated on the page). No student simulation is required.
- **Frozen interface (proposal; the architect freezes it, Q6 and Q3).** Student module `pairs_audit.py`:
  - `adf_t(series: list[float], lags: int) -> float`
  - `alpha_beta(y: list[float], x: list[float]) -> tuple[float, float]` (OLS of y on x with intercept)
  - `trading_spread(y: list[float], x: list[float], split: int) -> list[float]` (alpha and beta from indices `[0, split)`;
    returns `y_t - alpha - beta * x_t` for `t >= split`)
  - `eg_t(y: list[float], x: list[float], split: int, lags: int) -> float`
  - `half_life(spread: list[float]) -> float`
  - `survives(eg_stat: float, eg_critical: float, half_life_value: float) -> bool`
- **Named ValueError conditions (the only ones a test may assert as ValueError; Q8).** (i) `len(y) != len(x)`; (ii) `lags < 0`;
  (iii) `split` outside `[min_obs, n - min_obs]` with `min_obs = 30`; (iv) any non-finite input value; (v) `half_life` with
  \(\hat\phi \le 0\). Every other invalid input is outside the spec: no test asserts an exception type for it.
- **Required outputs.** `pairs_audit.py` (the student's engine), `diagnosis` memo `memo.md` (or a document of the student's
  choice of at most two pages) with a table of the 15 pairs: EG statistic, its critical value, the formation hedge ratio,
  the trading-window half-life, and the survival verdict. Every number cites its pair, window and transform.
- **Constraints.** No trading P&L and no transaction cost claim: the data are spot rates with no interest differential
  (`tools/data_sources.yaml:28-30`). No claim that any pair is profitable. Every claim about pair profitability in the memo is
  grade B or C and needs two-sided counter-evidence (REFERENCE_REQUEST R7), or is not made.
- **Grading.** `both`: the autograder runs `grader/test_project.py` on seeds 0-49; the memo is rubric-graded (section 5.5).
  The spec's grading entry names both "autograder" and "rubric" (`tools/check_projects.py:38-49`).
- **Reading list.** Registry keys only (section 7.1): `engle1987co`, `granger1974spurious`, `dickey1979distribution`,
  `johansen1991estimation`, `hamilton1994time` (book level). Nothing else.

### 5.3 Grader design (`grader/`, Builder E)

- **`grader/instance.py`:** `make_instance(seed: int) -> dict`. Deterministic. Generates `k = 6` pairs of length
  `n` in {400, 450, ..., 600} from the seed, with: two planted cointegrated pairs (AR(1) spread with \(\phi \in [0.8, 0.95]\),
  nonzero means on both series); two independent random-walk pairs; one "break" pair that is cointegrated on the formation
  window and has a trading-window spread with \(\hat\phi \ge 1\) (a drifting spread, so M10 is detectable); one pair with a
  noise-free exact relation for the alpha-beta tests. Labelled **SIMULATED** in the docstring and on the page. The instance
  contains the 5% EG and DF critical values for its own sample length, copied from the precomputed table in section 6. The
  instance validates every named condition (no ValueError is raised by valid instances). Seeds 0-49 must give materially
  different series (different planted \(\phi\), means, lengths), not only different labels.
- **`grader/reference.py`:** the full solution, stdlib only; must pass every test for seeds 0-49.
- **`grader/starter.py`:** the student's skeleton with the six signatures and docstrings, no solutions.
- **`grader/test_project.py`:** pytest suite of properties and numbers. Required tests (minimum set):
  1. `alpha_beta` recovers exact planted `alpha`, `beta` on the noise-free pair (tolerance 1e-9).
  2. `adf_t` is invariant to adding a constant to the series and to scaling it (t-statistic unchanged to 1e-9).
  3. `adf_t` on the planted stationary series is more negative than the DF critical value; on an independent random walk it
     is above it (both directions, instance-specific).
  4. `eg_t` on the planted cointegrated pairs is below `eg_critical`; on independent random walks it is above it (both
     directions).
  5. `eg_t` equals the test's own independent computation of the residual ADF with no intercept (the convention test).
  6. `half_life` on the noise-free path `s_t = 0.9**t` equals `ln 2 / (-ln 0.9)` to 1e-9 (exact; T).
  7. `half_life` on the linear path `s_t = t` returns `math.inf` (\(\hat\phi = 1\) exactly).
  8. `half_life` on the alternating path `s_t = (-0.5)**t` raises ValueError (named condition v).
  9. `half_life` is unchanged by adding a constant to the spread and by scaling it (invariance, 1e-9).
  10. `trading_spread` uses only formation data: changing the series after `split` changes the trading spread only by the
      same change in `y_t - alpha - beta x_t`, with `alpha`, `beta` unchanged (the lookahead test).
  11. `survives` is True iff `eg_stat < eg_critical` **and** the half-life is finite, checked on both sides of each inequality
      and on a half-life of `math.inf`.
  12. Each named ValueError condition (i) to (iv) raised by `trading_spread`, `eg_t` or `adf_t` as applicable, one test each,
      and a valid edge case at `lags = 0` (no ValueError).
  13. Edge cases: `split` at `min_obs` and at `n - min_obs` accepted; one below and one above rejected (both directions).
  Each test finishes under 5 s in Pyodide and the suite under 60 s.
- **Feedback.** A failing test names the property violated and a concept hint, never the expected number
  (`__tracebackhide__` in the helper, fixer rule 19).
- **Integrity.** Never claim the tests are secret. Integrity rests on per-seed instances (BUILDER_RULES 5.3 item 6).
- **Five alternative correct implementations (for the verifier; all pass seeds 0-49):** (1) OLS by the normal equations solved
  in `fractions.Fraction`, converted to float; (2) OLS by `numpy.linalg.lstsq` (the only use of NumPy in the grader's
  alternatives, not in the reference); (3) ADF by Frisch-Waugh-Lovell residualisation of the augmentation terms; (4) the
  half-life and ADF through the drift parametrisation \(\Delta s_t = c + \rho s_{t-1} + \dots\) with \(\hat\phi = 1 + \hat\rho\),
  for the half-life only; (5) OLS by pure-Python Gauss-Jordan elimination with partial pivoting. Runtime: alternative (1) may
  exceed the Pyodide budget; if it does, Q13 applies.
- **Ten student-error mutants (single-change copies of the reference under `ledgers/S3/mutants/`; first docstring line names
  the student error; the verifier writes and runs them, then `tools/mutate_graders.py --unit S3 --seeds 0-9`):**
  1. `half_life` returns \(\ln 2/(1-\hat\phi)\) (wrong formula).
  2. `half_life` uses base-10 logarithms (wrong units; the result is off by \(\ln 10\)).
  3. `eg_t` fits an intercept in the residual ADF (wrong EG convention).
  4. `adf_t` ignores the lag augmentation (drops the \(\Delta y_{t-j}\) terms).
  5. `adf_t` uses \(y_t\) instead of \(y_{t-1}\) on the level term (off-by-one lag).
  6. `alpha_beta` regresses x on y and inverts the slope (inverted regression).
  7. `alpha_beta` omits the intercept (biased slope when the means are nonzero).
  8. `survives` uses `eg_stat > eg_critical` (direction reversed).
  9. `trading_spread` estimates alpha and beta on the full sample (lookahead; killed by test 10).
  10. `survives` ignores the half-life (returns True when EG passes, even when the half-life is infinite; killed by test 11).
  A mutant that differs from the reference only inside a stated tolerance is equivalent and goes to `ledgers/S3/equivalent/`
  with its proof (ruling 9). A mutant that uses the DF critical value instead of the EG value is a student error only when the
  instance has a pair whose statistic lies between the two values; the instance must guarantee such a pair on each seed
  (design check at build time; if not guaranteed, the mutant is added as eleventh and killed by a designed pair).

### 5.4 Test-count line for the page

The page quotes the collect-only count of `grader/test_project.py` (fixer rule 19), read from `pytest --collect-only -q` in
the grader directory at build time. The planner expects 13 test functions plus parametrisation; the builder reports the
actual number.

### 5.5 Rubric (`table.rubric#rubric`; `tools/check_projects.py:58-71`)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to
1. Every descriptor is observable.

1. **Data and sample.** Level 4: names `fx_daily`, its six currencies, its date range and transform (log of USD per unit),
   the formation split and its length, and the number of observations per pair. Level 1: "uses the data".
2. **Test design.** Level 4: states the EG residual test with no intercept and `lags = 1`, names the critical value used for
   each pair and its source (the precomputed table, seed and replications), and states why the DF value is wrong for residuals.
   Level 1: "tests for cointegration".
3. **Half-life stability.** Level 4: gives the half-life formula, its units (business days), the trading-window values for
   each survivor, and the spread between the largest and smallest values, all to a stated rounding. Level 1: "discusses
   half-lives".
4. **Survivors and multiplicity.** Level 4: states the survival rule, the count of survivors out of 15, and the expected count
   under a per-test 5% level for 15 tests, with the statement that the pairs share currencies and are not independent.
   Level 1: "counts some pairs".
5. **Limits and evidence.** Level 4: names the model limits used in the verdict (spot rates with no interest differential,
   structural breaks, the 60% formation rule, the fixed lag), separates SIMULATED from data-backed results, and states the
   counter-evidence for any claim graded B or C. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on the **SIMULATED**
seeded instance (seed fixed on the page, so their numbers reproduce from `grader/reference.py`), annotated with the descriptors
each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`,
`data-exemplars="exemplar-a exemplar-b"`, as in S7 and M3). The page shows where the student's scores diverge from the
exemplar scores. Calibration: a separate blind scorer scores both exemplars within one level per criterion (ruling 23).

### 5.6 Adversarial question bank

Not required (Q7). The memo is not an investment-committee defence.

---

## 6. Real-data policy

- **Embedded and cleared: `fx_daily`** (`tools/data_sources.yaml:19-51`; `course/assets/data/market/MANIFEST.json`, `datasets[0]`).
  Issuer: Board of Governors of the Federal Reserve System, G.5/H.10 (noon buying rates in New York). Licence quote:
  "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed
  without permission. Please cite to the Board as the source of the information." (`tools/data_sources.yaml:23-26`;
  `licence_url` line 26). Columns: AUD, CAD, CHF, EUR, GBP, JPY, USD per unit of foreign currency (CAD, CHF, JPY inverted
  per the transform, `tools/data_sources.yaml:51`). Rows: 6,706; first 2000-01-03; last 2026-09-30; retrieved 2026-10-19
  (MANIFEST). The MANIFEST SHA-256 of the snapshot begins `02872dd7`.
- **Planner check (not a substitute for the verifier's check):** `course/assets/data/market/fx_daily.csv` has the header
  `date,AUD,CAD,CHF,EUR,GBP,JPY`, 6,706 data rows, and no empty or non-numeric entries in any of the six columns. Pairs can
  therefore use the full sample with no missing-value rule (the spec still states the rule, Q2).
- **Honest caveats (from the dataset's own note, `tools/data_sources.yaml:28-30`):** spot rates only; a currency position's
  return also earns the interest differential, which these series do not contain; dates are New York business days. The memo
  states these, and no carry or profit claim is made.
- **Not embedded:** no other series is needed. `fx_monthly` and `ust_daily` are available. `ust_daily` is used only in
  rung 4 and only with its discount-basis note (`tools/data_sources.yaml:101-102`).
- **Simulated data** is labelled SIMULATED on every figure, lab and exemplar that uses it.
- **Claimed pairs (honest data).** The default universe is the 15 pairs of the six currencies. No pair is described as a
  published claim. If a source with a published claim is wanted, it is a DATA_REQUEST, not an invented list (Q2).
- **Critical values (honest data).** The precomputed EG and DF 5% critical values are simulated (seed 0, 20,000 replications,
  a stated build script). They are SIMULATED values and are labelled so. The build script is not a lab twin and must not run
  in Pyodide; its output is embedded (BUILDER_RULES 6.1, precompute at build time, say so on the page). The table covers the
  formation lengths of the autograder instances and the `fx_daily` formation length (4,023 observations, floor of 0.6 × 6,706). The values are
  not typed by hand; they come from the build script's output file (Q3).
- No `data-files` attribute on any lab except `lab-S3-project-3`, which lists `data-files="fx_daily.csv"`. The browser writes
  `data/fx_daily.csv` before the run; `check_pages.py` requires the name to be in MANIFEST and on disk.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

Each key below was read in `references/references.json` (line numbers given) and each has `used_by` containing `S3`.
Attribution is at paper or book level, with no page, table, coefficient or number typed from memory.

| Key | Record (as read) | Status | Use in S3 |
|---|---|---|---|
| `dickey1979distribution` | Dickey and Fuller 1979, JASA, volume 74, issue "366a", pages 427-431 (`references/references.json:6895`) | verified; `used_by` S3; the curriculum string says "74(366)" (`curriculum/01-foundations.yaml:724`) | L03 (paper level for the DF test); reading list; project |
| `granger1974spurious` | Granger and Newbold 1974, Journal of Econometrics, volume 2, issue 2, pages 111-120 (`references/references.json:11021`) | verified; matches `curriculum/01-foundations.yaml:725` | L04 (paper level for the phenomenon; no content claim); reading list |
| `engle1987co` | Engle and Granger 1987, Econometrica, volume 55, issue 2, page 251 (`references/references.json:8054`) | verified; matches `curriculum/01-foundations.yaml:726` | L05, L06 (paper level); reading list |
| `johansen1991estimation` | Johansen 1991, Econometrica, volume 59, issue 6, page 1551 (`references/references.json:13773`) | verified; matches `curriculum/01-foundations.yaml:727` | L07 (paper level for the procedure); reading list |
| `sims1980macroeconomics` | Sims 1980, Econometrica, volume 48, issue 1, page 1 (`references/references.json:20851`) | verified; matches `curriculum/01-foundations.yaml:728` | L08 (paper level for VAR-based macro analysis) |
| `hamilton1989new` | Hamilton 1989, Econometrica, volume 57, issue 2, page 357 (`references/references.json:11310`) | verified; matches `curriculum/01-foundations.yaml:729` | L10 (paper level for the filter and the model) |
| `hamilton1994time` | Hamilton, "Time Series Analysis", Princeton University Press (`references/references.json:11346`); record type `edited-book`; `years` [1994, 2020] | verified; the curriculum string is `curriculum/01-foundations.yaml:723` | book level for L01, L02, L03, L09, L10 and the reading list; no year or edition typed |

Registry keys that exist but are NOT to be cited by S3 without the architect's approval (used by another unit):
`benjamini1995controlling` (`references/references.json:2260`, `used_by` S7). Benjamini-Hochberg is not used (Q9).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

Each entry describes the need. The planner does not type an author, year, title or venue from memory. The architect resolves
each through `tools/add_reference.py` (DOI, ISBN or an allow-listed issuer page; BUILDER_RULES 2.4).

- **R1.** The original paper that introduces the Kalman filter. Needed for: L09 attribution. Confidence in the need: certain;
  no record identified by this planner. Until resolved the filter is derived, not attributed.
- **R2.** The paper or papers on the asymptotic theory of regressions with unit roots and of spurious regressions (the
  Phillips line of work). Needed for: L03 or L04 if any asymptotic statement beyond the lab is made; otherwise not needed.
  Confidence: the need is possible, not certain.
- **R3.** The published Engle-Granger critical-value tables (the MacKinnon line of work). Needed for: an independent
  cross-check of the precomputed table in section 6 (a verifier check), not for teaching. Confidence: a check, not a need.
- **R4.** The general Wold decomposition theorem, original source. Needed for: L02 if the general theorem is to be proved or
  attributed. Until resolved it is not stated as proved (section 3, L02).
- **R5.** Structural VAR identification beyond recursive (Cholesky) schemes, including sign and long-run restrictions.
  Needed for: L08 two-sided treatment if any other scheme is named. Until resolved, L08 names Cholesky only.
- **R6.** A VAR and cointegration textbook (book level) for the Johansen procedure. Needed for: L07 if the trace test's
  critical values or its derivation are to be stated. Until resolved they are not stated.
- **R7.** Pairs-trading literature, both the evidence for profitability and the evidence against it. Needed for: any memo or
  lesson sentence that makes a profitability claim (B or C grade with counter-evidence, BUILDER_RULES 2.5). Default: no such
  claim is made.
- **R8.** Original source for the Markov-switching filter's application to business-cycle dating, both sides. Needed for: L10
  only if business-cycle dating is mentioned. Default: not mentioned.
- **U1 (used_by).** Adding `S3` to `used_by` of `benjamini1995controlling` if Benjamini-Hochberg is adopted (Q9). Architect only.

Until R1 to R8 are resolved, every empirical sentence is graded C at most with its basis named (the lab), or is removed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for S3 (section 0.1). No `atlas/S3.contract.md` is needed. `check_projects.py`
checks an Atlas contract only when the project names an `atlas` key (`tools/check_projects.py`, the Atlas check; S3's project
has none). The brief does not name Atlas. S4 is the Atlas milestone A4 and is downstream of S3 (`curriculum/01-foundations.yaml:763-769`).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/S/S3/cards.json`, ids `S3-c001` upward, `lesson` in L01-L10, one card per definition, theorem statement, key
  formula, key result and misconception (BUILDER_RULES 7). `tools/check_pages.py` `check_cards` (lines 366-398) checks the id
  prefix, the lesson's existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lesson 6, derivation of the half-life (exact)"`.
- Cite a registry key only for an attributed claim, and only at paper or book level (section 7.1). `cite` is `[]` where the card
  is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis` (for example `"basis": "Lab 4 (SIMULATED)"`), with grade C.
- The S7 cards already use `stationarity`, `autocorrelation-function` and `arma-model` (`course/modules/S/S7/cards.json`); the
  S3 cards for those concepts state the S3 definitions, not S7's usage.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit S3            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit S3
.venv/bin/python tools/check_projects.py --unit S3
.venv/bin/python tools/run_labs.py --unit S3               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/S/S3/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/S/S3/L04.html --refresh lab-S3-L04-1   # after editing a twin
.venv/bin/ruff check tests/labs/S3 && .venv/bin/ruff format --check tests/labs/S3
.venv/bin/mypy tests/labs/S3                               # strict, repository configuration
```

Grader, after `grader/` exists (Builder E; both modes):

```bash
.venv/bin/python tools/run_graders.py --unit S3 --seeds 0-49
.venv/bin/python -m pytest --collect-only -q course/modules/S/S3/grader   # the count quoted on the page (fixer rule 19)
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit S3 --seeds 0-9` (the ten mutants and
their killers), `.venv/bin/python tools/page_smoke.py --unit S3` (timing-sensitive; not run by builders),
`.venv/bin/python tools/verify_refs.py --unit S3` (the unit ledger's run, VERIFIER 2.1), and
`.venv/bin/python tools/fetch_data.py --check` (offline; run only if the MANIFEST or a snapshot is touched, which the plan does
not do).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md.

Not run for S3 by builders: `tools/fetch_vendor.py` (vendored runtime already present for M3 and S7; the architect runs it for
the deployment gate), `tools/run_labs.py --all`.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **Autograder and rubric.** Unlike E5, S3 is graded `both`. Its grader panel, test suite, reference, alternatives and
   mutants are required (`tools/check_projects.py:122-125`, 138-139; section 5).
2. **Tier M rung rule.** Rungs 1 and 2 are kept to the minimum at tier M (BUILDER_RULES 5.1). The E5 "full length" wording does
   not apply.
3. **No debate.** S3 has no `debate:` key (`curriculum/01-foundations.yaml:697-737`). The two-sided rule (BUILDER_RULES 2.5)
   still applies to Markov switching and any pairs-profitability claim.
4. **No Atlas.** No `atlas:` key and no Atlas entry names S3 (section 8).
5. **Closure is mostly unbuilt.** S0, S1, S2 and CS1 are not built (section 0.1). `check_dag.py` uses the curriculum closure, so
   the S3 pages can be checked; the concept anchors in `concepts.html` are expected for every concept, to be confirmed by grep at build time (generated by
   `tools/build_site.py`).
6. **Build order.** S7 (built) requires S3 (unbuilt) and cites its concepts (section 0.1). This is recorded (Q15).
7. **One curriculum lab, ten required.** The curriculum names one lab (`curriculum/01-foundations.yaml:730`); BUILDER_RULES 3.4
   requires a numerical check per key formula. The plan adds one lab per lesson (E5 and M3 precedent).
8. **check_dag sees linked uses only.** Unlinked uses of D1-D11 (section 4) pass the tool; the verifier reads for them.
9. **Hub hours rule.** `tools/check_pages.py:325-342`: lessons 100, project 30, total 130 (section 1).
10. **First-year and Quantitative Methods groupings** (`curriculum/meta.yaml:131`, `:154`): grouping only. No action (Q14).
11. **NumPy.** Labs may use NumPy (vendored, `tools/vendor_spec.yaml:59`); the grader does not (section 2.2).
12. **Pyodide timing.** The `fx_daily` twin (`lab-S3-project-3`) reads about 6,706 rows in pure Python; its runtime under
    Pyodide must be measured by the verifier and stated (Q13 covers the grader's seed range).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Q1, the project's data.** Use the embedded `fx_daily` as the project's real data, through `data-files`, with the quoted
   licence and the spot-rate caveat. **RECOMMENDED: yes.** The verifier opens `licence_url` (`tools/data_sources.yaml:26`) and
   finds the quoted sentence before the row passes (VERIFIER 2.8). The planner did not open the page.
2. **Q2, the claimed pairs.** The audit universe is the 15 pairs of the six embedded currencies, and no published claim is
   tested. **RECOMMENDED: yes.** The page says so in one sentence. A list of published claims is a DATA_REQUEST, never typed by
   the builder. The formation window is 60% of the sample (`floor(0.6 n)`), and the missing-value rule is stated although no
   entry is missing.
3. **Q3, critical values.** Precomputed EG and DF 5% critical values from a seeded Monte Carlo at build time, embedded in the
   page and in each autograder instance; no student simulation. **RECOMMENDED: yes**, with the build script's output file kept
   under `ledgers/S3/scripts/` and the seed and replications stated. The pure-Python runtime makes student simulation
   infeasible in Pyodide.
4. **Q4, outside-closure concepts.** Plain prose with no link for D1 to D11 (section 4), including the Kalman update derived by
   Gaussian conditioning rather than the L2 projection. **RECOMMENDED: yes.** Alternative: add M6 as a prerequisite of S3
   (a curriculum change, `curriculum/01-foundations.yaml:701`; precedent CF1 Q1). The architect decides; the builders do not
   edit the curriculum.
5. **Q5, notation.** `T` is the number of periods in the sample (registered as "number of return observations (periods) in a
   sample"); `\phi` for AR coefficients; `\phi(L)`, `\theta(L)`, `A(L)` for polynomials; never `\Phi`; `\gamma(h)` for
   autocovariances; `\Sigma_{\eta}`, `\Sigma_{\varepsilon}` for noise covariances. **RECOMMENDED: yes.** No NOTATION_REQUESTS.
6. **Q6, NumPy and the grader's language.** Labs may use NumPy (`data-packages="numpy"`), the grader and the reference are
   stdlib only, and the `pairs_audit.py` signatures are those of section 5.2. **RECOMMENDED: yes**, as M3 Q3 decided for NumPy.
   The signatures are frozen when the architect confirms this plan.
7. **Q7, adversarial.** Not adversarial: no question bank, no debate, no IC defence. **RECOMMENDED: yes** (M3 Q7 precedent).
8. **Q8, named ValueError conditions.** The five conditions in section 5.2 (lengths, lags below zero, split out of range with
   `min_obs = 30`, non-finite input, half-life with \(\hat\phi \le 0\)) are the only ones a test may assert as ValueError.
   **RECOMMENDED: yes.** Every other invalid input is outside the spec.
9. **Q9, multiplicity.** Survival is the EG test at 5% plus a finite half-life; no multiple-testing correction is applied, and
   the memo reports the count of survivors against the expected count under 15 tests at 5%, with the dependence caveat.
   **RECOMMENDED: this**, because a Bonferroni or Benjamini-Hochberg rule would need p-values for the EG test, which the
   precomputed table does not supply, and BH needs an architect `used_by` change (U1). Alternative: Bonferroni with a
   simulated level-\(\alpha/15\) table (a stretch for rung 4).
10. **Q10, no profitability or P&L.** The memo makes no profit, trade or cost claim, and no benchmark claim (random walk, PPP).
    **RECOMMENDED: yes.** The FX data carry no interest differential (`tools/data_sources.yaml:28-30`), so a P&L would be
    unsupported by the data.
11. **Q11, hours.** 10 lessons × 10 h and a 30 h project (23.1%). Alternatives within the rules: 9 lessons × 11 h and a 31 h
    project; 13 lessons × 8 h and a 26 h project. **RECOMMENDED: 10 × 10 and 30**, because it gives one concept-holding lesson
    per concept pair with no lesson left empty.
12. **Q12, problem-set minimum.** BUILDER_RULES 4.2 item 7 requires at least 3 problems in each of four tiers, so at least 12
    worked solutions per lesson, in 10 h. **RECOMMENDED: keep the rule**, and the builder writes short worked solutions; if
    the architect judges it infeasible, the change is a rule change, not a builder choice.
13. **Q13, seed range for the alternatives.** Five alternatives must pass seeds 0-49 (fixer ruling 10). Alternative (1), the
    `Fraction` normal equations, may exceed the Pyodide budget. **RECOMMENDED: seeds 0-49 for all five**, falling back to 0-9
    for alternative (1) only, with the page stating the reduction (E3 precedent, ruling 10). The verifier measures the runtime.
14. **Q14, groupings.** The first-year sequence (`curriculum/meta.yaml:131`) and the Quantitative Methods topic (`:154`) list S3
    without a tier conflict. No action. **RECOMMENDED: confirm no action.**
15. **Q15, build order.** S7 is built and requires S3, which is unbuilt; S2, S1 and S0 are unbuilt. **RECOMMENDED: S3 proceeds
    now** (the closure's links resolve through `concepts.html`), and the architect records that S7's "From S3" links are to
    concepts, not to S3 pages (`course/modules/S/S7/index.html:69`).
16. **Q16, registry metadata.** `hamilton1994time` (`edited-book`, years [1994, 2020]) and `dickey1979distribution` (issue
    "366a") are cited by key only, with no year, edition or issue typed. **RECOMMENDED: cite by key; the architect may correct
    the curriculum strings** (`curriculum/01-foundations.yaml:723-724`) after checking the record, as E5 B4 proposes.

Decisions needed before the builders start: **Q1, Q3, Q4, Q5, Q6, Q8, Q9**. The rest may proceed on the recommendation.

---

## 13. After the builders

1. Orchestrator integrates; runs the section 10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03 with the hub (`index.html`); L04-L06 (includes the
   curriculum lab `lab-S3-L04-1`); L07-L08; L09-L10; the project (grader, mutants, alternatives, the rubric and the blind
   scorer, which is a separate agent per fixer ruling 23); cards (sampled, plus duplicate scan). Failing rows return to the
   builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/S3.verification.json`; verifier scripts archived under `ledgers/S3/scripts/` (VERIFIER 3); mutants under
   `ledgers/S3/mutants/`; equivalent mutants under `ledgers/S3/equivalent/` with a README (ruling 9).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps (R1 to R8, Q-items not accepted) are named
   and agreed. Registry requests are answered by the architect through `tools/add_reference.py`, never by a builder.
5. Honest gaps the pages must state in one sentence each: no record for the Kalman filter's original paper (L09 derived, not
   attributed); the general Wold theorem not proved (L02); the Johansen critical values not stated (L07); the Engle-Granger
   critical values are precomputed simulation values (project); spot FX rates carry no interest differential (project); no
   profitability claim is made (project).

Architect decisions: pending (section 12). This plan is the planner's proposal.
