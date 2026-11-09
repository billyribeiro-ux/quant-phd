# E6 build plan: Macroeconomics II: Dynamic General Equilibrium (2026-11-09)

Unit: **E6 · Macroeconomics II: Dynamic General Equilibrium** · tier M · 150 h · prerequisites E5, M7, S3 · no Atlas
milestone · no debate key · grading `autograder` (no rubric) · output directory `course/modules/E/E6/` (part code `E`) ·
lab twins `tests/labs/E6/` · grader `course/modules/E/E6/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no ledger. Executors: Haiku builders, then
independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Registry facts cite `references/references.json:<line of the "key" field>`.
Planner-derived facts about the tooling were checked by reading the tool source, or by running `tools/coursekit.py`
(`prerequisite_closure`, `concept_owner`) through the repo venv. The planner did not read any paper or book named here;
no bibliographic detail, page, equation or number is typed from memory.

**Status: NO HARD BLOCKER. Three decisions are needed before the builders start (§0.3: B1 the unbuilt prerequisite S3,
B2 the outside-closure concepts that the NK model needs, B3 the Woodford year conflict). The hours are feasible (§0.2).
E6 needs no real data (§6), so the data blocker that E5 carries (E5 B1) does not apply.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part E, code `E`; E6 sits inside the part-E block (E1 begins at line 18, E9 at line 312) | `curriculum/02-economics-finance-core.yaml:18`, `:191`, `:312` |
| E6 id and title "Macroeconomics II: Dynamic General Equilibrium" | `curriculum/02-economics-finance-core.yaml:191-192` |
| Tier `M` | `curriculum/02-economics-finance-core.yaml:193` |
| Hours `150` | `curriculum/02-economics-finance-core.yaml:194` |
| Prereqs `[E5, M7, S3]` | `curriculum/02-economics-finance-core.yaml:195`; JSON row `curriculum/curriculum.json:7535` (the E6 `"id"` line) |
| Core: "RBC, New Keynesian models, determinacy, heterogeneous-agent (HANK) models, solution and estimation methods." | `curriculum/02-economics-finance-core.yaml:196-198` |
| `introduces` has 11 concepts (listed in §1) | `curriculum/02-economics-finance-core.yaml:200-210` |
| Sources: five free-text strings | `curriculum/02-economics-finance-core.yaml:212-216` |
| Lab: "Three-equation NK impulse responses." | `curriculum/02-economics-finance-core.yaml:217` |
| Project "NK model solver"; brief: "Solve the NK model by undetermined coefficients and numerically, verify the determinacy (Taylor) principle, and reproduce the canonical impulse responses."; deliverable "Tested solver plus a figure set."; grading `autograder` | `curriculum/02-economics-finance-core.yaml:218-225` (title 219, brief 220-223, deliverable 224, grading 225) |
| The E6 brief does not name Atlas (contrast E5's brief, `yaml:186-188`) | `curriculum/02-economics-finance-core.yaml:220-223` |
| No `debate:` key on E6 | `curriculum/02-economics-finance-core.yaml:191-225` (absent) |
| No Atlas entry names E6 (the 20 entries name CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/curriculum.json` `atlas` array (planner check: no `E6`) |
| E6 is referenced by a `requires` list at `:8`, by a credential at `curriculum/meta.yaml:123`, and by the first-year sequence group at `curriculum/meta.yaml:133` (E5, E6, E7) | the three locators named |
| E6 sits at position 55 (0-based) of the 134-unit `topological_order` | `curriculum/curriculum.json` `topological_order` (planner check) |
| Prerequisite closure of E6, computed with `tools/coursekit.py` `prerequisite_closure("E6")`: **{CS1, E1, E5, M1, M2, M3, M4, M7, P0.1, S0, S1, S2, S3}**; 176 concepts are introduced inside it | run output, planner |
| Built status of the closure: built with a ledger: E1 (`course/modules/E/E1`, `ledgers/E1.verification.json` PASS), E5 (`course/modules/E/E5`, `ledgers/E5.verification.json` PASS), M1-M4 and M7 (`course/modules/M/`, PASS ledgers). **Not built: CS1, P0.1, S0, S1, S2, S3** (`course/modules/CS/` holds only CS2; `course/modules/S/` holds only S7; no `P0.1` directory) | directory listing, planner |
| E6's 11 concepts all map to module E6 in `concepts` | `concept_owner()` planner check: owners of the 11 ids are E6 |

Nearest built prerequisite: **E5** (its plan `plans/E5-build-plan.md` is the structure template for this plan, and its
binding `Architect decisions` section, which closes that plan, is the precedent for the defaults in §2 and §12).
M7 is the nearest built **autograder** precedent: `course/modules/M/M7/project.html:359` (grader panel) and
`course/modules/M/M7/grader/` (instance, reference, starter, test_project).

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 150 h (`curriculum/02-economics-finance-core.yaml:194`). The tool rules:

- lesson `data-hours` between 6 and 12 inclusive (`tools/check_pages.py:227-228`);
- hub `data-hours-lessons + data-hours-project = 150` (`tools/check_pages.py:337-338`);
- project share 10-40% of 150, i.e. 15 to 60 h (`tools/check_pages.py:339-340`);
- lesson hours sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split (Q1): **10 lessons × 12 h = 120 h; project 30 h (20%)**. 120 + 30 = 150. Feasible. 12 h is the maximum a
lesson may declare, so no lesson can absorb overrun; the alternative in Q1 (11 × 10 h + 40 h project) is also feasible.
**No STOP condition on hours.**

### 0.3 Blocking and open issues (architect decision before the builders start)

**B1. Prerequisite S3 is in the closure but unbuilt.** `curriculum/02-economics-finance-core.yaml:195` lists S3;
`course/modules/S/` holds only S7. Concepts used from S3 (`kalman-filter`, `state-space-model`, `arma-model`,
`stationarity`, `vector-autoregression`, `markov-switching-model`; owners S3 and in closure) are linkable:
`course/concepts.html` carries their anchors (planner grep: `id="kalman-filter"` present). The reader is assumed to know
these concepts, but no page of S3 has been verified. **Recommended default:** proceed; L08 and L10 link S3 concepts as
`../../../concepts.html#<id>`; the hub's prerequisite line names S3 as text only, with no hub link (no S3 hub exists).
The architect acknowledges this as an honest gap (§12 Q2). E5 precedent: E5 was built while E1 was unbuilt (E5 plan §11
item 6, now stale because E1 is built).

**B2. The NK model needs concepts outside the closure.** Rational expectations (`rational-expectations-equilibrium`, E4),
CRRA utility (`crra-utility`, E3), dynamic programming (`dynamic-programming`, CS2) and the Euler equation
(`euler-equation-gmm`, AP3) are owned outside the closure (§4). **Recommended default:** plain prose with no link, as the
E5 defaults say (E5 plan, `Architect decisions`, line 563). The architect may instead add E4 or E3 as prerequisites, a
curriculum change the builders may not make (§4, §12 Q3-Q6).

**B3. Woodford year conflict.** The curriculum says "Woodford, Interest and Prices (2003)" (`yaml:215`). The registry
record `woodford2004interest` (`references/references.json:23317`) has `year: 2004`, with `notes.year`
`{"curriculum": "2003", "crossref": "2004"}`. **Recommended default:** cite the key only, with no year and no edition in
the prose (the E5 B4 precedent). The architect decides whether to correct `yaml:215` after checking the record (§12 Q8).

Non-blocking, noted for the architect:

- **N1.** The other four source strings match their registry records (§7.1): Kydland & Prescott (`yaml:212`), Clarida, Galí & Gertler (`yaml:213`), Galí 2nd ed. (`yaml:214`), Kaplan, Moll & Violante (`yaml:216`).
- **N2.** No review-queue entry names an E6 source (`references/review_queue.json` grep: no E6 or NK author match).
- **N3.** The E6 closure contains no unverified recall-only source: every closure key the plan cites is registry-verified (§7.1).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

10 lessons × 12 h = 120 h; project 30 h; total 150 h. Concept counts per row sum to 1+1+1+1+2+1+1+1+1+1 = 11; each E6 concept
sits in exactly one row (`yaml:200-210`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:200-210`) | Lab (twin id, `tests/labs/E6/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The real business cycle model | `rbc-model` (`yaml:200`) | `lab-E6-L01-1`: the RBC steady state, closed form checked against the Euler and resource residuals in floats and in `fractions.Fraction` | 12 | Builder A |
| L02 | Log-linearization | `log-linearization` (`yaml:206`) | `lab-E6-L02-1`: the log-linear Euler equation against the exact nonlinear one; the approximation error shrinks at the rate the Taylor remainder predicts | 12 | Builder A |
| L03 | The dynamic IS curve | `dynamic-is-curve` (`yaml:203`) | `lab-E6-L03-1`: the forward recursion of the log-linear IS curve, truncated at a stated horizon, against its closed form for an AR(1) real rate | 12 | Builder A |
| L04 | The New Keynesian Phillips curve | `new-keynesian-phillips-curve` (`yaml:202`) | `lab-E6-L04-1`: the forward solution of the NKPC against the truncated sum of discounted gaps, the truncation error printed | 12 | Builder B |
| L05 | The three-equation New Keynesian model | `new-keynesian-model` (`yaml:201`) | `lab-E6-L05-1`: the three equations solved for one shock path; the residual of each equation printed at every date | 12 | Builder B |
| L06 | Solving linear rational-expectations models by undetermined coefficients | `method-of-undetermined-coefficients` (`yaml:207`) | `lab-E6-L06-1`: the coefficient matrices solved in `fractions.Fraction` and in floats, checked by substitution | 12 | Builder B |
| L07 | Determinacy and the Taylor principle | `taylor-principle` (`yaml:204`), `equilibrium-determinacy` (`yaml:205`) | `lab-E6-L07-1`: a grid over the policy coefficients; the classification by root count against the derived inequality, the boundary printed | 12 | Builder C |
| L08 | Impulse responses (**the curriculum lab**, `yaml:217`) | `impulse-response-function` (`yaml:208`) | `lab-E6-L08-1`: the three-equation impulse responses to a demand shock and a policy shock, closed form against a direct recursion | 12 | Builder C |
| L09 | Heterogeneous agents: the HANK model | `hank-model` (`yaml:209`) | `lab-E6-L09-1`: a closed-form finite check of how the share of hand-to-mouth households changes the aggregate sensitivity to the real rate; no full HANK solution | 12 | Builder D |
| L10 | Estimating DSGE models | `dsge-estimation` (`yaml:210`) | `lab-E6-L10-1`: the exact Gaussian likelihood of a scalar state-space AR(1) by the Kalman recursion, checked against the direct density; SIMULATED data with a seed | 12 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 120/30 | none | none | - | Builder A |
| project | NK model solver (`autograder`, §5) | none | `lab-E6-project-1` (rung 1), `lab-E6-project-2` (rung 2, `class="lab completion"`), `lab-E6-project-3` (rung 3 check) | 30 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `test_project.py`, `starter.py`, `ledgers/E6/mutants/`, `ledgers/E6/alternatives/` | none | none | - | Builder E |
| cards | `cards.json` from L01-L10 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes `index.html` after L01-L03 exist.
Builder E writes `project.html`, the grader and the project labs, and does not depend on the lessons' prose; it depends
only on the concepts in §3 and the notation in §2.3. Each builder owns its own output (BUILDER_RULES §1.9).

Ordering check (`tools/check_dag.py` checks linked uses only, §4 and §11 item 7):

- L01 uses E1 `competitive-equilibrium` (linked to `concepts.html`), E5 `solow-model` and `total-factor-productivity` (linked), M7 `bellman-equation`, `lagrange-multiplier` (linked), M4 `expectation` (linked; registry-free use).
- L02 uses M2 `taylor-theorem` and `derivative` (linked), M1 `exponential-and-logarithm` (linked), and L01 `rbc-model` (`L01.html#def-rbc-model`).
- L03 uses L02 `log-linearization` and M4 `expectation`; the forward-looking real rate uses E5 `policy-rate` (linked).
- L04 uses L02, M4 `expectation`, E5 `phillips-curve` and `natural-rate-of-unemployment` (linked), and L03 `dynamic-is-curve` only in prose.
- L05 uses L03 and L04 (earlier definitions) and E5 `taylor-rule` and `policy-rate` (linked).
- L06 uses L05 (`new-keynesian-model`) and M3 `linear-map` (linked).
- L07 uses L06 and M3 `eigendecomposition` (linked).
- L08 uses L06 and L07, and S3 `arma-model` and `stationarity` for the AR(1) shock (linked to `concepts.html`).
- L09 uses L01 (household primitives), L03 (IS curve), and M4 `expectation`; the HANK concepts outside the closure are plain prose (§4).
- L10 uses S1 `bayesian-inference`, `maximum-likelihood-estimation`, S3 `state-space-model` and `kalman-filter` (all in closure, linked to `concepts.html`), and M4 `multivariate-normal` and `covariance-matrix` (linked).

Hours check: 10 × 12 = 120 (hub `data-hours-lessons="120"`); project 30 (hub `data-hours-project="30"`); 150 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E6)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` (its `Architect
decisions` section is binding precedent), `plans/M7-build-plan.md` (autograder precedent), this file, and
`/Users/billyribeiro/.fanout/fixer-rules.md`. Study `course/modules/M/M7/` for the grader layout and `course/modules/E/E5/`
for the hub and lesson grammar. `course/templates/` holds the four skeletons.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or
   double-precision values stated with their tolerance, and rounded only at display. Every IRF value, steady-state value and
   coefficient states its rounding rule. Precedent: E5 §2.1 item 1; fixer-rules line 6.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Every statement "checked", "verified" or "matches" names the lab, line or test that did the
   check (E5 §2.2). Precedent: M1 LESSON_TEXT_DEFECTS; fixer-rules line 7.
3. **Attribute nothing unread.** Only the registry keys in §7.1 may be cited, and only at paper or book level unless the
   builder has read the abstract (VERIFIER §2.1). No page, table, equation, coefficient or date is typed from memory. A grade-C
   span needs a registry key or an explicit page-level basis. Precedent: fixer-rules line 8; E5 §2.1 item 3.
4. **Scope words need a computation.** "every", "all", "always", "never", "any", "only", "same", "exactly", "drives", "offsets",
   "the natural rate", "welfare", "determinacy", "the Taylor principle" are used only where a derivation, a finite check or a
   lab computes the claim. E6 scope (Q14): closed economy; log-linear three-equation NK model with a Taylor rule; Calvo pricing
   as a stated assumption; RBC as the one-sector model with Cobb-Douglas technology; HANK described with one closed-form check
   and not solved; no open economy (E8), no global nonlinear solution, no financial frictions.
5. **Define before use.** Each of the 11 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the 11 (the household's stochastic discount term, the output gap, the natural
   real rate, the Calvo parameter, the steady state, the hand-to-mouth household) are defined in prose at first use with a
   plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`; E5 §2.1 item 5).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions (A1, A2,
   ...) before the statement. "Assuming ..." appears in the statement of every result that uses an assumed fact (fixer-rules
   line 12). Examples the builders must state: the steady-state result needs `beta` in (0,1), a CRRA coefficient
   `sigma > 0`, a Cobb-Douglas capital share in (0,1), and a positive capital stock; the NKPC needs the Calvo assumptions as
   numbered Assumptions; the determinacy result needs the stated rule and the stated parameter signs; the IRF result needs
   |rho| < 1 for the shock.
7. **Grader rule (binding; §5.4 and fixer-rules line 19).** Every condition, boundary and error type the project page names
   gets its own isolated test, in both directions of each inequality. A test may demand an exception type only for a condition
   the page names; a correct implementation that raises `TypeError` for a non-number must pass unless the page says
   `ValueError`. Failure messages name the violated property and never print the expected value (`__tracebackhide__`).
   The collect-only count quoted on the page is updated.
8. **Money.** E6 has no money output. Rates, coefficients and IRFs are double-precision or `Fraction`, each with its unit
   (percent per year, or a decimal per period) and its basis (quarterly period, log or simple deviation). Precedent: E5 §2.1
   item 8 and item 11.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; escape `$` as `\$` inside math (fixer-rules line 14). `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ ==
    "__main__":` guard (fixer-rules line 7). `run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (E5 §2.1 item 10, `tools/run_labs.py` lines 51-60, not re-read by this planner). No warnings: NumPy floating-point warnings
    become errors under `-W error`, so every twin uses guarded arithmetic.
11. **Model rates are basis-explicit.** Any rate is stated with its unit, its period (quarterly or annual) and whether it is
    a log or a simple deviation. The E6 model is per period; the builders state the period once, in L02, and never change it.
12. **Labs may use NumPy and SciPy (Q11).** Recommended default: allowed. `tools/page_smoke.py:250` preloads `numpy` before
    a lab's timer starts; `tools/page_smoke.py:227` states that importing NumPy and SciPy is side-effect free. Four built
    modules declare `data-packages="numpy scipy"` (planner grep over `course/modules`). Under `-W error` every twin must be warning-free.
13. **Process words are banned in learner text** (fixer-rules line 14): no "build", "builder", "round", "verifier",
    "REQUESTS", "unit report". No planning reference in code comments (E5 §2.2).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded
  claim names its published counter-evidence (BUILDER_RULES §2.5). **The registry holds no NK Phillips-curve slope estimate, no
  Taylor-principle empirical estimate, no HANK result that this planner has read, and no DSGE estimation record that this
  planner has read.** Those claims are either derivations (grade T, conditional on the stated model) or go to
  `REFERENCE_REQUESTS` (§7.2) with the counter-evidence lead; until resolved, each empirical sentence is graded C at most with
  its basis named, or removed.
- Concepts: §1 table; `<dfn>` only for the 11 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">`
  for a concept outside the prerequisite closure (§4 and `tools/check_dag.py`).
- Prerequisite links: `href="../../../concepts.html#<id>"` for every concept from a closure unit (E1, E5, M1-M4, M7, S1, S3,
  CS1, P0.1); `href="Lnn.html#def-<id>"` for an earlier E6 lesson. A lesson never links a concept defined in a later lesson.
  Hub links: `../E5/index.html` (E5 hub, built) and `../../M/M7/index.html` (M7 hub, built); no S3 hub link (B1).
- Labs: code lives once in `tests/labs/E6/lab-E6-Lnn-1.py` and `lab-E6-project-1..3.py`. The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-E6-<page>-<n>`
  (`tools/check_pages.py` lab-id check, E5 §2.2). Seeded RNG only (`numpy.random.default_rng(seed)` or `random.Random(seed)`);
  no network; under 10 s in Pyodide; no warnings.
- SIMULATED label: on every lab, figure or grader instance that draws a stochastic path (L10 lab, the project's rung-1 path,
  the rung-2 path if stochastic). Deterministic model output (a closed-form IRF, a steady state) is labelled "model output,
  no data" (Q13).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py:58-72` `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth rates and IRF values state the convention.
- A finite enumeration (a grid of parameters) is grade C with its basis named, not grade T (E5 §2.2; M1 L06 precedent).
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3).
- Quiz explanations are read against their lesson (CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that E6 must not give a different meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered symbol | Registered meaning (locator) | E6 conflict and rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation/notation.json:112`, module S1) | **Restricted.** E6 may write `T` only for a sample length in the estimation lesson (L10), with that meaning. A forecast or impulse horizon is `H`. Transpose is `^\top`. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and inverse (`notation/notation.json:117-119`, M4) | Not used. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (`notation/notation.json:122-129`, M4) | Not used. Plain `\gamma` is free but not used. |
| `R^\ast`, `R^{e\ast}` | SDF return and projection (`notation/notation.json:132-138`, AP1) | Not used. |
| `R_f` | gross riskless return (`notation/notation.json:142-144`, AP1) | **Not used.** The nominal rate is `i_t`; the real rate is `r_t`; the natural real rate is `r^{n}_t` (E5 convention, §2.3 of E5 plan). Never write `R_t` for a gross rate. |
| `\mathbb{Q}` | a probability measure, by default risk-neutral (`notation/notation.json:147-149`, AP1) | Not used. |
| `\E` (macro, `notation/notation.json:5-8`) | expectation operator | **Use it.** Conditional expectation is `\E_t[\cdot]`. E5 wrote expected inflation as `\pi^{e}_t`; E6 must state the relation between `\pi^{e}_t` and `\E_t[\pi_{t+1}]` as an assumption or a derivation, never by identity (Q21). |
| `\R` (macro, `notation/notation.json:25-28`) | real numbers | Standard. Do not write `\mathbb{R}` (FINAL-ARCHITECT-RULINGS ruling 1). |
| `\Var`, `\Cov`, `\Corr`, `\Normal`, `\iid`, `\tr`, `\diag` (macros, `notation/notation.json:13-20, 37-44, 61-68`) | variance, covariance, correlation, normal law, i.i.d., trace, diagonal | Use for the shock-process and estimation content (L06, L10). |

Local symbols (allowed; `notation/notation.json` `about` field: letters conventionally local are defined per lesson):
`Y` output, `C` consumption, `I` investment, `K` capital, `L` labour, `N` labour force or population, `n` population growth
(defined where used), `s` saving rate, `\delta` depreciation, `\alpha` capital share, `g` growth, `u` unemployment,
`\pi` inflation, `i` nominal rate, `r` real rate, `\beta` discount factor, `\sigma` CRRA coefficient (`sigma` is named
local in `notation.json` `about`), `\kappa` Phillips slope, `\phi_\pi` and `\phi_y` policy coefficients, `\rho` shock
persistence, `\varepsilon` shock, `x_t` output gap (defined in L03), `H` horizon. Each is defined on the lesson where it first
appears and never redefined.

**E5 symbols reused by E6 (binding, Q21).** E5's built pages use `\phi_{\pi}`, `\phi_{y}`, `\pi^{e}_t`, `\bar\pi`, `\alpha`,
`\beta`, `\kappa`, `\delta`, `\eta` and `\lambda` (planner grep over `course/modules/E/E5/*.html`). E6 must read the E5 pages and
keep each shared letter's E5 meaning; `\phi_\pi` and `\phi_y` are the same Taylor coefficients. The builder greps the E5
pages before it writes L05 and records the grep output. A letter that E5 uses with another meaning is renamed in E6 and
listed in the lesson's notation note.

NOTATION_REQUESTS: none (Q21). If a symbol is needed that the registry lacks, the builder reports it under NOTATION_REQUESTS;
none is planned.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson. Derivations are
shown on the page (grade T, conditional on the Assumptions named); empirical sentences are grade C at most or removed.

- **L01** `rbc-model`: household utility with CRRA form (plain prose, §4 D3), budget constraint, Cobb-Douglas firm (E5
  `growth-accounting` and `total-factor-productivity` as background, linked), resource constraint, the planner's problem
  solved by the Lagrangian (M7 `lagrange-multiplier`, `kkt-conditions`) and by the Bellman form (M7 `bellman-equation`).
  Steady state derived in closed form (T; Assumptions for `beta` in (0,1), `sigma` > 0, capital share in (0,1)).
  Canon breaks: no nominal rigidity, no unemployment, one sector, a productivity shock as the only disturbance. Registry:
  `kydland1982time` at paper level only (its content is the time-to-build model of the title; no result attributed).
- **L02** `log-linearization`: first-order expansion of log variables around the steady state (M2 `taylor-theorem`,
  `derivative`); the log-linear Euler and resource equations for L01. The period is stated once here (per period, quarterly
  or as the builder chooses, stated). Lab: the exact versus log-linear Euler residual, error by deviation size; the claim
  "error falls quadratically" is only stated if the printed numbers show it.
- **L03** `dynamic-is-curve`: the log-linear Euler equation as the dynamic IS curve, `x_t = \E_t[x_{t+1}] - (1/\sigma)(i_t - \E_t[\pi_{t+1}] - r^{n}_t)`
  in the builder's notation after derivation (T conditional on the L02 Assumptions); the output gap `x_t` defined here. Forward
  solution for an AR(1) natural rate, the truncation error at horizon `H` stated. Canon breaks: the closed economy with no
  financial frictions; the natural real rate taken as given.
- **L04** `new-keynesian-phillips-curve`: Calvo staggered pricing as a stated Assumption (plain prose, no citation, §4 D8).
  The derivation of `\pi_t = \beta \E_t[\pi_{t+1}] + \kappa x_t` is shown with its assumptions (T conditional). The meaning of
  `\kappa` as a composite of the Calvo parameter and the curvature of marginal cost is derived, not typed from memory. Forward
  solution as a discounted sum of gaps (lab checks the truncation). Connects to E5 `phillips-curve` and
  `natural-rate-of-unemployment` (linked) by contrast: the E5 curve is not forward-looking; the E6 curve is. Canon breaks: no
  price dispersion beyond the Calvo assumption; the slope is a model parameter; no empirical slope is claimed (grade C only
  with a registry key, none available in §7.1: REFERENCE_REQUESTS, §7.2).
- **L05** `new-keynesian-model`: the three equations (dynamic IS, NKPC, Taylor rule with E5's `\phi_\pi`, `\phi_y`), the
  system in a single form, its exogenous shock process. Links to E5 `taylor-rule` and `policy-rate`. Lab: one shock path
  solved, the residual of each equation at each date printed (the residuals must be zero to the stated tolerance).
- **L06** `method-of-undetermined-coefficients`: guess `\pi_t = a u_t`, `x_t = b u_t` for an AR(1) shock `u_t`; the linear system
  for `a`, `b` solved; the solution is unique when the system is nonsingular (Assumption). Lab: coefficients in `fractions.Fraction`
  for rational parameter values and in floats, checked by substitution. Registry: no paper cited for the method beyond the
  name; the method is a derivation (T). Canon breaks: the guess must fit the shock process; no general solution method is
  claimed here (the general linear solver is a REFERENCE_REQUEST lead, §7.2).
- **L07** `taylor-principle`, `equilibrium-determinacy`: for the two forward-looking equations and the rule, the count of
  roots of the coefficient system outside the unit circle versus the number of forward-looking variables. The Taylor principle
  is derived as the condition that the rule raises the real rate enough: the inequality is derived on the page (T) and
  checked in the lab over a grid (grade C naming the lab, because a grid is finite). The equality (boundary) case and the
  sign conditions are stated explicitly and tested in both directions (§5.4). Canon breaks: indeterminacy and sunspot
  equilibria are **not stated** here (no registry source read; REFERENCE_REQUESTS, §7.2); determinacy depends on the
  log-linearization (L02) and on the rule's form.
- **L08** `impulse-response-function` (**curriculum lab, `yaml:217`**): deterministic impulse responses of `x`, `\pi`, `i`
  to a unit demand shock and a unit policy shock; the recursion and the closed form agree (lab); the sign of each response
  is stated and derived (T). Shock processes from S3 `arma-model` and `stationarity` (linked to `concepts.html`). Canon
  breaks: no persistence beyond the stated AR(1); no nonlinearity; the policy shock is an exogenous deviation from the rule.
- **L09** `hank-model`: the heterogeneous-agent setting described in prose: two household types (hand-to-mouth and forward-looking),
  incomplete markets, the aggregate Euler equation's sensitivity to the real rate as a function of the hand-to-mouth share
  (one closed-form finite check in the lab; the builder derives the expression). The paper `kaplan2018monetary` is cited at
  paper level for the model's existence only; no number from it is used (it has not been read; VERIFIER §2.1). Dynamic
  programming and the wealth distribution are named in plain prose (§4 D2, D7). Canon breaks: the model's computational
  solution is not implemented; the lab is a finite check of one derived expression only.
- **L10** `dsge-estimation`: state-space form of the log-linear model; the Kalman recursion (S3 `kalman-filter`,
  `state-space-model`, linked); the Gaussian likelihood as a function of the parameters (S1 `maximum-likelihood-estimation`,
  linked); Bayesian updating as a definition (S1 `bayesian-inference`, linked). Lab: exact likelihood of a scalar AR(1) state
  with a seeded SIMULATED path, the Kalman value compared with the direct Gaussian density at the stated tolerance. No
  empirical estimate for E6's model is typed (none read). Canon breaks: identification and the prior are model choices; the
  lab is a one-state check, not an estimation of the NK model.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it (for example,
  fixed Calvo pricing in L04, one-sector technology in L01, a linear rule in L05).
- No lesson uses a term from E7 (monetary transmission, FTPL), E8 (open economy, `uncovered-interest-parity`) or AP
  (`stochastic-discount-factor`, `consumption-capm`) as a concept (§4).

---

## 4. DAG problems (concepts that natural E6 content would use outside the closure)

Prerequisite closure of E6 (computed, §0.1): **{CS1, E1, E5, M1, M2, M3, M4, M7, P0.1, S0, S1, S2, S3}**, with 176
usable concepts. Owners below are from `curriculum/curriculum.json` `concepts` (planner check via `concept_owner()`).
Concepts inside the closure that E6 uses are linked, not redefined: E5 (`taylor-rule`, `policy-rate`,
`phillips-curve`, `natural-rate-of-unemployment`, `business-cycle`, `solow-model`, `total-factor-productivity`); M7
(`bellman-equation`, `lagrange-multiplier`, `kkt-conditions`); M2 (`taylor-theorem`, `derivative`, `jacobian`,
`implicit-function-theorem`); M3 (`linear-map`, `eigendecomposition`); M4 (`expectation`, `covariance-matrix`,
`multivariate-normal`); S3 (`arma-model`, `stationarity`, `state-space-model`, `kalman-filter`, `vector-autoregression`);
S1 (`bayesian-inference`, `maximum-likelihood-estimation`).

| Ref | Concept | Owner (outside closure, `concept_owner`) | Where natural E6 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `rational-expectations-equilibrium` | E4 | every forward-looking equation (L03-L07); the term "rational expectations" | Plain prose, no link (default, Q3). Architect may add E4 as a prerequisite (curriculum change). |
| D2 | `dynamic-programming` | CS2 | the household and planner problems in L01, L09 | Use `bellman-equation` (M7, in closure, linked) for the recursive form; the words "dynamic programming" in plain prose, no link (Q4). |
| D3 | `crra-utility`, `expected-utility` | E3 | household utility in L01, L03, L09 | The CRRA form written out as an explicit Assumption, plain prose, no link (default, Q5). Architect may add E3. |
| D4 | `euler-equation-gmm`, `consumption-capm`, `stochastic-discount-factor` | AP3, AP1 | the consumption Euler equation (L03) | "The consumption Euler equation" in plain prose; no SDF or CAPM language (Q6). |
| D5 | `value-function-iteration`, `banach-fixed-point-theorem`, `newtons-method`, `monte-carlo-integration` | M5, M8 | any numerical solution of the model | Not used by the reference solver: linear algebra only (M3, closure) (Q7). No fixed-point claim. |
| D6 | `narrative-shock-identification`, `high-frequency-monetary-surprise`, `fiscal-theory-of-the-price-level` | E7 | empirical monetary shocks (L08), fiscal regimes | Not used. The policy shock is an exogenous deviation from the rule, stated as such. |
| D7 | `heterogeneous-agent-asset-pricing`, `incomplete-markets` (no concept) | AP4 (the first only) | HANK (L09) | Plain prose only. |
| D8 | Calvo staggered pricing (no concept in the curriculum; planner grep of concept ids found none) | none | NKPC derivation (L04) | Plain prose, stated as an Assumption; no citation (default). A registry source for Calvo is not in §7.1 (§7.2 lead). |
| D9 | Blanchard-Kahn solution condition (no concept in the curriculum) | none | counting roots (L07) | Plain prose, named as a lead only (§7.2); the counting argument is derived on the page. |
| D10 | `markov-decision-process`, `policy-iteration`, `policy-gradient` | QR5, SC6, QR5 | none planned | Not used. |
| D11 | `first-welfare-theorem`, `noisy-rational-expectations-equilibrium` | E4 | welfare of the RBC allocation (L01) | Not used. No welfare statement is made. |
| D12 | `expectation` (M4, in closure) | M4 | every `\E_t` | Allowed, linked. Not outside the closure. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **D1, D2, D3 need the architect's confirmation (§12 Q3-Q5).**
`tools/check_dag.py` checks linked uses only (`tools/check_dag.py` lines 11, 68); an unlinked use of D1-D11 passes the tool,
so the verifier reads every lesson for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): autograder, ladder, spec, grader, mutants, alternatives

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:84-90` requires the order and a completion lab or quiz)

Tier M: rungs 1-2 are kept to the minimum (BUILDER_RULES §5.1; BLUEPRINT §4 expertise reversal).

1. **Rung 1, worked example** (`lab-E6-project-1`, model output, no data): one fully solved, annotated computation of the
   steady state, the log-linear coefficients for one default parameter set, and the first three IRF values. Each step has a
   "why" annotation. Short (about 2 h, §5.3).
2. **Rung 2, completion problem** (`lab-E6-project-2`, `class="lab completion"`): the determinacy check line and the
   coefficient line are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the
   twin line or contains a blank (E5 §5.1 item 2; FINAL-ARCHITECT-RULINGS ruling 11).
3. **Rung 3, independent project** (graded by the autograder, §5.3): the solver module `nk_solver.py`, the IRF file
   `irf.csv`, and the figure set (§5.2). `lab-E6-project-3` is the rung-3 check: it runs the reference on the page's default
   seed and prints the table the student's solver must reproduce (the reference is not printed, only its output table).
4. **Rung 4, stretch** (optional, not graded): a cost-push shock added to the NKPC and the change in the determinacy region,
   stated as a hypothesis before the run.

### 5.2 Spec (`course/modules/E/E6/project.html`, grader panel and spec)

`check_projects.py` requires the terms context, inputs, required outputs, constraints and grading (E5 §5.2 precedent). The
spec's grading entry must name the word "autograder" (`tools/check_projects.py:38`).

- **Context.** A monetary economist must solve a three-equation NK model for a policy rule, state whether the solution is
  determinate, and report the impulse responses to two shocks. The solver must give the same answers the reference gives,
  and it must refuse invalid parameters with the named error.
- **Inputs.** No data file. One parameter set per seed, drawn by `make_instance(seed)` (grader/instance.py). The page states
  the ranges of each parameter (`beta`, `sigma`, `kappa`, `phi_pi`, `phi_y`, `rho`) and the seed derivation from the
  workspace ID. Every instance is valid (grader rule, §5.3). The planner did not type any range value; the builder states the
  ranges and the reference enforces them.
- **Required outputs** (exact names; the builder fixes the final signatures and the reference is written to them):
  - `nk_solver.py` containing `solve_undetermined(params) -> tuple` returning the coefficient matrices for the state
    `u_t`, the function `is_determinate(params) -> bool` for the stated rule, and `impulse_responses(params, horizon) -> dict`
    returning the output-gap, inflation and rate paths for `horizon + 1` dates (date 0 included).
  - `irf.csv` written by the student's script from `impulse_responses`, with a header row and one row per date.
  - A figure set (the student's choice of tool). The figures are not graded; they must be drawn from `irf.csv` (stated).
  - Named errors: `ValueError` for invalid input (`beta` not in (0,1); `sigma` not positive; `kappa` not positive; `|rho| >= 1`;
    `horizon` not a non-negative integer) and `ValueError` when `solve_undetermined` is called for an indeterminate rule.
    No other exception type is named, so no test demands one.
- **Constraints.** Standard library or NumPy and SciPy (the grader panel declares `data-packages="numpy scipy"`, Q11).
  Each stated tolerance is the one the grader uses (§5.4, ruling 22 of FINAL-ARCHITECT-RULINGS: the tolerance binds the grader).
  A solver that is correct inside the stated tolerance but differs outside it is not accepted.
- **Grading.** Autograder (`grader/`), dual-mode (Pyodide and local `pytest`). Figure set and write-up: ungraded (Q12).
  Not adversarial (Q17).
- **Reading list** (`ol.reading-list`, registry keys only, §7.1): `kydland1982time`, `clarida1999science`, `gali2015monetary`,
  `woodford2004interest` (cited by key only, no year, B3), `kaplan2018monetary`. Nothing else.
- **The data-packages note.** `data-packages="numpy scipy"` on the grader panel (precedent: four built modules).

### 5.3 Time budget (`<table id="hours">`, sums to 30 h; every row needs a one-line rationale; `check_projects.py` lines 107-118)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved default case, annotated line by line |
| Rung 2, completion problem | 2 | Fill the determinacy line and the coefficient line, then run the instant check |
| Derive the log-linear system and the coefficient equations by hand | 6 | Write the derivation from the model in the spec's notation; check each step against L05-L06 |
| Implement `solve_undetermined` and `is_determinate` | 6 | Two functions, the named errors, the stated tolerance |
| Implement `impulse_responses` and write `irf.csv` | 4 | Date 0 included, the horizon edge cases, the header row |
| Test the solver against the spec's cases (own tests) | 5 | Boundary of the determinacy rule, invalid inputs, residual checks |
| Figure set from `irf.csv` and a short write-up | 5 | Two figures, axes and units stated, one caption per figure |
| **Total** | **30** | Equals `data-hours-project` on the hub |

Estimate check (verifier): each row is within the 30% band of §5.3's total; the planner's own estimate is 30 h (the total is
not in dispute).

### 5.4 Grader design (autograder; `course/modules/E/E6/grader/`)

**Files.** `grader/instance.py` (`make_instance(seed: int) -> dict`, deterministic, valid for every seed, materially different
per seed, returns a regime-balanced mix: about half the seeds are determinate under the stated rule and about half are not,
so both directions of the determinacy test are exercised); `grader/reference.py` (full solution, passes seeds 0-49);
`grader/test_project.py` (pytest suite, properties and numbers); `grader/starter.py` (the student's starting file, with the
three named functions and their docstrings, no answers). The grader panel carries `data-unit="E6" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="reference.py" data-starter="starter.py"
data-packages="numpy scipy"` (attribute names as `tools/check_projects.py:127-131` requires; the M7 panel at
`course/modules/M/M7/project.html:359` is the template).

**Oracles (two independent methods, both in the reference).** (i) Determinacy by root count: the number of roots of the
coefficient system outside the unit circle, compared with the number of forward-looking variables. (ii) Determinacy by the
inequality derived on L07, checked as an identity at each seed. The two must agree on every seed. The planner did not type
the inequality; the builder derives it on L07 and the reference implements it. **Coefficients** by two methods: the linear
solve (undetermined coefficients) and the root-based solve, both checked by substitution into the three equations.

**Tests (each isolated; both directions where an inequality is stated; the list is the page's named conditions).**
1. Invalid input raises `ValueError`: `beta` = 0, `beta` = 1, `beta` > 1 (three tests); `sigma` = 0 and `sigma` < 0 (two);
   `kappa` = 0 and `kappa` < 0 (two); `rho` = 1, `rho` = -1 and `|rho|` > 1 (three); non-integer and negative `horizon` (two).
   Each is its own test and each names the parameter in the message without printing the expected value.
2. Accept at the edges of valid input: `beta` just inside (0,1); `rho` = 0; `horizon` = 0 returns one date.
3. Determinacy at the boundary: for the page's rule and seed-chosen `kappa`, `beta`, `phi_y`, two tests at `phi_pi` one
   tolerance step above and one below the boundary (the boundary is the one the reference computes from the derived
   inequality), each direction its own test.
4. Indeterminate rule: `solve_undetermined` raises `ValueError` (named on the page); `is_determinate` returns `False`.
5. Residuals: the solution satisfies the three equations at every date to the stated tolerance (`1e-10` times
   `max(1, |expected|)`, ruling 22).
6. Agreement: `solve_undetermined` and the root-based coefficients agree to the stated tolerance.
7. IRF shape: `impulse_responses` returns `horizon + 1` dates; date 0 is the impact date.
8. IRF sign: a positive demand shock raises output on impact; a positive policy shock raises the rate on impact (the sign
   convention stated on the page).
9. IRF decay: for determinate parameters with `|rho|` < 1 the path at the last date is below the stated threshold.
10. `irf.csv`: header row names the columns named on the page; values match the reference to the stated tolerance on the
    default seed.
11. Seed sweep: the same suite passes the reference on seeds 0-49 (`tools/run_graders.py --unit E6 --seeds 0-49`,
    `tools/run_graders.py:138-139` runs only units with grading `autograder`).

Failure messages name the violated property and give a hint at the concept (for example "the solution must satisfy the
Phillips curve at every date; check the forward term's timing in L04"). They never print the expected value
(`__tracebackhide__`, fixer-rules line 19). Each test finishes in under 5 s in Pyodide and the suite in under 60 s
(BUILDER_RULES §5.3.4).

**Integrity.** The suite is public; integrity rests on per-seed instances (BLUEPRINT §5.2). The page does not claim secrecy.

**Mutants (ten student errors, `ledgers/E6/mutants/`, each a single-change copy of the reference, first docstring line
naming the error; `tools/mutate_graders.py` reads that directory, `tools/mutate_graders.py:41-43`; each must fail at least one test).**
The planner lists the error classes; the verifier writes the code and the builder does not.
- m01: determinacy check drops the output-gap term of the derived inequality (uses the inflation-only part).
- m02: determinacy check uses a non-strict inequality where the page states a strict one (boundary test, §5.4 item 3).
- m03: NKPC forward term dated `t` instead of `t+1` (uses `\pi_t` for `\E_t[\pi_{t+1}]`).
- m04: IRF applies the shock at date 1 instead of date 0 (off-by-one horizon).
- m05: solver picks the explosive root when a quadratic has two real roots (root-selection error).
- m06: real rate computed ex post (`i_t - \pi_t`) instead of ex ante (`i_t - \E_t[\pi_{t+1}]`).
- m07: sign of the policy shock flipped in `impulse_responses` (rate falls on impact).
- m08: the policy rate reported as an annual percentage without the stated conversion (units).
- m09: a hard-coded answer for seed 0 (the solver returns the seed-0 table for all inputs).
- m10: invalid input accepted without raising (for example `sigma` <= 0 passes through), a named error missing.

If a mutant differs from the reference only where the page states nothing, it goes to `ledgers/E6/equivalent/` with a README
proof (FINAL-ARCHITECT-RULINGS ruling 9). A mutant that differs only inside a stated tolerance goes to `equivalent/` with a
measured sweep, labelled as measured and not proved (rulings 25 and 40 precedent). No mutant is authored at the tolerance
boundary (ruling 25).

**Alternatives (five correct implementations of different styles; each passes seeds 0-49, `ledgers/E6/alternatives/`; FINAL-ARCHITECT-RULINGS ruling 10).**
- alt1: undetermined coefficients as a linear system solved by `numpy.linalg.solve`.
- alt2: companion-matrix eigendecomposition for determinacy (root count) and for the coefficients.
- alt3: a generalized eigenproblem solved by the QZ decomposition from SciPy, then the same counting rule.
- alt4: iterative coefficient solve (fixed-point on the coefficient matrix) that returns only after an exact residual check
  passes, otherwise raises (the iterative style differs from the direct solves).
- alt5: exact arithmetic with `fractions.Fraction` for the coefficient system, converted to float at output, with the same
  tolerances.

An alternative that is wrong on a stated exact rule is a mutant, not an alternative (ruling 10).

**Commands (for the builder and the verifier; run from the repo root).**

```bash
.venv/bin/python tools/run_graders.py --unit E6 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit E6 --seeds 0-9
.venv/bin/python tools/page_smoke.py --unit E6        # verifier only, alone, quiet machine
```

---

## 6. Real-data policy (no real data is needed)

- **No embedded dataset.** E6's lab, its project and its grader use model output and seeded simulations only. No
  `course/assets/data/market/` entry is needed. No `data-files` attribute on any lab. No MANIFEST entry is added by builders.
  No DATA_REQUESTS entry. This differs from E5 (E5 B1), whose curriculum lab names national-accounts data
  (`curriculum/02-economics-finance-core.yaml:183`); E6's lab (`yaml:217`) names no data.
- **Stochastic paths** (L10 lab; the project's rung-1 and rung-2 paths if any are stochastic) are labelled SIMULATED on the
  page and in the lab's hypothesis line (BUILDER_RULES §1.7).
- **Deterministic model output** (the steady state, the closed-form IRF) is labelled "model output, no data" (Q13).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`; line numbers are the `"key"` lines)

| Key | Record (as read, `references/references.json`) | Curriculum string (`yaml`) | Status and use in E6 |
|---|---|---|---|
| `kydland1982time` | Kydland & Prescott, "Time to Build and Aggregate Fluctuations", Econometrica, volume 50, issue 6, year 1982, DOI 10.2307/1913386 (`references/references.json:15242`) | "Kydland & Prescott (1982), Econometrica 50(6)" (`yaml:212`); matches | verified, `used_by: ["E6"]`. L01 (paper level, no result attributed); reading list |
| `clarida1999science` | Clarida, Galí & Gertler, "The Science of Monetary Policy: A New Keynesian Perspective", JEL, volume 37, issue 4, year 1999, pages 1661-1707, DOI 10.1257/jel.37.4.1661 (`references/references.json:5433`) | "Clarida, Galí & Gertler (1999), JEL 37(4)" (`yaml:213`); matches | verified, `used_by: ["E6"]`. L05 (paper level); reading list |
| `gali2015monetary` | Galí, "Monetary Policy, Inflation, and the Business Cycle: ... Second Edition", Princeton University Press, year 2015, ISBN 9780691164786 (`references/references.json:9634`) | "Galí, Monetary Policy, Inflation, and the Business Cycle, 2nd ed. (2015)" (`yaml:214`); matches the record's second edition | verified (Open Library), `used_by: ["E6"]`. L05, L08 (book level); reading list |
| `woodford2004interest` | Woodford, "Interest and Prices: Foundations of a Theory of Monetary Policy", Princeton University Press, year 2004, DOI 10.1515/9781400830169 (`references/references.json:23317`); `notes.year` `{curriculum: "2003", crossref: "2004"}` | "Woodford, Interest and Prices (2003)" (`yaml:215`); **year conflict (B3)** | verified, `used_by: ["E6"]`. Cite the key only, with no year or edition typed in prose; reading list |
| `kaplan2018monetary` | Kaplan, Moll & Violante, "Monetary Policy According to HANK", AER, volume 108, issue 3, year 2018, pages 697-743, DOI 10.1257/aer.20160042 (`references/references.json:14263`) | "Kaplan, Moll & Violante (2018), AER 108(3)" (`yaml:216`); matches | verified, `used_by: ["E6"]`. L09 (paper level, no number used); reading list |
| `stokey1989recursive` | Stokey, Lucas & Prescott, "Recursive Methods in Economic Dynamics", Harvard University Press, year 1989, ISBN 9780674735187 (`references/references.json:21298`; `used_by: ["M7"]`) | **not curriculum-listed for E6** | verified (Crossref), `used_by: ["M7"]`. Optional book-level use in the reading list for dynamic-programming content (Q10). Default: not cited in E6 |
| `taylor1993discretion` | Taylor, "Discretion versus policy rules in practice", Carnegie-Rochester Conference Series, volume 39, year 1993, pages 195-214, DOI 10.1016/0167-2231(93)90009-l (`references/references.json:21688`) | **not curriculum-listed for E6** (used by E7) | verified, `used_by: ["E7"]`. Default: not cited in E6 (Q9) |

Not used by E6: `solow1956contribution` (E5), `hicks1937mr` (E5), `phelps1968money` (E5), `blanchard2020macroeconomics` (E5, B4 of E5 plan),
`sims1980macroeconomics` (S3), `bernanke2020new`, `romer2004new`, `kydland1977rules`, `barro1983positive` (E7),
`hansen1982generalized` (AP3), `calvo1998capital` (E9; a sudden-stops paper, not the Calvo pricing model).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

The planner did not type authors, years or venues for these. Each is a lead the architect resolves through
`tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until a record is admitted, the
lessons teach the model with derivations and no empirical attribution.

- {doi: null, authors: "solution method for linear rational-expectations models (lead only; authors not typed)", year: "not typed", title: "the standard solution method and root-counting condition for linear rational-expectations systems (lead only)", venue: "not typed", needed_for: "L07 root-counting statement and the attribution of the counting condition (D9)", confidence: "the need is certain; the lead is the planner's recall and is unverified; no record identified"}
- {doi: null, authors: "linear rational-expectations solution literature, second source (lead only)", year: "not typed", title: "a second solution method for linear rational-expectations models (lead only)", venue: "not typed", needed_for: "L06 cross-check of the coefficient method (optional)", confidence: "optional; unverified lead"}
- {doi: null, authors: "Calvo staggered-pricing literature (lead only; authors not typed)", year: "not typed", title: "staggered price-setting with a constant reset probability (lead only)", venue: "not typed", needed_for: "L04 only if the builder wants a citation for the Calvo assumption (default: plain prose, no citation; D8)", confidence: "the need is optional; unverified lead"}
- {doi: null, authors: "empirical literature on the New Keynesian Phillips-curve slope (lead only)", year: "not typed", title: "estimates of the forward-looking inflation equation (lead only)", venue: "not typed", needed_for: "L04 two-sided treatment of any empirical sentence about the slope (BUILDER_RULES §2.5); until resolved, the sentence is removed", confidence: "the need is certain; no record identified by this planner"}
- {doi: null, authors: "empirical literature on Taylor-principle determinacy and indeterminacy (lead only)", year: "not typed", title: "estimates of the policy-rule coefficients and the determinacy region (lead only)", venue: "not typed", needed_for: "L07 counter-evidence for any empirical claim about the Taylor principle", confidence: "the need is certain; no record identified by this planner"}
- {doi: null, authors: "literature on sunspot and indeterminacy equilibria (lead only)", year: "not typed", title: "indeterminacy and self-fulfilling expectations (lead only)", venue: "not typed", needed_for: "L07 canon-breaks sentence on indeterminacy (currently not stated; §3)", confidence: "optional; unverified lead"}
- {doi: null, authors: "empirical literature on heterogeneous-agent models and the transmission of monetary policy (lead only)", year: "not typed", title: "estimates of the hand-to-mouth share and the aggregate sensitivity to the real rate (lead only)", venue: "not typed", needed_for: "L09 two-sided treatment; until resolved, no empirical sentence is made", confidence: "the need is certain; no record identified by this planner"}
- {doi: null, authors: "DSGE estimation literature (lead only)", year: "not typed", title: "estimated medium-scale DSGE models and their likelihood (lead only)", venue: "not typed", needed_for: "L10 any empirical claim about estimated parameters (default: none made)", confidence: "optional; unverified lead"}

Blanchard & Kahn is named in §4 D9 only as the lead above. No record, year or venue is typed for it.

---

## 8. Atlas milestone

None. No Atlas entry names E6 (§0.1); the E6 project entry has no `atlas` key (`yaml:218-225`). No
`atlas/E6.contract.md` is needed. `tools/check_projects.py` skips the contract check when no `atlas` key is present
(`tools/check_projects.py:144-146` per E5 §11 item 1). The `atlas/` directory is not touched by builders.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/E/E6/cards.json`, ids `E6-c001` upward (non-sequential ids are not defects, FINAL-ARCHITECT-RULINGS ruling 2),
  `lesson` in L01-L10, one card per definition, theorem statement, key formula, key result and misconception
  (BUILDER_RULES §7). `tools/check_pages.py` checks the id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab L06, derivation 2 (exact)"` (FINAL-ARCHITECT-RULINGS ruling 13). A value that appears only in a lab's output is
  graded C with the lab named.
- Cite a registry key only for an empirical or attributed claim (§7.1). `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- A card and the key-results row it mirrors carry the same grade and basis (ruling 13).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit E6            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E6
.venv/bin/python tools/check_projects.py --unit E6
.venv/bin/python tools/run_labs.py --unit E6               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E6/L01.html        # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/E/E6/L02.html --refresh lab-E6-L02-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit E6 --seeds 0-49               # project builder, after grader files exist
.venv/bin/ruff check tests/labs/E6 course/modules/E/E6/grader && .venv/bin/ruff format --check tests/labs/E6 course/modules/E/E6/grader
.venv/bin/mypy tests/labs/E6 course/modules/E/E6/grader    # strict, repository configuration
```

Not run for E6 by builders:

- `tools/page_smoke.py --unit E6` (verifier only, on a quiet machine; timing-sensitive; `tools/page_smoke.py:227-253`).
- `tools/mutate_graders.py --unit E6 --seeds 0-9` is run by the verifier after the mutants are written (§5.4).
- `tools/verify_refs.py --unit E6` (the unit ledger's run, VERIFIER §2.1; uses the network, so the verifier runs it).
- `tools/fetch_data.py --check` is not needed (no dataset).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. The gate is run once before the push, not after each edit (user policy: targeted tests).

Flag checks: `tools/check_pages.py` and `tools/check_dag.py` accept `--unit`; `tools/check_projects.py` accepts `--unit`;
`tools/run_labs.py` accepts `--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`.
The planner ran only the coursekit closure and concept-owner functions (§0.1); no builder command was executed by the planner.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **E1 is built.** E5's plan (§6 and §11 item 6) says E1 is not built; that is stale. `course/modules/E/E1/` exists with
   a PASS ledger (`ledgers/E1.verification.json`). E6's closure contains E1 (§0.1), so E1 concept anchors are linkable.
2. **Unbuilt closure units.** CS1, P0.1, S0, S1, S2 and S3 have no built module (§0.1). Their concept anchors exist in
   `course/concepts.html` (planner grep: `id="kalman-filter"`). Links from E6 go to those anchors only (B1).
3. **No Atlas milestone** (§8). `check_projects.py` skips the contract check when no `atlas` key exists (E5 §11 item 1).
4. **No debate.** E6 has no `debate:` key (§0.1); no debate brief is required. The NK claims are contested, so the two-sided
   rule (BUILDER_RULES §2.5) applies anyway (§7.2 leads).
5. **Autograder, not rubric.** E6's grading is `autograder` (`yaml:225`). `check_projects.py` requires the grader panel
   (`tools/check_projects.py:122-137`), the files, and `make_instance(seed: int)` (`tools/check_projects.py:136`). No
   rubric or exemplars are required.
6. **Mutant count.** `tools/mutate_graders.py:41-43` requires at least three mutants; the rule for E6 is ten (§5.4, fixer-rules
   line 19). The rule is stricter and governs.
7. **check_dag sees linked uses only** (`tools/check_dag.py` lines 11, 68). The unlinked uses in §4 (D1-D11) pass the tool;
   the verifier reads for them (VERIFIER §2.9).
8. **Labs may use NumPy.** The lab runtime preloads NumPy (`tools/page_smoke.py:250`). The E5 rule "standard library only"
   (E5 §2.1 item 10 neighbourhood) is E5's own; for E6 it is replaced by the Q11 default.
9. **Hub prerequisites.** The hub has a prerequisites section (`tools/check_pages.py:347`), a placement diagnostic
   (`tools/check_pages.py:350-354`: `section.quiz#placement` with `data-mastery` and at least two `data-skill` items), a lesson
   map and a ladder. The S3 prerequisite has no hub, so it is named in text (B1).
10. **Honest gap for the first-year group.** `curriculum/meta.yaml:133` lists E5, E6 and E7 as one group (no action; Q15).

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **Lesson count and hours (Q1).** Confirm 10 lessons × 12 h and a 30 h project (20%). Alternatives within the rules:
   11 × 10 h and a 40 h project (26.7%); or 9 × 12 h and a 42 h project (28%). **RECOMMENDED: 10 × 12 h + 30 h.**
2. **Unbuilt prerequisite S3 (B1, Q2).** Confirm that E6 proceeds while S3 is unbuilt, with S3 concepts linked to
   `concepts.html` anchors and named as text in the hub. **RECOMMENDED: proceed; state the gap on the hub and in the
   architect's merge note.** Alternative: defer L08 and L10 until S3 is built.
3. **Rational expectations (D1, Q3).** `rational-expectations-equilibrium` (E4) is needed by every forward-looking equation.
   **RECOMMENDED: plain prose "rational expectations", no link, no dfn** (E5 default, E5 plan line 563). Alternative: add E4 to
   E6's prerequisites (a curriculum change the builders may not make).
4. **Dynamic programming (D2, Q4).** **RECOMMENDED: use `bellman-equation` (M7, linked) for the recursive form; "dynamic
   programming" in plain prose only.**
5. **CRRA and expected utility (D3, Q5).** **RECOMMENDED: write the CRRA form as an explicit Assumption, plain prose, no link.**
   Alternative: add E3 as a prerequisite (E3 is outside the closure, so this is a curriculum change).
6. **Euler equation and SDF language (D4, Q6).** **RECOMMENDED: "consumption Euler equation" in plain prose; no SDF or CAPM terms.**
7. **Numerical methods (D5, Q7).** **RECOMMENDED: the reference solver uses linear algebra only (M3 closure), with no fixed-point
   or Newton claim.** Alternative: add M5 or M8 (curriculum change).
8. **Woodford year (B3, Q8).** **RECOMMENDED: cite `woodford2004interest` by key with no year or edition in prose.** The architect may
   correct `yaml:215` after checking the record and the edition. The builders do not edit `curriculum/*.yaml`.
9. **Taylor 1993 (Q9).** `taylor1993discretion` is verified and used by E7 (§7.1). **RECOMMENDED: not cited in E6** (the rule is
   a definition in L05). Alternative: cite it at paper level for the rule's name, with architect approval (E5 Q4 precedent).
10. **Book-level recursive methods (Q10).** `stokey1989recursive` is verified and used by M7. **RECOMMENDED: optional book-level
    entry in the reading list for L01 and L09 dynamic-programming content; no claim attributed to it.**
11. **NumPy and SciPy in labs and grader (Q11).** **RECOMMENDED: allowed** (§2.1 item 12; four built modules use
    `data-packages="numpy scipy"`).
12. **Figures (Q12).** No live figures in the lessons (E5 Q13 precedent; no kernel). The project's figure set is the student's,
    drawn from `irf.csv`, and is ungraded. **RECOMMENDED: as stated.** If the architect wants a live IRF figure, it needs a
    kernel and a test (BUILDER_RULES §6.4).
13. **Simulated and model-output labels (Q13).** **RECOMMENDED: stochastic paths labelled SIMULATED; deterministic model output
    labelled "model output, no data".**
14. **Scope (Q14).** Confirm §2.1 item 4: closed economy; log-linear three-equation NK model with a Taylor rule; Calvo pricing as an
    assumption; one-sector RBC with Cobb-Douglas technology; HANK described with one finite check; no open economy (E8); no global
    nonlinear solution; no financial frictions. **RECOMMENDED: confirm.**
15. **First-year group (`curriculum/meta.yaml:133`).** The group lists E5, E6 and E7 as one sequence while E6 is tier M. No action
    planned. **RECOMMENDED: confirm no action.**
16. **Autograder interface and exceptions (Q15).** Confirm the names in §5.2 (`nk_solver.py`, three functions, `irf.csv`) and that
    the only named exception type is `ValueError`. **RECOMMENDED: confirm.** The builder fixes final signatures and the reference
    is written to them.
17. **Adversarial question bank (Q17).** The project is an autograder, not a debate or an IC defence. No question bank.
    **RECOMMENDED: none.**
18. **Atlas (Q18).** None. **RECOMMENDED: confirm (§8).**
19. **Counter-evidence (Q19).** Every empirical sentence in E6 is graded C at most with its basis named, or removed, until §7.2
    items are resolved. **RECOMMENDED: request the §7.2 leads from the architect now.**
20. **Lead-only entries (Q20).** The §7.2 leads (linear rational-expectations solution method, Calvo, sunspots, HANK evidence,
    DSGE estimation evidence) are lead-only and typed without bibliographic data. **RECOMMENDED: the architect resolves through
    `add_reference.py`; no lead is typed as a record by a builder.**
21. **Notation reuse from E5 (Q21).** **RECOMMENDED:** E6 uses `\E_t` for conditional expectation (registered macro); E5's
    `\pi^{e}_t` keeps its E5 meaning; L03 and L04 state the relation between them as an assumption, never an identity; `\phi_\pi`,
    `\phi_y` are the E5 Taylor coefficients; a letter that E5 uses with another meaning is renamed in E6 and listed in its notation
    note.
22. **Hub prerequisite links (Q22).** **RECOMMENDED:** link E5 and M7 hubs; name S3 in text only (B1).
23. **Lesson-hours overrun (Q23).** Lessons at 12 h are at the maximum. **RECOMMENDED:** a builder that needs more time reports it;
    the architect chooses Q1's alternative. No lesson is declared above 12 h.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05-L06, L07-L08 (includes the curriculum lab),
   L09-L10, the project (grader, mutants, alternatives, rung-2 twin match). Failing rows return to the builder that owns the
   file, with only the failing rows.
3. Ledger at `ledgers/E6.verification.json`. Mutants at `ledgers/E6/mutants/` (ten, §5.4), alternatives at
   `ledgers/E6/alternatives/` (five), equivalents at `ledgers/E6/equivalent/` with a README per equivalent (ruling 9).
   Verifier scripts archived under `ledgers/E6/scripts/` (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 (S3) and B2 (D1-D3)
   must be resolved or named as honest gaps first. The full gate runs once, immediately before the push (user policy).

Architect decisions: pending (§12). This plan is the planner's proposal.

## Architect decisions

Pending. The planner records no decision. The architect fills this section with the answers to §12 Q1-Q23 before any builder starts.
